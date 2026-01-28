"""
TCSinger2 Demo Application with Gradio UI

This application provides a user-friendly interface for demonstrating
TCSinger2's zero-shot singing voice synthesis capabilities.
"""

import gradio as gr
import numpy as np
import torch
import os
import tempfile
from pathlib import Path

# Import utilities
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.model_loader import load_pretrained_model, TCSinger2Model
from utils.audio_utils import (
    load_audio,
    save_audio,
    audio_to_tensor,
    tensor_to_audio,
    normalize_audio,
    parse_notes,
    generate_silence
)
from app.config import (
    SAMPLE_RATE,
    MAX_AUDIO_LENGTH,
    DEFAULT_CFG_SCALE,
    EXAMPLE_LYRICS,
    EXAMPLE_NOTES
)


class TCSinger2DemoApp:
    """Main application class for TCSinger2 demo"""
    
    def __init__(self, model_path: str = None):
        """
        Initialize the demo application
        
        Args:
            model_path: Path to pretrained model checkpoint
        """
        print("🎵 Initializing TCSinger2 Demo App...")
        self.model = load_pretrained_model(checkpoint_path=model_path)
        self.temp_dir = tempfile.mkdtemp()
        print(f"✓ Temporary directory: {self.temp_dir}")
        print("✓ Initialization complete!")
        
    def synthesize_singing(
        self,
        audio_prompt,
        lyrics: str,
        notes: str,
        cfg_scale: float,
        progress=gr.Progress()
    ):
        """
        Main synthesis function called by Gradio UI
        
        Args:
            audio_prompt: Audio file for timbre reference
            lyrics: Text lyrics
            notes: Musical notes
            cfg_scale: Classifier-free guidance scale
            progress: Gradio progress bar
            
        Returns:
            Tuple of (output_audio_path, status_message)
        """
        try:
            progress(0.1, desc="Loading audio prompt...")
            
            # Validate inputs
            if audio_prompt is None:
                return None, "❌ Please upload an audio prompt file"
            
            if not lyrics.strip():
                return None, "❌ Please enter lyrics text"
            
            if not notes.strip():
                return None, "❌ Please enter musical notes"
            
            # Load and process audio prompt
            progress(0.2, desc="Processing audio prompt...")
            prompt_audio, sr = load_audio(audio_prompt, target_sr=SAMPLE_RATE)
            prompt_tensor = audio_to_tensor(prompt_audio, device=self.model.device)
            
            # Parse notes
            progress(0.3, desc="Parsing musical notes...")
            parsed_notes = parse_notes(notes)
            
            # Synthesize
            progress(0.5, desc="Synthesizing singing voice...")
            output_tensor = self.model.synthesize(
                audio_prompt=prompt_tensor,
                text=lyrics,
                notes=notes,
                cfg_scale=cfg_scale
            )
            
            # Convert to numpy and normalize
            progress(0.8, desc="Post-processing audio...")
            output_audio = tensor_to_audio(output_tensor)
            output_audio = normalize_audio(output_audio)
            
            # Save output
            progress(0.9, desc="Saving output...")
            output_path = os.path.join(self.temp_dir, "synthesized_output.wav")
            save_audio(output_audio, output_path, sr=SAMPLE_RATE)
            
            progress(1.0, desc="Complete!")
            
            status = f"""
            ✅ Synthesis Complete!
            
            📊 Details:
            - Lyrics: "{lyrics}"
            - Notes: {notes}
            - CFG Scale: {cfg_scale}
            - Device: {self.model.device}
            - Output Length: {len(output_audio) / SAMPLE_RATE:.2f}s
            """
            
            return output_path, status
            
        except Exception as e:
            error_msg = f"❌ Error during synthesis: {str(e)}"
            print(error_msg)
            return None, error_msg
    
    def create_ui(self):
        """Create and configure the Gradio UI"""
        
        with gr.Blocks(
            title="TCSinger2 Demo",
            theme=gr.themes.Soft()
        ) as demo:
            
            gr.Markdown("""
            # 🎵 TCSinger2 Demo App
            
            **Customizable Multilingual Zero-shot Singing Voice Synthesis**
            
            This demo showcases TCSinger2's ability to synthesize singing voices with:
            - **Audio Prompt**: Upload an audio file to define the timbre/voice style
            - **Lyrics**: Enter the text you want to be sung
            - **Musical Notes**: Specify the melody using note names (C4, D4, etc.) or MIDI numbers
            
            ---
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📤 Inputs")
                    
                    # Audio prompt upload
                    audio_prompt = gr.Audio(
                        label="Audio Prompt (for timbre)",
                        type="filepath",
                        sources=["upload", "microphone"]
                    )
                    
                    gr.Markdown("""
                    *Upload or record a short audio clip (3-10 seconds) of the voice 
                    style you want to replicate.*
                    """)
                    
                    # Lyrics input
                    lyrics = gr.Textbox(
                        label="Lyrics",
                        placeholder="Enter the lyrics you want to synthesize...",
                        lines=3,
                        value=EXAMPLE_LYRICS[0]
                    )
                    
                    # Notes input
                    notes = gr.Textbox(
                        label="Musical Notes",
                        placeholder="e.g., C4 D4 E4 F4 G4 or 60 62 64 65 67",
                        lines=2,
                        value=EXAMPLE_NOTES[0]
                    )
                    
                    gr.Markdown("""
                    *Supported formats:*
                    - Note names: `C4 D4 E4 F4`
                    - MIDI numbers: `60 62 64 65`
                    - Mixed with rests: `C4 rest E4 G4`
                    """)
                    
                    # Advanced settings
                    with gr.Accordion("⚙️ Advanced Settings", open=False):
                        cfg_scale = gr.Slider(
                            minimum=1.0,
                            maximum=10.0,
                            value=DEFAULT_CFG_SCALE,
                            step=0.5,
                            label="CFG Scale",
                            info="Higher values = more adherence to prompts"
                        )
                    
                    # Synthesize button
                    synthesize_btn = gr.Button(
                        "🎤 Synthesize Singing Voice",
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📥 Output")
                    
                    # Output audio
                    output_audio = gr.Audio(
                        label="Synthesized Singing Voice",
                        type="filepath"
                    )
                    
                    # Status message
                    status_msg = gr.Textbox(
                        label="Status",
                        lines=8,
                        interactive=False
                    )
            
            # Examples section
            gr.Markdown("---")
            gr.Markdown("### 📝 Example Prompts")
            
            with gr.Row():
                example_btns = []
                for i, (lyric, note) in enumerate(zip(EXAMPLE_LYRICS, EXAMPLE_NOTES)):
                    with gr.Column():
                        btn = gr.Button(f"Example {i+1}")
                        example_btns.append((btn, lyric, note))
            
            # Set up event handlers
            synthesize_btn.click(
                fn=self.synthesize_singing,
                inputs=[audio_prompt, lyrics, notes, cfg_scale],
                outputs=[output_audio, status_msg]
            )
            
            # Example button handlers
            for btn, lyric, note in example_btns:
                btn.click(
                    fn=lambda l=lyric, n=note: (l, n),
                    inputs=[],
                    outputs=[lyrics, notes]
                )
            
            # Footer
            gr.Markdown("""
            ---
            
            **About TCSinger2**
            
            TCSinger 2 is a state-of-the-art multilingual zero-shot singing voice synthesis model 
            developed by researchers at Zhejiang University. It supports style transfer, 
            multi-level style control, and cross-lingual synthesis.
            
            - 📄 [Paper](https://arxiv.org/abs/2505.14910) (ACL 2025)
            - 💻 [GitHub](https://github.com/AaronZ345/TCSinger2)
            - 🎧 [Demo Page](https://aaronz345.github.io/TCSinger2Demo/)
            
            **Note**: This is a demo application adapted for macOS with Apple Metal support.
            For production use, please refer to the official repository.
            
            ⚠️ **Disclaimer**: Please only use this technology with consent. 
            Do not generate singing voices of public figures without permission.
            """)
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the Gradio application"""
        demo = self.create_ui()
        demo.launch(**kwargs)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="TCSinger2 Demo App")
    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Path to pretrained model checkpoint"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Create a public share link"
    )
    parser.add_argument(
        "--server-name",
        type=str,
        default="127.0.0.1",
        help="Server host"
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=7860,
        help="Server port"
    )
    
    args = parser.parse_args()
    
    # Create and launch app
    app = TCSinger2DemoApp(model_path=args.model_path)
    app.launch(
        share=args.share,
        server_name=args.server_name,
        server_port=args.server_port
    )


if __name__ == "__main__":
    main()
