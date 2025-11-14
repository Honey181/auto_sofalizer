# 🎧 Auto Sofalizer

Automated SOFA-based spatial audio processing for video files using FFmpeg.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-Honey181-181717?logo=github)](https://github.com/Honey181/auto_sofalizer)

## 📋 Overview

Auto Sofalizer processes video files by applying SOFA (Spatially Oriented Format for Acoustics) filters to audio tracks, creating immersive spatial audio experiences. The tool automatically:

- Extracts audio tracks from video files
- Applies SOFA spatial audio filters
- Normalizes audio volume (boosts quiet SOFA-processed audio back to optimal levels)
- Muxes the processed audio back into the video
- Sets the processed audio as the default track

## ✨ Features

- **🎯 Batch Processing**: Process entire folders of video files automatically
- **🔊 Auto Normalization**: Boosts quiet SOFA-processed audio to optimal volume levels
- **🎬 Multiple Formats**: Supports MKV, MP4, AVI, and other FFmpeg-compatible formats
- **📊 Progress Tracking**: Visual progress bars and detailed logging
- **🛡️ Error Handling**: Robust error handling and recovery
- **🔧 Configurable**: Flexible command-line options
- **🪟 Cross-Platform**: Works on Windows, macOS, and Linux
- **🧪 Dry Run Mode**: Preview operations before processing
- **📝 Detailed Logging**: Complete operation logs for debugging

## 🚀 Installation

### Prerequisites

1. **Python 3.7+**
   ```bash
   python --version  # Check your Python version
   ```

2. **FFmpeg** (with SOFA support)
   - **Windows**: Download from [FFmpeg.org](https://ffmpeg.org/download.html) or use `winget install FFmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or `sudo dnf install ffmpeg` (Fedora)

### Install Auto Sofalizer

#### Option 1: Install from source (recommended for development)

```bash
git clone https://github.com/Honey181/auto_sofalizer.git
cd auto_sofalizer
pip install -r requirements.txt
```

#### Option 2: Install as a package

```bash
pip install -e .
```

This makes `auto-sofalizer` available as a command anywhere on your system.

## 📖 Usage

### Basic Usage

```bash
python auto_sofalizer.py INPUT_FOLDER OUTPUT_FOLDER EXTENSIONS AUDIO_TRACK
```

**Arguments:**
- `INPUT_FOLDER`: Directory containing video files to process
- `OUTPUT_FOLDER`: Directory where processed files will be saved
- `EXTENSIONS`: File extensions to process (comma-separated)
- `AUDIO_TRACK`: Stream index of audio track to process (usually `1` for first audio track, `2` for second, etc.)

### Examples

#### Process all MKV files
```bash
python auto_sofalizer.py ./input ./output mkv 1
```

#### Process multiple file types
```bash
python auto_sofalizer.py ./videos ./processed mkv,mp4,avi 1
```

#### Use a custom SOFA file
```bash
python auto_sofalizer.py ./input ./output mkv 1 --sofa my_custom.sofa
```

#### Dry run (preview without processing)
```bash
python auto_sofalizer.py ./input ./output mkv 1 --dry-run
```

#### Keep temporary files for debugging
```bash
python auto_sofalizer.py ./input ./output mkv 1 --keep-temp
```

#### Verbose output
```bash
python auto_sofalizer.py ./input ./output mkv 1 --verbose
```

### Advanced Options

```bash
python auto_sofalizer.py --help
```

**Available options:**
- `--sofa FILE`: Specify custom SOFA file (default: irc_1003.sofa)
- `--ffmpeg-verbosity LEVEL`: Set FFmpeg logging level
- `--keep-temp`: Keep temporary files after processing
- `--dry-run`: Show what would be done without processing
- `--verbose`, `-v`: Enable detailed logging
- `--version`: Show version information

## 📂 Project Structure

```
auto_sofalizer/
├── auto_sofalizer.py          # Main script
├── irc_1003.sofa              # Default SOFA file
├── requirements.txt           # Python dependencies
├── setup.py                   # Package installation
├── README.md                  # This file
├── LICENSE                    # MIT License
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── .gitignore                # Git ignore rules
└── examples/                 # Usage examples
    └── example_usage.md
```

## 🎓 How It Works

1. **Extract Audio**: Extracts the specified audio track from the video
2. **Apply SOFA Filter**: Processes audio with spatial SOFA filter (typically reduces volume)
3. **Detect Volume**: Analyzes processed audio for peak volume
4. **Normalize**: Boosts audio back to optimal 0dB peak level
5. **Mux**: Combines processed audio back with original video
6. **Set Default**: Marks the processed audio track as default

## 🔧 SOFA Files

The default SOFA file (`irc_1003.sofa`) is included. You can use custom SOFA files:

- Download SOFA files from [SOFA Conventions](https://www.sofaconventions.org/)
- Use custom head-related transfer functions (HRTFs)
- Specify with `--sofa your_file.sofa`

## 🐛 Troubleshooting

### FFmpeg not found
```
Error: FFmpeg is not installed or not in PATH
```
**Solution**: Install FFmpeg and ensure it's in your system PATH.

### SOFA file not found
```
Error: SOFA file does not exist
```
**Solution**: Ensure `irc_1003.sofa` is in the script directory or specify path with `--sofa`.

### Audio track not found
```
Error: Audio track X not found
```
**Solution**: Use `ffprobe` to check available audio streams:
```bash
ffprobe your_video.mkv 2>&1 | findstr "Stream"
```

Look for the audio streams. Example:
```
Stream #0:0: Video       ← Stream 0 (don't use this!)
Stream #0:1: Audio       ← Stream 1 (first audio - use 1)
Stream #0:2: Audio       ← Stream 2 (second audio - use 2)
Stream #0:3: Subtitle    ← Stream 3 (don't use this!)
```

**Important**: Count ALL streams (video + audio + subtitles), not just audio tracks!

### Permission errors
**Solution**: Ensure you have write permissions for the output folder.

## 📊 Performance

Processing time depends on:
- Video file size and resolution
- Audio track complexity
- CPU performance
- Storage speed (SSD vs HDD)

**Typical rates**: 
- 1080p video: ~0.5-2x realtime
- 4K video: ~0.2-1x realtime

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[ThreeDeeJay (3DJ)](https://github.com/ThreeDeeJay)** - For the incredible [Binaural Audio resources](https://kutt.it/binaural) that inspired this project and taught me about HRTF and spatial audio. Join the [Discord community](https://kutt.it/BinauralDiscord) for discussions on binaural audio!
- **FFmpeg team** - For the excellent multimedia framework and SOFA filter support
- **SOFA Conventions community** - For spatial audio standards
- **Contributors and users** - For feedback and testing

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/Honey181/auto_sofalizer/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/Honey181/auto_sofalizer/issues)

## 🗺️ Roadmap

- [ ] Parallel processing support for multiple files
- [ ] GUI interface
- [ ] Preset SOFA file configurations
- [ ] Integration with popular video editors
- [ ] Docker container support
- [ ] Web interface

## 📈 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Made with ❤️ for spatial audio enthusiasts**

