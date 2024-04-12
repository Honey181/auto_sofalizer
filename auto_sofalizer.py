import shutil
import os
import glob
import subprocess
import re
from tqdm import tqdm

# Define the sofa_file name
SOFA_FILE_NAME = 'irc_1003.sofa'

def run_command(command, log_file, progress=None):
    with open(log_file, 'a') as f:
        command_str = f"Running command: {' '.join(command)}\n"
        f.write(command_str)
        print(command_str)  # Print the command to the terminal
        f.flush()  # Flush the file to ensure the output is written immediately
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        max_volume = None
        for line in process.stdout:
            f.write(line)
            f.flush()  # Flush the file to ensure the output is written immediately
            print(line, end='')  # Output to terminal
            match = re.search(r"max_volume: (-?\d+.\d+) dB", line)
            if match:
                max_volume = float(match.group(1))
            if progress:
                progress.update()

        process.wait()
        return max_volume, process.returncode
       
def main(input_folder, output_folder, extensions, audio_track):
    original_dir = os.getcwd()
    ffmpeg_verbosity = 'repeat+24'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sofa_file = os.path.join(script_dir, SOFA_FILE_NAME)
    temp_folder = os.path.join(output_folder, 'temp')
    log_file = os.path.join(temp_folder, 'log.txt')
    
    # Check if temp_folder already exists and remove it if it does
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

    os.makedirs(temp_folder, exist_ok=True)
    os.chdir(temp_folder)

    # Copy the sofa_file to the temp_folder
    shutil.copy(sofa_file, temp_folder)
    sofa_file = SOFA_FILE_NAME

    total_files = sum([len(list(glob.glob(f"{input_folder}/*.{extension}"))) for extension in extensions])
    file_progress = tqdm(total=total_files, desc="Files", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

    for extension in extensions:
        for file in glob.glob(f"{input_folder}/*.{extension}"):
            filename = os.path.basename(file)
            base = os.path.splitext(filename)[0]
            output_file = f"{output_folder}/{base}(sofa).{extension}"

            step_progress = tqdm(total=8, desc="Steps", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', leave=False)
            
            # Extract audio track
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', file, '-map', f'0:{audio_track}', '-c:a', 'copy', f'{temp_folder}/{base}.mkv']
            run_command(command, log_file, step_progress)
            step_progress.update()

            # Process audio track with sofalizer filter
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', f'{temp_folder}/{base}.mkv', '-af', f'sofalizer=sofa={sofa_file}', f'{temp_folder}/{base}_sofa.flac']
            run_command(command, log_file, step_progress)
            step_progress.update()

            # Get max_volume
            command = ['ffmpeg', '-v', 'repeat+32', '-i', f'{temp_folder}/{base}_sofa.flac', '-af', 'volumedetect', '-f', 'null', '/dev/null']
            max_volume, returncode = run_command(command, log_file, step_progress)
            #print(f"Max volume: {max_volume} dB, Return code: {returncode}")
            step_progress.update()

            # Add gain
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', f'{temp_folder}/{base}_sofa.flac', '-af', f'volume={max_volume}', '-c:a', 'flac', f'{temp_folder}/{base}_gain.flac']
            _, returncode = run_command(command, log_file, step_progress)
            step_progress.update()

            # Mux the flac file
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', file, '-i', f'{temp_folder}/{base}_gain.flac', '-map', '1:a', '-map', '0', '-c', 'copy', '-max_interleave_delta', '0', '-y', f'{temp_folder}/{base}_almost_done.{extension}']
            run_command(command, log_file, step_progress)
            step_progress.update()

            # Remove default flag and add it to new track
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', f'{temp_folder}/{base}_almost_done.{extension}', '-map', '0', '-c', 'copy', '-disposition:a', '0', '-y', output_file]
            run_command(command, log_file, step_progress)
            step_progress.update()

            # Unmark all audio tracks as default
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', f'{temp_folder}/{base}_almost_done.{extension}', '-map', '0', '-c', 'copy', '-disposition:a', '0', '-y', f'{temp_folder}/{base}_unmarked.{extension}']
            run_command(command, log_file, step_progress)
            step_progress.update()

            # Mark the first audio track as default
            command = ['ffmpeg', '-v', ffmpeg_verbosity, '-i', f'{temp_folder}/{base}_unmarked.{extension}', '-map', '0', '-c', 'copy', '-disposition:a:0', 'default', '-y', output_file]
            run_command(command, log_file, step_progress)
            step_progress.update()

            step_progress.close()
            file_progress.update()

    file_progress.close()

    # Change the current working directory back to the original directory
    os.chdir(original_dir)
    # Ask user to remove temporary files
    remove_files = input("Do you want to remove temporary files? (y/N): ")
    if remove_files.lower() == 'y':
        shutil.rmtree(temp_folder)
    
    print("Script is done.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: python auto_sofalizer.py <input_folder> <output_folder> <extensions> <audio_track>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3].split(','), int(sys.argv[4]))
