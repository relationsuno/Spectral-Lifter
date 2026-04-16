import numpy as np
import librosa

class DynamicsProcessor:
    def __init__(self):
        self.bands = {
            "sibilance": (5000, 8000),
            "shimmer": (10000, 14000),
            "artifacts_hf": (18000, 24000)
        }
        self.reduction_db = {
            "sibilance": 3.0,
            "shimmer": 6.0,
            "artifacts_hf": 12.0
        }
        
    def _apply_multiband_compression(self, y, sr):
        S = librosa.stft(y, n_fft=2048, hop_length=512)
        S_mag, S_phase = librosa.magphase(S)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
        
        idx_s_start = np.searchsorted(freqs, self.bands["sibilance"][0])
        idx_s_end = np.searchsorted(freqs, self.bands["sibilance"][1])
        
        idx_sh_start = np.searchsorted(freqs, self.bands["shimmer"][0])
        idx_sh_end = np.searchsorted(freqs, self.bands["shimmer"][1])
        
        idx_a_start = np.searchsorted(freqs, self.bands["artifacts_hf"][0])
        idx_a_end = np.searchsorted(freqs, self.bands["artifacts_hf"][1])
        
        def apply_reduction(start, end, reduction_db, threshold_percentile=70):
            if start >= len(freqs): return
            end = min(end, len(freqs))
            band_energy = np.mean(S_mag[start:end, :], axis=0) # Average magnitude in band per frame
            thresh = np.percentile(band_energy, threshold_percentile)
            
            reduction_linear = 10 ** (-reduction_db / 20)
            mask = np.ones_like(band_energy)
            
            excess = band_energy > thresh
            if np.any(excess):
                mask[excess] = reduction_linear + (1 - reduction_linear) * (thresh / (band_energy[excess] + 1e-10))
            
            mask = np.convolve(mask, np.ones(5)/5, mode='same')
            mask = np.clip(mask, reduction_linear, 1.0)
            S_mag[start:end, :] *= mask[np.newaxis, :]
            
        apply_reduction(idx_s_start, idx_s_end, self.reduction_db["sibilance"], 80)
        apply_reduction(idx_sh_start, idx_sh_end, self.reduction_db["shimmer"], 60)
        apply_reduction(idx_a_start, idx_a_end, self.reduction_db["artifacts_hf"], 50)
        
        S_new = S_mag * S_phase
        y_proc = librosa.istft(S_new, hop_length=512)
        
        if len(y_proc) > len(y):
            y_proc = y_proc[:len(y)]
        elif len(y_proc) < len(y):
            y_proc = np.pad(y_proc, (0, len(y) - len(y_proc)))
        return y_proc

    def process(self, y, sr):
        """
        Multi-band de-essing for 5-8kHz, 10-14kHz, and 18kHz+.
        """
        if y.ndim > 1:
            y_out = y.copy()
            for ch in range(y_out.shape[0]):
                y_out[ch] = self._apply_multiband_compression(y_out[ch], sr)
            return y_out
        else:
            return self._apply_multiband_compression(y, sr)
