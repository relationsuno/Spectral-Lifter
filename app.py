import gradio as gr
from processor import AudioProcessor

def process_audio(input_file):
    if input_file is None:
        return None, "Please upload an audio file."
    
    processor = AudioProcessor()
    output_file = processor.process(input_file)
    
    return output_file, "Processing complete!"

with gr.Blocks(title='Antigravity - Spectral Lifter') as demo:
    gr.Markdown("# Antigravity - Spectral Lifter (v1.0)")
    gr.Markdown("Resolve high-frequency cutoff and AI shimmer in Suno AI generated audio.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(type="filepath", label="Input Audio (Suno AI)")
            process_btn = gr.Button("Process Audio")
        with gr.Column():
            audio_output = gr.Audio(type="filepath", label="Processed Audio (Spectral Lifter)")
            status_text = gr.Textbox(label="Status", interactive=False)
            
    process_btn.click(fn=process_audio, inputs=audio_input, outputs=[audio_output, status_text])

if __name__ == "__main__":
    # `share=True` is required to generate a public link when running on Google Colab or external servers.
    demo.launch(share=True)
