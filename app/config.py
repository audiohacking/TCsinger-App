"""
Configuration settings for TCSinger2 Demo App
"""

import os

# Model settings
MODEL_NAME = "tcsinger2"
SAMPLE_RATE = 48000  # TCSinger2 uses 48kHz
HOP_LENGTH = 512
WIN_LENGTH = 2048

# Default paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
CACHE_DIR = os.path.join(MODEL_DIR, "cache")

# UI Settings
MAX_AUDIO_LENGTH = 30  # seconds
DEFAULT_CFG_SCALE = 3.5  # Classifier-free guidance scale

# Apple Metal settings
USE_MPS = True  # Use Metal Performance Shaders if available
DEVICE = "mps" if USE_MPS else "cpu"

# Example prompts
EXAMPLE_LYRICS = [
    "Hello world, this is a singing voice synthesis demo",
    "I love music and technology combined together",
    "The future of AI is bright and amazing"
]

EXAMPLE_NOTES = [
    "C4 D4 E4 F4 G4 A4 B4 C5",
    "60 62 64 65 67 69 71 72",  # MIDI note numbers
    "rest C4 E4 G4 rest"
]
