from core.analysis import Analyzer
from core.denoising import Denoiser
from core.upscaling import Upscaler
from core.dynamics import DynamicsProcessor
from utils.audio_io import load_audio, save_audio, finalize_audio
import os

class AudioProcessor:
    def __init__(self):
        self.analyzer = Analyzer()
        self.denoiser = Denoiser()
        self.upscaler = Upscaler()
        self.dynamics = DynamicsProcessor()
        
    def process(self, file_path):
        # 1. Load Audio
        y, sr = load_audio(file_path)
        
        # 2. Analyze
        analysis_data = self.analyzer.analyze(y, sr)
        
        # 3. Denoise
        y_denoised = self.denoiser.process(y, sr)
        
        # 4. Upscale (Bandwidth Extension)
        y_upscaled = self.upscaler.process(y_denoised, sr, analysis_data)
        
        # 5. Dynamics (De-essing, Shimmer control)
        y_final = self.dynamics.process(y_upscaled, sr)
        
        # 6. Finalize (LUFS, True Peak)
        y_final = finalize_audio(y_final, sr)
        
        # Save output
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(dir_name, f"{name}_lifter{ext}")
            
        save_audio(output_path, y_final, sr)
        return output_path
