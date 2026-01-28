"""
Audio processing utilities
"""

import numpy as np
import torch
import librosa
import soundfile as sf
from typing import Tuple, Optional


def load_audio(
    audio_path: str,
    target_sr: int = 48000,
    mono: bool = True
) -> Tuple[np.ndarray, int]:
    """
    Load audio file and resample if necessary
    
    Args:
        audio_path: Path to audio file
        target_sr: Target sample rate
        mono: Convert to mono if True
        
    Returns:
        Tuple of (audio array, sample rate)
    """
    try:
        audio, sr = librosa.load(audio_path, sr=target_sr, mono=mono)
        return audio, sr
    except Exception as e:
        raise ValueError(f"Failed to load audio: {e}")


def save_audio(
    audio: np.ndarray,
    output_path: str,
    sr: int = 48000
) -> str:
    """
    Save audio array to file
    
    Args:
        audio: Audio array
        output_path: Output file path
        sr: Sample rate
        
    Returns:
        Output file path
    """
    try:
        sf.write(output_path, audio, sr)
        return output_path
    except Exception as e:
        raise ValueError(f"Failed to save audio: {e}")


def audio_to_tensor(
    audio: np.ndarray,
    device: str = "cpu"
) -> torch.Tensor:
    """
    Convert numpy audio array to PyTorch tensor
    
    Args:
        audio: Audio array
        device: Target device
        
    Returns:
        Audio tensor
    """
    tensor = torch.from_numpy(audio).float()
    if device != "cpu":
        tensor = tensor.to(device)
    return tensor


def tensor_to_audio(
    tensor: torch.Tensor
) -> np.ndarray:
    """
    Convert PyTorch tensor to numpy audio array
    
    Args:
        tensor: Audio tensor
        
    Returns:
        Audio array
    """
    if tensor.is_cuda or str(tensor.device).startswith('mps'):
        tensor = tensor.cpu()
    return tensor.numpy()


def normalize_audio(
    audio: np.ndarray,
    target_level: float = -20.0
) -> np.ndarray:
    """
    Normalize audio to target dB level
    
    Args:
        audio: Audio array
        target_level: Target dB level
        
    Returns:
        Normalized audio array
    """
    # Calculate current RMS level
    rms = np.sqrt(np.mean(audio**2))
    if rms > 0:
        current_db = 20 * np.log10(rms)
        gain_db = target_level - current_db
        gain_linear = 10 ** (gain_db / 20)
        audio = audio * gain_linear
    
    # Clip to prevent overflow
    audio = np.clip(audio, -1.0, 1.0)
    
    return audio


def parse_notes(notes_str: str) -> list:
    """
    Parse note string into a list of notes
    
    Supports formats:
    - Note names: "C4 D4 E4 F4"
    - MIDI numbers: "60 62 64 65"
    - Mixed: "C4 rest 64 E4"
    
    Args:
        notes_str: Note string
        
    Returns:
        List of parsed notes
    """
    notes = notes_str.strip().split()
    parsed = []
    
    for note in notes:
        if note.lower() == 'rest':
            parsed.append({'type': 'rest'})
        elif note.isdigit():
            # MIDI number
            parsed.append({'type': 'midi', 'value': int(note)})
        else:
            # Note name (e.g., C4, D#5)
            parsed.append({'type': 'name', 'value': note})
    
    return parsed


def note_to_midi(note_name: str) -> int:
    """
    Convert note name to MIDI number
    
    Args:
        note_name: Note name (e.g., "C4", "D#5", "Bb3")
        
    Returns:
        MIDI number
    """
    note_map = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
        'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }
    
    # Parse note name and octave
    if len(note_name) < 2:
        raise ValueError(f"Invalid note name: {note_name}")
    
    # Extract octave (last character)
    try:
        octave = int(note_name[-1])
    except ValueError:
        raise ValueError(f"Invalid octave in note name: {note_name}")
    
    # Extract note (everything before octave)
    note = note_name[:-1]
    
    # Validate note
    if note not in note_map:
        raise ValueError(f"Invalid note: {note}")
    
    # Calculate MIDI number (C4 = middle C = 60)
    # Formula: note_value + (octave * 12) + 12
    midi = note_map[note] + (octave + 1) * 12
    
    return midi



def generate_silence(duration: float, sr: int = 48000) -> np.ndarray:
    """
    Generate silence
    
    Args:
        duration: Duration in seconds
        sr: Sample rate
        
    Returns:
        Silent audio array
    """
    return np.zeros(int(duration * sr))
