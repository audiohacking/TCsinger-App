"""
Basic tests for TCSinger2 Demo App utilities
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from app import config
        print("✓ app.config imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import app.config: {e}")
        return False
    
    try:
        from utils import audio_utils
        print("✓ utils.audio_utils imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils.audio_utils: {e}")
        return False
    
    try:
        from utils import model_loader
        print("✓ utils.model_loader imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import utils.model_loader: {e}")
        return False
    
    return True


def test_audio_utils():
    """Test audio utility functions"""
    try:
        from utils.audio_utils import parse_notes, note_to_midi, generate_silence
        
        # Test note parsing
        notes = parse_notes("C4 D4 rest E4")
        assert len(notes) == 4, "Should parse 4 notes"
        print("✓ parse_notes works correctly")
        
        # Test MIDI conversion
        midi = note_to_midi("C4")
        assert midi == 60, f"C4 should be MIDI 60, got {midi}"
        print("✓ note_to_midi works correctly")
        
        # Test silence generation
        silence = generate_silence(1.0, sr=48000)
        assert len(silence) == 48000, "Should generate 1 second of silence at 48kHz"
        print("✓ generate_silence works correctly")
        
        return True
    except Exception as e:
        print(f"✗ Audio utils test failed: {e}")
        return False


def test_model_loader():
    """Test model loader"""
    try:
        from utils.model_loader import TCSinger2Model
        
        # Create model instance
        model = TCSinger2Model()
        print(f"✓ TCSinger2Model created, device: {model.device}")
        
        return True
    except Exception as e:
        print(f"✗ Model loader test failed: {e}")
        return False


def test_config():
    """Test configuration"""
    try:
        from app import config
        
        assert hasattr(config, 'SAMPLE_RATE'), "Should have SAMPLE_RATE"
        assert config.SAMPLE_RATE == 48000, "SAMPLE_RATE should be 48000"
        print(f"✓ Config loaded, SAMPLE_RATE: {config.SAMPLE_RATE}")
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False


if __name__ == "__main__":
    print("Running TCSinger2 Demo App Tests")
    print("=" * 50)
    
    all_passed = True
    
    print("\n1. Testing imports...")
    all_passed &= test_imports()
    
    print("\n2. Testing configuration...")
    all_passed &= test_config()
    
    print("\n3. Testing audio utilities...")
    all_passed &= test_audio_utils()
    
    print("\n4. Testing model loader...")
    all_passed &= test_model_loader()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
