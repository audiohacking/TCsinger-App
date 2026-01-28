# Contributing to TCSinger2 Demo App

Thank you for your interest in contributing to the TCSinger2 Demo App! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/TCsinger-App.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/audiohacking/TCsinger-App.git
cd TCsinger-App

# Run setup
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Add comments for complex logic

### Formatting

We use `black` for code formatting:

```bash
pip install black
black app/ utils/
```

### Linting

We use `flake8` for linting:

```bash
pip install flake8
flake8 app/ utils/ --max-line-length=100
```

## Project Structure

```
TCsinger-App/
├── app/               # Main application code
│   ├── config.py     # Configuration
│   └── demo.py       # Gradio UI
├── utils/            # Utility functions
│   ├── model_loader.py
│   └── audio_utils.py
├── models/           # Model checkpoints
├── examples/         # Example files
└── tests/           # Test files
```

## Adding Features

### New Audio Processing Features

1. Add function to `utils/audio_utils.py`
2. Add tests for the function
3. Update documentation

### New UI Components

1. Modify `app/demo.py`
2. Update `app/config.py` if needed
3. Test the UI thoroughly
4. Take screenshots of changes

### Model Integration

1. Update `utils/model_loader.py`
2. Ensure compatibility with Apple Metal
3. Test on different hardware if possible
4. Document new model requirements

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_audio_utils.py

# Run with coverage
python -m pytest --cov=app --cov=utils tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names
- Test edge cases and error conditions

Example:
```python
def test_load_audio_valid_file():
    """Test loading a valid audio file"""
    audio, sr = load_audio("path/to/audio.wav")
    assert audio is not None
    assert sr == 48000
```

## Documentation

- Update README.md for major changes
- Add docstrings to new functions
- Update example files if needed
- Include code comments for complex logic

## Commit Messages

Use clear and descriptive commit messages:

```
Add: New feature description
Fix: Bug description
Update: What was updated
Refactor: What was refactored
Docs: Documentation changes
Test: Test additions or changes
```

Examples:
- `Add: Support for additional audio formats`
- `Fix: Audio normalization causing clipping`
- `Update: Gradio UI layout for better UX`
- `Docs: Add installation instructions for M1 Macs`

## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md if applicable
5. Submit PR with clear description of changes

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How were these changes tested?

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
```

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

- Open an issue for questions about contributing
- Join discussions in existing issues
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Acknowledgments

Thank you to all contributors who help improve this project!
