# Contributing to Auto Sofalizer

First off, thank you for considering contributing to Auto Sofalizer! It's people like you that make this tool better for everyone.

## 🎯 Code of Conduct

This project and everyone participating in it is governed by common sense and mutual respect. Be kind, be professional, and be constructive.

## 🚀 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When you create a bug report, please include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected behavior**
- **Actual behavior**
- **System information** (OS, Python version, FFmpeg version)
- **Log files** if applicable
- **Sample files** if possible (or describe file characteristics)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Detailed explanation** of the proposed feature
- **Why this enhancement would be useful** to most users
- **Possible implementation approach** (if you have ideas)

### Pull Requests

1. **Fork the repository** at [https://github.com/Honey181/auto_sofalizer](https://github.com/Honey181/auto_sofalizer) and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Write good commit messages**
6. **Submit the pull request**

## 💻 Development Setup

### Prerequisites

- Python 3.7+
- FFmpeg (with SOFA support)
- Git

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/auto_sofalizer.git
cd auto_sofalizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=auto_sofalizer

# Run specific test
pytest tests/test_specific.py
```

### Code Formatting

We use Black for code formatting:

```bash
# Format all Python files
black .

# Check without modifying
black --check .
```

### Linting

```bash
# Run flake8
flake8 auto_sofalizer.py

# Run mypy for type checking
mypy auto_sofalizer.py
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) formatter (line length: 100)
- Use type hints for function signatures
- Write docstrings for all public functions and classes

### Example Function

```python
def process_audio(input_file: Path, output_file: Path, config: ProcessingConfig) -> bool:
    """
    Process an audio file with SOFA filter
    
    Args:
        input_file: Path to input audio file
        output_file: Path where output will be saved
        config: Processing configuration
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        FFmpegCommandError: If FFmpeg command fails
        ValueError: If input file doesn't exist
    """
    # Implementation here
    pass
```

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: add parallel processing support
fix: resolve Windows path handling issue
docs: update README with new examples
refactor: extract audio processing into separate class
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new features
- Ensure existing tests pass
- Aim for good coverage of critical paths
- Use descriptive test names

### Test Structure

```python
def test_feature_name_should_do_something():
    """Test that feature correctly handles specific case"""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

## 📚 Documentation

### Code Documentation

- Write clear docstrings for modules, classes, and functions
- Include type hints
- Document exceptions that can be raised
- Provide usage examples for complex functions

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Installation instructions (if needed)
- Troubleshooting section (if applicable)

## 🔄 Pull Request Process

1. **Update the CHANGELOG.md** with details of changes
2. **Update the README.md** if functionality changes
3. **Ensure all tests pass** and code is formatted
4. **Update version numbers** following [Semantic Versioning](https://semver.org/)
5. **Request review** from maintainers

### PR Title Format

Use the same format as commit messages:
```
feat: add support for custom SOFA file selection
fix: handle missing audio track gracefully
```

### PR Description Template

```markdown
## Description
Brief description of the changes

## Motivation
Why is this change needed?

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] CHANGELOG.md updated
```

## 🎓 Learning Resources

### FFmpeg and SOFA
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [SOFA Conventions](https://www.sofaconventions.org/)
- [Spatial Audio Guide](https://en.wikipedia.org/wiki/Spatial_audio)

### Python Best Practices
- [Python PEP 8](https://pep8.org/)
- [Real Python Tutorials](https://realpython.com/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)

## 💬 Questions?

- Open an issue with the `question` label at [https://github.com/Honey181/auto_sofalizer/issues](https://github.com/Honey181/auto_sofalizer/issues)
- Join discussions in existing issues
- Check existing documentation first

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Git commit history

Thank you for contributing to Auto Sofalizer! 🎧

