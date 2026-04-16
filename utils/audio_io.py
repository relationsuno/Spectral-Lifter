import numpy as np
import librosa
import soundfile as sf
import pyloudnorm as pyln

def load_audio(file_path, target_sr=48000):
    # Load stereo audio
    y, sr = librosa.load(file_path, sr=target_sr, mono=False)
    if y.ndim == 1:
        y = np.expand_dims(y, axis=0) # Make it 2D (channels, samples)
    return y, sr

def save_audio(file_path, y, sr):
    # soundfile expects (samples, channels)
    if y.shape[0] < y.shape[1] and y.shape[0] <= 2:
        y = y.T
    sf.write(file_path, y, sr, subtype='FLOAT')

def finalize_audio(y, sr, target_lufs=-14.0, max_true_peak=-1.0):
    """
    Format audio loudness and true peak.
    """
    # pyloudnorm requires shape to be (samples, channels)
    is_transposed = False
    if y.shape[0] < y.shape[1] and y.shape[0] <= 2:
        y = y.T
        is_transposed = True
        
    meter = pyln.Meter(sr) 
    loudness = meter.integrated_loudness(y)
    
    # Normalize to target LUFS
    y_norm = pyln.normalize.loudness(y, loudness, target_lufs)
    
    # Need to add True Peak Limiter (Soft Clipper or proper limiter)
    # For now, simplistic peak normalization if true peak exceeds
    current_peak = np.max(np.abs(y_norm))
    target_peak_linear = 10 ** (max_true_peak / 20)
    
    if current_peak > target_peak_linear:
        # Simple gain reduction to hit max true peak
        y_norm = y_norm * (target_peak_linear / current_peak)
        
    if is_transposed:
        y_norm = y_norm.T
        
    return y_norm
