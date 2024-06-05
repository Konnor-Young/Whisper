import librosa
import tempfile
import soundfile as sf
import os

def is_file_under_size_limit(file_path, size_limit_mb=25):
    """
    Check if the file size is under the specified limit in megabytes.

    Parameters:
    - file_path (str): The path to the file.
    - size_limit_mb (int): The size limit in megabytes. Default is 25MB.

    Returns:
    - bool: True if the file is under the size limit, False otherwise.
    """
    file_size_bytes = os.path.getsize(file_path)
    size_limit_bytes = size_limit_mb * 1024 * 1024
    return file_size_bytes < size_limit_bytes
#Example Usage
# file_path = 'path/to/audio.mp4'
# if is_file_under_size_limit(file_path):
#     print(f"The file is under the 25mb size limit.")
# else:
#     print(f"The file exceeds the 25mb size limit.")

def split_audio_by_size(file_path, size_limit_mb=25):
    """
    Splits an audio file into segments, ensuring each segment is under a specified maximum size.
    Saves the segments as temporary files and returns their file paths.

    Parameters:
    - file_path: The path to the audio file to split.
    - max_size_mb: The maximum size of each segment in megabytes.

    Returns:
    - A list of file paths, each representing a temporary audio file of a segment.
    """
    audio, sr = librosa.load(file_path)
    total_samples = len(audio)
    max_size_bytes = size_limit_mb * 1024 * 1024  # Convert MB to bytes
    
    segment_file_paths = []

    with tempfile.TemporaryDirectory() as temp_dir:
        segment_start = 0
        segment_index = 0
        
        while segment_start < total_samples:
            segment_end = segment_start
            segment_size_bytes = 0
            
            while segment_end < total_samples:
                segment = audio[segment_start:segment_end]
                segment_size_bytes = len(segment.tobytes())
                
                if segment_size_bytes > max_size_bytes:
                    break
                
                segment_end += 1

            segment = audio[segment_start:segment_end]
            segment_path = f"{temp_dir}/segment_{segment_index}.wav"
            sf.write(segment_path, segment, sr, format='WAV')
            segment_file_paths.append(segment_path)
            
            segment_start = segment_end
            segment_index += 1
    
    return segment_file_paths
# Example usage
# file_path = 'path/to/your/audio/file.mp3'
# max_size_mb = 25  # Maximum segment size in megabytes

# segment_file_paths = split_audio_by_size(file_path, max_size_mb)

# for segment_path in segment_file_paths:
#   # Pass each segment file path to your Whisper transcription function
    # transcribe_audio(segment_path)