import numpy as np
import librosa
from scipy.signal import find_peaks

class Analyzer:
    def __init__(self, cutoff_range=(12000, 16000), harmonic_range=(300, 800)):
        self.cutoff_range = cutoff_range
        self.harmonic_range = harmonic_range
        
    def analyze(self, y, sr):
        """
        Analyze the audio to find cutoff boundary and harmonics.
        Returns useful data for the upscaler.
        """
        if y.ndim > 1:
            y_mono = librosa.to_mono(y if y.shape[0] > y.shape[1] else y.T)
        else:
            y_mono = y

        # 1. Detect Cutoff Boundary (12kHz - 16kHz)
        S = np.abs(librosa.stft(y_mono))
        freqs = librosa.fft_frequencies(sr=sr)
        mean_spectrum = np.mean(S, axis=1)
        mean_spectrum_db = librosa.amplitude_to_db(mean_spectrum, ref=np.max)
        
        cutoff_idx_start = np.searchsorted(freqs, self.cutoff_range[0])
        cutoff_idx_end = np.searchsorted(freqs, self.cutoff_range[1])
        
        if cutoff_idx_start < len(freqs) and cutoff_idx_end <= len(freqs):
            db_diff = np.diff(mean_spectrum_db[cutoff_idx_start:cutoff_idx_end])
            if len(db_diff) > 0:
                steepest_drop_idx = np.argmin(db_diff)
                cutoff_freq = freqs[cutoff_idx_start + steepest_drop_idx]
            else:
                cutoff_freq = 16000.0
        else:
            cutoff_freq = 16000.0

        # 2. Isolate Artifacts (Preparation)
        # Separate harmonic and percussive to later observe shimmer in non-harmonic HF
        y_harmonic, _ = librosa.effects.hpss(y_mono, margin=1.2)
        
        # 3. Harmonic Structure Analysis (300Hz - 800Hz)
        h_S = np.abs(librosa.stft(y_harmonic))
        h_mean_spectrum = np.mean(h_S, axis=1)
        
        harm_idx_start = np.searchsorted(freqs, self.harmonic_range[0])
        harm_idx_end = np.searchsorted(freqs, self.harmonic_range[1])
        
        target_band_spectrum = h_mean_spectrum[harm_idx_start:harm_idx_end]
        target_band_freqs = freqs[harm_idx_start:harm_idx_end]
        
        peaks, _ = find_peaks(target_band_spectrum, prominence=0.1)
        dominant_harmonics = [
            {"freq": float(target_band_freqs[p]), "magnitude": float(target_band_spectrum[p])} 
            for p in peaks
        ]
        
        # Sort by magnitude descending
        dominant_harmonics = sorted(dominant_harmonics, key=lambda d: d['magnitude'], reverse=True)
        
        return {
            "cutoff_frequency": float(cutoff_freq),
            "dominant_harmonics": dominant_harmonics,
            "has_shimmer": True
        }
