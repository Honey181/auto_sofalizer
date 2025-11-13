# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-13

### Added
- Complete code refactor with modern Python practices
- Type hints throughout the codebase
- Comprehensive error handling and validation
- Cross-platform compatibility (Windows, macOS, Linux)
- Progress bars with tqdm integration
- Detailed logging system with file output
- Dry-run mode for previewing operations
- Command-line argument validation
- Better user feedback and status messages
- Setup.py for proper package installation
- Comprehensive README with examples
- Contributing guidelines
- This CHANGELOG file
- MIT License
- Proper .gitignore file
- Class-based architecture for better maintainability
- Configuration dataclass for settings management
- FFmpeg availability checking
- Skip already processed files
- Processing statistics and summary
- Verbose logging option
- Version flag (--version)

### Changed
- Replaced `/dev/null` with `os.devnull` for Windows compatibility
- Improved command-line argument parsing with argparse
- Better temporary file management
- Enhanced logging output format
- More descriptive variable and function names
- Separated concerns into classes (AudioProcessor, ProcessingConfig)
- Improved error messages
- Better handling of FFmpeg output

### Fixed
- Critical bug: Windows compatibility issue with /dev/null
- Indentation error on line 92 (mixed spaces/tabs)
- Missing error handling for failed FFmpeg commands
- No validation of input paths
- No check for FFmpeg availability
- Missing SOFA file not handled gracefully
- Hard-coded values throughout the code
- Poor error messages

### Improved
- Code structure and organization
- Documentation and comments
- User experience with better feedback
- Performance with better temp file cleanup
- Maintainability with type hints and classes

## [1.0.0] - Original Release

### Initial Release
- Basic functionality for applying SOFA filters to videos
- Audio track extraction
- Volume detection and normalization
- Audio muxing back to video
- Default audio track management
- Simple command-line interface
- Temporary file handling
- Log file generation

### Known Issues
- Windows compatibility problems (/dev/null)
- Limited error handling
- No input validation
- Mixed indentation (tabs/spaces)
- Hard-coded values
- Basic user feedback
- No proper package structure

---

## Version History

- **2.0.0**: Major refactor with modern practices and fixes
- **1.0.0**: Initial release with basic functionality

