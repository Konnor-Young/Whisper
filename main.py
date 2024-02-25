from audio import is_file_under_size_limit, split_audio_file
from model import transcribe_audio, generate_meeting_minutes, get_last_tokens
import json
import argparse
import os

def save_json(data):
    """Save the data to a JSON file."""
    with open("text/transcript.json", 'r') as json_file:
        notes = json.load(json_file)
    notes.append(data)
    with open("text/transcript.json", 'w') as json_file:
        json.dump(notes, json_file, indent=4)

def save_text(data):
    """Save the data to a txt file."""
    with open(" text/transcript.txt", 'w') as file:
        file.write(data)

def main(file_path):
    with open(file_path, 'rb') as file:
        if is_file_under_size_limit(file_path):
            text = ""
            text = transcribe_audio(file)
        else:
            text = ""
            seg = split_audio_file(file_path)
            for i in range(len(seg)):
                if i == 0:
                    text += transcribe_audio(seg[i])
                else:
                    tok = get_last_tokens(text)
                    text += transcribe_audio(seg[i], tok)
    notes = generate_meeting_minutes(text)
    # print(notes)

    try:
        notes_json = json.loads(notes)
        save_json(notes_json)
        print("The returned notes are in a valid JSON format.")
        return
    except json.JSONDecodeError:
        print("The returned notes are not in a valid JSON format.")
        save_text(notes)
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an audio file to generate meeting notes.")
    parser.add_argument('file_path', type=str, help='The path to the audio file to process.')
    args = parser.parse_args()

    main(args.file_path)