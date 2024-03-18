import os
import sys
import subprocess
import re

# Check if correct number of arguments are provided
if len(sys.argv) != 4:
    print("Usage: python main.py \"path/to/input/folder\" \"path/to/output/folder\" \"audio_track_number\"")
    sys.exit(1)

input_folder = sys.argv[1]
output_folder = sys.argv[2]
audio_track_number = sys.argv[3]

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to extract max_volume from ffmpeg output
def get_max_volume(input_file, audio_track_number):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-map', '0:a:{}'.format(audio_track_number),
        '-af', 'volumedetect',
        '-vn',
        '-f', 'null',
        '-'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    max_volume_matches = re.search(r"max_volume: ([\-\d\.]+) dB", result.stderr)
    if max_volume_matches:
        return float(max_volume_matches.group(1))
    else:
        return 0

# Function to demux the selected audio track from the video
def demux_audio(input_video, output_audio, audio_track_number):
    demux_command = [
        'ffmpeg',
        '-i', input_video,
        '-map', '0:a:{}'.format(audio_track_number),
        '-c:a', 'copy',
        '-y', output_audio
    ]
    subprocess.run(demux_command)

# Function to process the audio with SOFA and gain
def process_audio(input_audio, output_audio, max_volume):
    # Calculate the adjustment needed (if max_volume is negative)
    volume_adjustment = '+{}dB'.format(-max_volume) if max_volume < 0 else '+0dB'

    # Construct the ffmpeg command for processing with SOFA and gain adjustment
    process_command = [
        'ffmpeg',
        '-i', input_audio,
        '-filter_complex', '[0:a]sofalizer=sofa=irc_1003.sofa[volume];[volume]volume={}'.format(volume_adjustment),
        '-c:a', 'flac',
        '-y', output_audio
    ]
    subprocess.run(process_command)

# Function to mux the new audio track into the video
def mux_audio(input_video, new_audio, output_video):
    mux_command = [
        'ffmpeg',
        '-i', input_video,
        '-i', new_audio,
        '-map', '1:a',
        '-map', '0:v',
        '-map', '0:a',
        '-map', '0:s?',
        '-c', 'copy',
        '-disposition:a:0', 'default',
        output_video
    ]
    subprocess.run(mux_command)

# Process each file in the input directory
for filename in os.listdir(input_folder):
    if filename.endswith(".mkv"):
        # Construct the full paths for input and output files
        input_file = os.path.join(input_folder, filename)
        demuxed_audio_file = os.path.join(output_folder, filename.replace('.mkv', '.mka'))
        processed_audio_file = os.path.join(output_folder, filename.replace('.mkv', '.flac'))
        output_file = os.path.join(output_folder, filename.replace('.mkv', '(sofa).mkv'))

        # Demux the selected audio track
        demux_audio(input_file, demuxed_audio_file, audio_track_number)

        # Get the max_volume from the first pass
        max_volume = get_max_volume(demuxed_audio_file, audio_track_number)

        # Process the audio with SOFA and gain
        process_audio(demuxed_audio_file, processed_audio_file, max_volume)

        # Mux the new audio track into the video
        mux_audio(input_file, processed_audio_file, output_file)

print("Processing complete.")
