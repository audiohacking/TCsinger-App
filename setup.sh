#!/bin/bash

# TCSinger2 Demo App Setup Script for macOS

echo "🎵 Setting up TCSinger2 Demo App..."
echo ""

# Check if Python 3.10+ is available
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10 or higher is required. Found: $python_version"
    exit 1
fi

echo "✓ Python version: $python_version"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is optimized for macOS"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyTorch with MPS support for Apple Silicon
echo ""
echo "Installing PyTorch..."
if [[ $(uname -m) == 'arm64' ]]; then
    echo "  (Detected Apple Silicon - installing with MPS support)"
    pip install torch torchvision torchaudio
else
    echo "  (Detected Intel Mac - installing standard version)"
    pip install torch torchvision torchaudio
fi

# Install other dependencies
echo ""
echo "Installing other dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p models/cache
mkdir -p tmp

echo "✓ Directories created"

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "
import torch
import gradio as gr
print('✓ PyTorch version:', torch.__version__)
print('✓ Gradio version:', gr.__version__)
if hasattr(torch.backends, 'mps'):
    print('✓ MPS (Metal) available:', torch.backends.mps.is_available())
else:
    print('⚠️  MPS not available (normal for Intel Macs)')
print('✓ CUDA available:', torch.cuda.is_available())
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the demo app:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app/demo.py"
echo ""
echo "For more options: python app/demo.py --help"
