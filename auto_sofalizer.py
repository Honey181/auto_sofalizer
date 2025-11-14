#!/usr/bin/env python3
"""
Auto Sofalizer - Automated SOFA-based spatial audio processing for video files

This script processes video files by applying SOFA (Spatially Oriented Format for Acoustics)
filters to audio tracks, with automatic volume normalization.
"""

import os
import sys
import shutil
import glob
import subprocess
import re
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    print("Note: Install 'tqdm' for progress bars: pip install tqdm")


__version__ = "2.0.0"
__author__ = "Auto Sofalizer Contributors"


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuration for audio processing"""
    input_folder: Path
    output_folder: Path
    extensions: List[str]
    audio_track: int
    sofa_file: Path
    ffmpeg_verbosity: str = 'repeat+24'
    keep_temp: bool = False
    dry_run: bool = False
    skip_normalize: bool = False
    
    def validate(self) -> None:
        """Validate the configuration"""
        if not self.input_folder.exists():
            raise ValueError(f"Input folder does not exist: {self.input_folder}")
        
        if not self.input_folder.is_dir():
            raise ValueError(f"Input path is not a directory: {self.input_folder}")
        
        if not self.sofa_file.exists():
            raise ValueError(f"SOFA file does not exist: {self.sofa_file}")
        
        if self.audio_track < 0:
            raise ValueError(f"Audio track must be non-negative: {self.audio_track}")
        
        if not self.extensions:
            raise ValueError("At least one file extension must be specified")


class FFmpegCommandError(Exception):
    """Raised when an FFmpeg command fails"""
    pass


class AudioProcessor:
    """Handles audio processing operations using FFmpeg"""
    
    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.temp_folder = config.output_folder / 'temp'
        self.log_file = self.temp_folder / 'processing.log'
        self.stats = {
            'processed': 0,
            'failed': 0,
            'skipped': 0
        }
        self.file_handler = None  # Will be set up in setup_workspace()
    
    @staticmethod
    def check_ffmpeg() -> bool:
        """Check if FFmpeg is available"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def setup_workspace(self) -> None:
        """Setup the temporary workspace"""
        logger.info(f"Setting up workspace at: {self.temp_folder}")
        
        # Create output folder if it doesn't exist
        self.config.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Remove existing temp folder if it exists
        if self.temp_folder.exists():
            logger.warning(f"Removing existing temp folder: {self.temp_folder}")
            shutil.rmtree(self.temp_folder)
        
        # Create temp folder
        self.temp_folder.mkdir(parents=True, exist_ok=True)
        
        # Setup logging to file (now that temp folder exists)
        self.file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(self.file_handler)
        
        # Copy SOFA file to temp folder
        sofa_dest = self.temp_folder / self.config.sofa_file.name
        shutil.copy(self.config.sofa_file, sofa_dest)
        logger.info(f"Copied SOFA file to: {sofa_dest}")
    
    def run_command(self, command: List[str], description: str = "") -> Tuple[Optional[float], int]:
        """
        Run an FFmpeg command and capture output
        
        Args:
            command: Command to run as list of strings
            description: Human-readable description of the command
            
        Returns:
            Tuple of (max_volume, return_code)
            
        Raises:
            FFmpegCommandError: If the command fails
        """
        if description:
            logger.info(f"Running: {description}")
        
        command_str = ' '.join(str(c) for c in command)
        logger.debug(f"Command: {command_str}")
        
        if self.config.dry_run:
            logger.info("[DRY RUN] Would execute: " + command_str)
            return None, 0
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            max_volume = None
            output_lines = []
            
            for line in process.stdout:
                output_lines.append(line)
                # Look for max_volume in volumedetect output
                match = re.search(r"max_volume:\s*(-?\d+\.?\d*)\s*dB", line)
                if match:
                    max_volume = float(match.group(1))
            
            return_code = process.wait()
            
            if return_code != 0:
                error_msg = f"Command failed with return code {return_code}"
                logger.error(error_msg)
                logger.error("Last 10 lines of output:")
                for line in output_lines[-10:]:
                    logger.error(line.rstrip())
                raise FFmpegCommandError(error_msg)
            
            return max_volume, return_code
            
        except FileNotFoundError:
            raise FFmpegCommandError("FFmpeg not found. Please install FFmpeg and ensure it's in your PATH")
        except Exception as e:
            raise FFmpegCommandError(f"Unexpected error running command: {e}")
    
    def get_stream_info(self, input_file: Path, stream_index: int) -> dict:
        """
        Get information about a specific stream using ffprobe
        
        Args:
            input_file: Path to input file
            stream_index: Stream index to query
            
        Returns:
            Dictionary with stream info
        """
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-select_streams', str(stream_index),
                 '-show_entries', 'stream=codec_type,codec_name,channels,channel_layout,sample_rate:stream_tags=language,title',
                 '-show_entries', 'stream_disposition=default',
                 '-of', 'json', str(input_file)],
                capture_output=True,
                text=True,
                check=True
            )
            
            import json
            data = json.loads(result.stdout)
            if data.get('streams'):
                return data['streams'][0]
            return {}
        except Exception as e:
            logger.debug(f"Could not get stream info: {e}")
            return {}
    
    def process_file(self, input_file: Path) -> bool:
        """
        Process a single video file
        
        Args:
            input_file: Path to input video file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filename = input_file.name
            base = input_file.stem
            extension = input_file.suffix[1:]  # Remove the dot
            output_file = self.config.output_folder / f"{base}(sofa).{extension}"
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {filename}")
            logger.info(f"{'='*60}")
            
            if output_file.exists():
                logger.warning(f"Output file already exists: {output_file}")
                logger.warning("Skipping... (delete the output file if you want to reprocess)")
                self.stats['skipped'] += 1
                return False
            
            # Get and display selected audio track info
            stream_info = self.get_stream_info(input_file, self.config.audio_track)
            if stream_info:
                logger.info(f"Selected audio track (stream {self.config.audio_track}):")
                
                codec_type = stream_info.get('codec_type', 'unknown')
                codec_name = stream_info.get('codec_name', 'unknown')
                logger.info(f"  Type: {codec_type.upper()} ({codec_name.upper()})")
                
                if 'channels' in stream_info:
                    channels = stream_info['channels']
                    layout = stream_info.get('channel_layout', 'unknown')
                    logger.info(f"  Channels: {channels} ({layout})")
                
                if 'sample_rate' in stream_info:
                    sample_rate = int(stream_info['sample_rate']) / 1000
                    logger.info(f"  Sample rate: {sample_rate} kHz")
                
                tags = stream_info.get('tags', {})
                if 'language' in tags:
                    logger.info(f"  Language: {tags['language']}")
                if 'title' in tags:
                    logger.info(f"  Title: {tags['title']}")
                
                disposition = stream_info.get('disposition', {})
                if disposition.get('default') == 1:
                    logger.info(f"  Default: Yes")
                
                logger.info("")  # Empty line for readability
            
            # Step 1: Extract audio track
            extracted_audio = self.temp_folder / f"{base}.mkv"
            self.run_command(
                ['ffmpeg', '-v', self.config.ffmpeg_verbosity, '-i', str(input_file),
                 '-map', f'0:{self.config.audio_track}', '-c:a', 'copy', str(extracted_audio)],
                f"Extracting audio track {self.config.audio_track}"
            )
            
            # Step 2: Apply sofalizer filter
            sofa_file_name = self.config.sofa_file.name
            sofalizer_output = self.temp_folder / f"{base}_sofa.flac"
            self.run_command(
                ['ffmpeg', '-v', self.config.ffmpeg_verbosity, '-i', str(extracted_audio),
                 '-af', f'sofalizer=sofa={sofa_file_name}', str(sofalizer_output)],
                "Applying SOFA spatial audio filter"
            )
            
            # Step 3 & 4: Volume detection and normalization (optional)
            if self.config.skip_normalize:
                logger.info("Skipping volume normalization (--no-normalize flag)")
                normalized_audio = sofalizer_output  # Use SOFA output directly
            else:
                # Step 3: Detect volume
                max_volume, _ = self.run_command(
                    ['ffmpeg', '-v', 'repeat+32', '-i', str(sofalizer_output),
                     '-af', 'volumedetect', '-f', 'null', os.devnull],
                    "Detecting audio volume"
                )
                
                if max_volume is None:
                    logger.warning("Could not detect max volume, skipping normalization")
                    gain_db = "0dB"
                else:
                    gain_db = f"{-max_volume}dB"
                    logger.info(f"Max volume: {max_volume} dB, applying gain: {gain_db}")
                
                # Step 4: Apply gain normalization
                normalized_audio = self.temp_folder / f"{base}_gain.flac"
                self.run_command(
                    ['ffmpeg', '-v', self.config.ffmpeg_verbosity, '-i', str(sofalizer_output),
                     '-af', f'volume={gain_db}', '-c:a', 'flac', str(normalized_audio)],
                    "Applying volume normalization"
                )
            
            # Step 5: Mux the processed audio with original video
            almost_done = self.temp_folder / f"{base}_almost_done.{extension}"
            self.run_command(
                ['ffmpeg', '-v', self.config.ffmpeg_verbosity, '-i', str(input_file),
                 '-i', str(normalized_audio), '-map', '1:a', '-map', '0', '-c', 'copy',
                 '-max_interleave_delta', '0', '-y', str(almost_done)],
                "Muxing processed audio with video"
            )
            
            # Step 6: Set audio track disposition (combined: unmark all, then mark first)
            self.run_command(
                ['ffmpeg', '-v', self.config.ffmpeg_verbosity, '-i', str(almost_done),
                 '-map', '0', '-c', 'copy', '-disposition:a', '0', 
                 '-disposition:a:0', 'default', '-y', str(output_file)],
                "Setting processed audio as default track"
            )
            
            # Clean up intermediate files for this video
            for temp_file in self.temp_folder.glob(f"{base}*"):
                if temp_file.is_file() and temp_file != output_file:
                    temp_file.unlink()
            
            logger.info(f"[SUCCESS] Successfully processed: {filename}")
            logger.info(f"  Output: {output_file}")
            self.stats['processed'] += 1
            return True
            
        except FFmpegCommandError as e:
            logger.error(f"[FAILED] Failed to process {input_file.name}: {e}")
            self.stats['failed'] += 1
            return False
        except Exception as e:
            logger.error(f"[ERROR] Unexpected error processing {input_file.name}: {e}")
            self.stats['failed'] += 1
            return False
    
    def process_all(self) -> None:
        """Process all matching files in the input folder"""
        # Find all matching files
        all_files = []
        for extension in self.config.extensions:
            pattern = self.config.input_folder / f"*.{extension}"
            files = list(self.config.input_folder.glob(f"*.{extension}"))
            all_files.extend(files)
        
        if not all_files:
            logger.warning(f"No files found matching extensions: {', '.join(self.config.extensions)}")
            logger.warning(f"Searched in: {self.config.input_folder}")
            return
        
        logger.info(f"Found {len(all_files)} file(s) to process")
        
        # Process files
        if TQDM_AVAILABLE and not self.config.dry_run:
            iterator = tqdm(all_files, desc="Processing files", unit="file")
        else:
            iterator = all_files
        
        for input_file in iterator:
            self.process_file(input_file)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print processing summary"""
        logger.info(f"\n{'='*60}")
        logger.info("PROCESSING SUMMARY")
        logger.info(f"{'='*60}")
        logger.info(f"Successfully processed: {self.stats['processed']}")
        logger.info(f"Failed: {self.stats['failed']}")
        logger.info(f"Skipped: {self.stats['skipped']}")
        logger.info(f"{'='*60}\n")
    
    def cleanup(self) -> None:
        """Clean up temporary files"""
        if self.config.keep_temp:
            logger.info(f"Keeping temporary files in: {self.temp_folder}")
            return
        
        if self.config.dry_run:
            logger.info("[DRY RUN] Would remove temporary files")
            return
        
        try:
            if self.temp_folder.exists():
                # Ask user for confirmation
                response = input(f"\nRemove temporary files in {self.temp_folder}? [y/N]: ").strip().lower()
                if response == 'y':
                    shutil.rmtree(self.temp_folder)
                    logger.info("Temporary files removed")
                else:
                    logger.info(f"Temporary files kept in: {self.temp_folder}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary files: {e}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Auto Sofalizer - Apply SOFA spatial audio filters to video files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all MKV files in a folder
  %(prog)s input_videos/ output_videos/ mkv 1
  
  # Process multiple file types
  %(prog)s input/ output/ mkv,mp4,avi 1
  
  # Use custom SOFA file
  %(prog)s input/ output/ mkv 1 --sofa custom.sofa
  
  # Dry run (show what would be done)
  %(prog)s input/ output/ mkv 1 --dry-run
  
  # Keep temporary files for debugging
  %(prog)s input/ output/ mkv 1 --keep-temp
        """
    )
    
    parser.add_argument(
        'input_folder',
        type=str,
        help='Input folder containing video files'
    )
    
    parser.add_argument(
        'output_folder',
        type=str,
        help='Output folder for processed videos'
    )
    
    parser.add_argument(
        'extensions',
        type=str,
        help='File extensions to process (comma-separated, e.g., "mkv,mp4,avi")'
    )
    
    parser.add_argument(
        'audio_track',
        type=int,
        help='Stream index of audio track (usually 1 for first audio, 2 for second, etc. Use ffprobe to check)'
    )
    
    parser.add_argument(
        '--sofa',
        type=str,
        default='irc_1003.sofa',
        help='SOFA file to use (default: irc_1003.sofa in script directory)'
    )
    
    parser.add_argument(
        '--ffmpeg-verbosity',
        type=str,
        default='repeat+24',
        choices=['quiet', 'panic', 'fatal', 'error', 'warning', 'info', 'verbose', 'debug', 'repeat+24', 'repeat+32'],
        help='FFmpeg verbosity level (default: repeat+24)'
    )
    
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary files after processing'
    )
    
    parser.add_argument(
        '--no-normalize',
        action='store_true',
        help='Skip volume normalization (faster but audio will likely be too quiet). SOFA processing typically reduces volume.'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually processing'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point"""
    args = parse_arguments()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Resolve paths
    script_dir = Path(__file__).parent.resolve()
    input_folder = Path(args.input_folder).resolve()
    output_folder = Path(args.output_folder).resolve()
    
    # Resolve SOFA file path
    sofa_path = Path(args.sofa)
    if not sofa_path.is_absolute():
        sofa_path = script_dir / args.sofa
    
    # Parse extensions
    extensions = [ext.strip() for ext in args.extensions.split(',')]
    
    # Create configuration
    try:
        config = ProcessingConfig(
            input_folder=input_folder,
            output_folder=output_folder,
            extensions=extensions,
            audio_track=args.audio_track,
            sofa_file=sofa_path,
            ffmpeg_verbosity=args.ffmpeg_verbosity,
            keep_temp=args.keep_temp,
            dry_run=args.dry_run,
            skip_normalize=args.no_normalize
        )
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    
    # Check FFmpeg availability
    if not AudioProcessor.check_ffmpeg():
        logger.error("FFmpeg is not installed or not in PATH")
        logger.error("Please install FFmpeg: https://ffmpeg.org/download.html")
        return 1
    
    logger.info(f"Auto Sofalizer v{__version__}")
    logger.info(f"Input folder: {config.input_folder}")
    logger.info(f"Output folder: {config.output_folder}")
    logger.info(f"Extensions: {', '.join(config.extensions)}")
    logger.info(f"Audio track: {config.audio_track}")
    logger.info(f"SOFA file: {config.sofa_file}")
    
    if config.skip_normalize:
        logger.warning("Volume normalization DISABLED - output will likely be too quiet (SOFA typically reduces volume)")
    
    if args.dry_run:
        logger.info("\n*** DRY RUN MODE - No files will be modified ***\n")
    
    # Create processor and run
    processor = AudioProcessor(config)
    
    try:
        processor.setup_workspace()
        processor.process_all()
        processor.cleanup()
        
        logger.info("All done!")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\n\nInterrupted by user")
        logger.info(f"Temporary files are in: {processor.temp_folder}")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.exception("Stack trace:")
        return 1


if __name__ == "__main__":
    sys.exit(main())

