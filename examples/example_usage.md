# Auto Sofalizer - Usage Examples

This document provides detailed examples and use cases for Auto Sofalizer.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Examples](#advanced-examples)
3. [Common Workflows](#common-workflows)
4. [Troubleshooting Examples](#troubleshooting-examples)
5. [Integration Examples](#integration-examples)

## Basic Usage

### Example 1: Process Single Format

Process all MKV files in a folder:

```bash
python auto_sofalizer.py ./my_videos ./output mkv 1
```

**What happens:**
- Looks for `*.mkv` files in `./my_videos`
- Processes audio track 1 (second track, 0-indexed)
- Saves results to `./output` with "(sofa)" suffix
- Applies default `irc_1003.sofa` filter

### Example 2: Multiple File Formats

Process MKV, MP4, and AVI files:

```bash
python auto_sofalizer.py ./videos ./processed mkv,mp4,avi 1
```

### Example 3: Different Audio Track

Process using the first audio track (index 0):

```bash
python auto_sofalizer.py ./videos ./output mkv 0
```

## Advanced Examples

### Example 4: Custom SOFA File

Use a custom SOFA file for specific spatial characteristics:

```bash
python auto_sofalizer.py ./input ./output mkv 1 --sofa ./my_sofa_files/custom_hrtf.sofa
```

**Use case:** You have a SOFA file optimized for your headphones or listening setup.

### Example 5: Dry Run Before Processing

Preview what will be done without actually processing:

```bash
python auto_sofalizer.py ./videos ./output mkv 1 --dry-run
```

**Output:**
```
Auto Sofalizer v2.0.0
Input folder: C:\Users\julia\videos
Output folder: C:\Users\julia\output
Extensions: mkv
Audio track: 1
SOFA file: C:\Users\julia\auto_sofalizer\irc_1003.sofa

*** DRY RUN MODE - No files will be modified ***

Found 5 file(s) to process
[DRY RUN] Would execute: ffmpeg -v repeat+24 -i ...
...
```

### Example 6: Verbose Logging

Enable detailed logging for debugging:

```bash
python auto_sofalizer.py ./videos ./output mkv 1 --verbose
```

### Example 7: Keep Temporary Files

Keep intermediate files for inspection or debugging:

```bash
python auto_sofalizer.py ./videos ./output mkv 1 --keep-temp
```

**Temporary files location:** `./output/temp/`

Contains:
- `*.mkv` - Extracted audio
- `*_sofa.flac` - Audio with SOFA filter applied
- `*_gain.flac` - Normalized audio
- `*_almost_done.*` - Intermediate muxed file
- `*_unmarked.*` - File with audio tracks unmarked
- `processing.log` - Detailed log

### Example 8: Custom FFmpeg Verbosity

Adjust FFmpeg output detail level:

```bash
# Quiet mode (minimal output)
python auto_sofalizer.py ./videos ./output mkv 1 --ffmpeg-verbosity quiet

# Debug mode (maximum output)
python auto_sofalizer.py ./videos ./output mkv 1 --ffmpeg-verbosity debug
```

## Common Workflows

### Workflow 1: Movie Collection Processing

You have a collection of movies with 5.1 surround sound and want binaural audio:

```bash
# Step 1: Check what audio tracks are available
ffprobe movie.mkv

# Step 2: Dry run to verify
python auto_sofalizer.py ./movies ./movies_binaural mkv 1 --dry-run

# Step 3: Process with verbose output
python auto_sofalizer.py ./movies ./movies_binaural mkv 1 --verbose

# Step 4: Check results
ls ./movies_binaural/
```

### Workflow 2: Batch Processing with Custom SOFA

Process multiple folders with different SOFA files:

```bash
# Action movies with dynamic SOFA
python auto_sofalizer.py ./action ./processed/action mkv,mp4 1 --sofa dynamic.sofa

# Music videos with studio SOFA
python auto_sofalizer.py ./music ./processed/music mkv,mp4 1 --sofa studio.sofa

# Documentaries with clear speech SOFA
python auto_sofalizer.py ./docs ./processed/docs mkv,mp4 1 --sofa speech.sofa
```

### Workflow 3: Quality Control Pipeline

```bash
# Step 1: Dry run to count files
python auto_sofalizer.py ./input ./output mkv 1 --dry-run

# Step 2: Process with temp files kept
python auto_sofalizer.py ./input ./output mkv 1 --keep-temp --verbose

# Step 3: Manually inspect intermediate files in ./output/temp/

# Step 4: If satisfied, process remaining and clean up
python auto_sofalizer.py ./input_batch2 ./output mkv 1
```

### Workflow 4: Testing Different Audio Tracks

Some videos have multiple audio tracks (languages, commentaries, etc.):

```bash
# Check available tracks
ffprobe -v error -show_entries stream=index,codec_type,codec_name -of compact video.mkv

# Test with track 0
python auto_sofalizer.py ./test ./test_output mkv 0 --keep-temp

# Test with track 1
python auto_sofalizer.py ./test ./test_output mkv 1 --keep-temp

# Compare results and choose best track
```

## Troubleshooting Examples

### Example: Diagnose Processing Failure

A file fails to process:

```bash
# Run with maximum verbosity
python auto_sofalizer.py ./problem_videos ./output mkv 1 --ffmpeg-verbosity debug --verbose --keep-temp

# Check the detailed log
cat ./output/temp/processing.log

# Manually test FFmpeg commands from log
ffmpeg -i problem_video.mkv
```

### Example: Check SOFA File Compatibility

```bash
# Test SOFA file with a sample video
python auto_sofalizer.py ./test_sample ./test_output mkv 1 --sofa new_sofa.sofa --verbose

# If it works, proceed with full batch
python auto_sofalizer.py ./full_collection ./output mkv 1 --sofa new_sofa.sofa
```

### Example: Resume After Interruption

Script was interrupted (Ctrl+C):

```bash
# Processed files are skipped automatically
# Just run the same command again
python auto_sofalizer.py ./videos ./output mkv 1

# Output will show:
# "Output file already exists: output/movie1(sofa).mkv"
# "Skipping... (delete the output file if you want to reprocess)"
```

## Integration Examples

### Example: Batch Script (Windows)

Create `process_all.bat`:

```batch
@echo off
echo Processing Movies...
python auto_sofalizer.py "D:\Movies" "D:\Movies_Binaural" mkv 1

echo Processing TV Shows...
python auto_sofalizer.py "D:\TV" "D:\TV_Binaural" mkv 1

echo Processing Anime...
python auto_sofalizer.py "D:\Anime" "D:\Anime_Binaural" mkv 1 --sofa anime_hrtf.sofa

echo All done!
pause
```

### Example: Bash Script (Linux/macOS)

Create `process_all.sh`:

```bash
#!/bin/bash

# Configuration
INPUT_BASE="/mnt/media"
OUTPUT_BASE="/mnt/media_processed"
SOFA_FILE="./irc_1003.sofa"

# Process each subfolder
for folder in movies tv_shows documentaries; do
    echo "Processing $folder..."
    python3 auto_sofalizer_improved.py \
        "$INPUT_BASE/$folder" \
        "$OUTPUT_BASE/$folder" \
        mkv,mp4 \
        1 \
        --sofa "$SOFA_FILE" \
        --verbose
done

echo "All processing complete!"
```

Make it executable:
```bash
chmod +x process_all.sh
./process_all.sh
```

### Example: Python Script for Automation

Create `automated_processor.py`:

```python
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def process_folder(input_folder, output_folder, extensions="mkv", track=1):
    """Process a folder with auto_sofalizer"""
    cmd = [
        sys.executable,
        "auto_sofalizer_improved.py",
        str(input_folder),
        str(output_folder),
        extensions,
        str(track)
    ]
    
    print(f"Processing: {input_folder}")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✓ Success: {input_folder}")
    else:
        print(f"✗ Failed: {input_folder}")
    
    return result.returncode

if __name__ == "__main__":
    folders = [
        ("./movies", "./movies_processed"),
        ("./tv_shows", "./tv_processed"),
        ("./anime", "./anime_processed"),
    ]
    
    for input_dir, output_dir in folders:
        process_folder(input_dir, output_dir)
```

### Example: Watch Folder Automation

Create `watch_and_process.py`:

```python
#!/usr/bin/env python3
"""
Watch a folder and automatically process new video files
Requires: pip install watchdog
"""
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class VideoFileHandler(FileSystemEventHandler):
    def __init__(self, output_folder):
        self.output_folder = output_folder
        self.extensions = {'.mkv', '.mp4', '.avi'}
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix.lower() in self.extensions:
            print(f"New file detected: {file_path}")
            time.sleep(5)  # Wait for file to finish writing
            self.process_file(file_path)
    
    def process_file(self, file_path):
        cmd = [
            "python",
            "auto_sofalizer_improved.py",
            str(file_path.parent),
            str(self.output_folder),
            file_path.suffix[1:],  # Extension without dot
            "1"
        ]
        subprocess.run(cmd)

if __name__ == "__main__":
    watch_folder = Path("./watch")
    output_folder = Path("./processed")
    
    watch_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    
    event_handler = VideoFileHandler(output_folder)
    observer = Observer()
    observer.schedule(event_handler, str(watch_folder), recursive=False)
    observer.start()
    
    print(f"Watching folder: {watch_folder}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

## Performance Tips

### Tip 1: Process During Off-Hours

For large batches, use task scheduler:

**Windows Task Scheduler:**
```batch
REM Run at 2 AM daily
schtasks /create /tn "Auto Sofalizer" /tr "python C:\path\to\auto_sofalizer_improved.py C:\input C:\output mkv 1" /sc daily /st 02:00
```

**Linux Cron:**
```bash
# Add to crontab
0 2 * * * cd /path/to/auto_sofalizer && python3 auto_sofalizer_improved.py /input /output mkv 1
```

### Tip 2: Process by File Size

Process smaller files first for quick wins:

```bash
# List files by size
ls -lSr ./videos/*.mkv

# Process individually
python auto_sofalizer.py ./videos/small1.mkv ./output mkv 1
python auto_sofalizer.py ./videos/small2.mkv ./output mkv 1
# ... then larger files
```

### Tip 3: Monitor System Resources

```bash
# Windows (PowerShell)
Get-Process python | Select-Object CPU,WorkingSet

# Linux/macOS
top -p $(pgrep -f auto_sofalizer)
```

## Best Practices

1. **Always test first**: Use `--dry-run` on new batches
2. **Keep originals**: Never overwrite source files
3. **Check results**: Sample processed files before deleting originals
4. **Use appropriate SOFA**: Different content may benefit from different SOFA files
5. **Monitor disk space**: Processing creates temporary files
6. **Regular backups**: Keep backups of both originals and SOFA files

## Need Help?

- Check the main [README.md](../README.md)
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for development help
- Open an issue on GitHub with details and logs

---

**Happy spatial audio processing! 🎧**

