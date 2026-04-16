import numpy as np
import librosa

class Denoiser:
    def __init__(self, passes=2, threshold_multiplier=1.5):
        self.passes = passes
        self.threshold_multiplier = threshold_multiplier
        
    def _spectral_gate(self, y, sr):
        # 1. Compute STFT
        S = librosa.stft(y, n_fft=2048, hop_length=512)
        S_mag, S_phase = librosa.magphase(S)
        
        # 2. Estimate Noise Profile
        # Estimate from the quietest frames (e.g., lower 5th percentile)
        noise_profile = np.percentile(S_mag, 5, axis=1, keepdims=True)
        
        # 3. Soft Masking (Spectral Subtraction)
        threshold = noise_profile * self.threshold_multiplier
        # Use a soft knee to prevent excessive musical noise
        mask = np.clip((S_mag - threshold) / (S_mag + 1e-10), 0.1, 1.0)
        
        # 4. Reconstruct
        S_clean = S_mag * mask * S_phase
        y_clean = librosa.istft(S_clean, hop_length=512)
        
        # Match lengths in case istft pads/truncates slightly
        if len(y_clean) > len(y):
            y_clean = y_clean[:len(y)]
        elif len(y_clean) < len(y):
            y_clean = np.pad(y_clean, (0, len(y) - len(y_clean)))
            
        return y_clean
        
    def process(self, y, sr):
        """
        Apply adaptive noise reduction and multi-pass processing.
        y shape expected: (channels, samples) or (samples,)
        """
        y_denoised = y.copy()
        
        if y_denoised.ndim > 1:
            for ch in range(y_denoised.shape[0]):
                y_ch = y_denoised[ch]
                for p in range(self.passes):
                    y_ch = self._spectral_gate(y_ch, sr)
                y_denoised[ch] = y_ch
        else:
            for p in range(self.passes):
                y_denoised = self._spectral_gate(y_denoised, sr)
                
        return y_denoised
