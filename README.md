# 🎵 TCSinger2 Demo App for macOS

A demonstration application for [TCSinger2](https://github.com/AaronZ345/TCSinger2) - Customizable Multilingual Zero-shot Singing Voice Synthesis, optimized for macOS with Apple Metal GPU support.

## Features

✨ **Zero-shot Singing Voice Synthesis**: Synthesize singing voices without training on specific singers
🎤 **Timbre Control**: Use audio prompts to define voice style and timbre
🎵 **Musical Control**: Specify lyrics and musical notes for synthesis
🖥️ **macOS Optimized**: Adapted for Apple Metal Performance Shaders (MPS)
🎨 **User-Friendly UI**: Built with Gradio for easy interaction

## About TCSinger2

TCSinger 2 is a state-of-the-art multilingual zero-shot singing voice synthesis model that supports:
- Style transfer from audio prompts
- Multi-level style control
- Cross-lingual synthesis
- Speech-to-singing conversion

**Paper**: [TCSinger 2: Customizable Multilingual Zero-shot Singing Voice Synthesis](https://arxiv.org/abs/2505.14910) (ACL 2025)

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3) or Intel Mac
- Python 3.10 or higher
- At least 8GB RAM (16GB recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/audiohacking/TCsinger-App.git
cd TCsinger-App
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

For Apple Silicon (M1/M2/M3):
```bash
# Install PyTorch with MPS support
pip install torch torchvision torchaudio

# Install other dependencies
pip install -r requirements.txt
```

For Intel Macs:
```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import torch; print('PyTorch:', torch.__version__); print('MPS Available:', torch.backends.mps.is_available())"
```

## Usage

### Quick Start

Launch the demo application:

```bash
python app/demo.py
```

The application will start and open in your default browser at `http://127.0.0.1:7860`

### Command Line Options

```bash
python app/demo.py --help
```

Available options:
- `--model-path`: Path to pretrained model checkpoint (optional)
- `--share`: Create a public share link for remote access
- `--server-name`: Server host (default: 127.0.0.1)
- `--server-port`: Server port (default: 7860)

Example:
```bash
python app/demo.py --share --server-port 8080
```

## How to Use the Demo

1. **Upload Audio Prompt**: 
   - Upload a short audio clip (3-10 seconds) or record using your microphone
   - This defines the timbre/voice style you want to replicate

2. **Enter Lyrics**: 
   - Type the text you want to be sung
   - Supports multiple languages

3. **Specify Musical Notes**:
   - Use note names: `C4 D4 E4 F4 G4`
   - Or MIDI numbers: `60 62 64 65 67`
   - Or mixed with rests: `C4 rest E4 G4`

4. **Adjust Settings** (Optional):
   - CFG Scale: Controls adherence to prompts (1.0-10.0)
   - Higher values = more faithful to input prompts

5. **Synthesize**: 
   - Click "Synthesize Singing Voice"
   - Wait for processing
   - Download or play the result

## Project Structure

```
TCsinger-App/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   └── demo.py            # Main Gradio application
├── utils/
│   ├── __init__.py
│   ├── audio_utils.py     # Audio processing utilities
│   └── model_loader.py    # Model loading and inference
├── models/                # Model checkpoints directory
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Model Checkpoints

This demo is designed to work with TCSinger2 pretrained models. To use a pretrained model:

1. Download model checkpoints from [TCSinger2 repository](https://github.com/AaronZ345/TCSinger2)
2. Place checkpoints in the `models/` directory
3. Launch with: `python app/demo.py --model-path models/your_checkpoint.pt`

**Note**: Currently, the demo runs with a placeholder model for demonstration. For full functionality, you'll need to:
- Clone and set up the [TCSinger2 repository](https://github.com/AaronZ345/TCSinger2)
- Train or download pretrained models
- Integrate the actual model code

## Apple Metal Support

This application is optimized for Apple Metal GPUs:

- Automatically detects and uses MPS (Metal Performance Shaders) when available
- Falls back to CPU if MPS is not available
- Significantly faster inference on Apple Silicon Macs

To verify Metal support:
```python
import torch
print(torch.backends.mps.is_available())  # Should print True on Apple Silicon
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
# Format code
black app/ utils/

# Check style
flake8 app/ utils/
```

## Future Enhancements

- [ ] Custom model training interface
- [ ] Batch processing support
- [ ] Advanced audio preprocessing options
- [ ] More language support
- [ ] Export in multiple formats
- [ ] Integration with DAWs

## Troubleshooting

### Issue: "MPS backend not available"
- Ensure you're on macOS 12.3 or later with Apple Silicon
- Update to the latest PyTorch version

### Issue: "ModuleNotFoundError"
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate the virtual environment: `source venv/bin/activate`

### Issue: Audio quality is poor
- Try adjusting the CFG scale
- Use a higher quality audio prompt
- Ensure lyrics and notes are properly aligned

## Citation

If you use TCSinger2 in your research, please cite:

```bibtex
@article{zhang2025tcsinger,
  title={TCSinger 2: Customizable Multilingual Zero-shot Singing Voice Synthesis},
  author={Zhang, Yu and Guo, Wenxiang and Pan, Changhao and Yao, Dongyu and Zhu, Zhiyuan and Jiang, Ziyue and Wang, Yuhan and Jin, Tao and Zhao, Zhou},
  journal={arXiv preprint arXiv:2505.14910},
  year={2025}
}
```

## License

This project is for demonstration and research purposes. Please refer to the [TCSinger2 repository](https://github.com/AaronZ345/TCSinger2) for licensing information.

## Disclaimer

⚠️ **Important**: This technology should only be used ethically and legally:
- Do not generate singing voices of public figures without permission
- Respect copyright and intellectual property rights
- Obtain consent before using someone's voice
- Follow all applicable laws and regulations

## Acknowledgements

- [TCSinger2](https://github.com/AaronZ345/TCSinger2) by Zhejiang University
- [Gradio](https://gradio.app/) for the UI framework
- [PyTorch](https://pytorch.org/) for deep learning
- Apple Metal Performance Shaders for GPU acceleration

## Support

For issues related to:
- **This demo app**: Open an issue in this repository
- **TCSinger2 model**: Visit the [official repository](https://github.com/AaronZ345/TCSinger2)

---

Made with ❤️ for the audio synthesis community
