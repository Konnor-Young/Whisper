import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

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

def split_audio_file(file_path, min_silence_len=1000, silence_thresh=-40, keep_silence=500):
    """
    Splits an audio file into segments based on silence.

    Parameters:
    - file_path: The path to the audio file to split.
    - min_silence_len: The minimum length of silence (in ms) that will be used to split the audio. Default is 1000ms.
    - silence_thresh: The silence threshold (in dB) below which the audio is considered silent. Default is -40 dB.
    - keep_silence: The amount of silence (in ms) to leave at the beginning and end of each segment. Default is 500ms.

    Returns:
    - A list of AudioSegment instances, each representing a segment of the original audio.
    """
    audio = AudioSegment.from_file(file_path)
    
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence
    )
    
    return segments
# Example usage
# file_path = 'path/to/your/audio/file.mp3'
# segments = split_audio_file(file_path)
# Optionally, save the segments to separate files
# for i, segment in enumerate(segments):
#     segment_path = f"segment_{i+1}.mp3"
#     segment.export(segment_path, format="mp3")
#     print(f"Exported {segment_path}")