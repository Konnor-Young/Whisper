from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the API key from the .env file
load_dotenv()
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=file_path,
        response_format="text",
        language="en",
        )
    print("Transcript: "+transcript)
    return transcript

# Function to generate meeting minutes using GPT-4
def generate_meeting_minutes(transcription):
    response = client.chat.completions.create(
      model="gpt-4-0125-preview",  # Replace with gpt-4 model if available
      messages=[{"role":"system", "content": "You are a helpful assistant who has been taking notes on a meeting. You should now look through the notes and summarize all important information"},
                {"role": "user", "content": transcription}],
      temperature=0,
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    audio_file = open("VOXTAB_legal_audio.mp3", "rb")
    transcription = transcribe_audio(audio_file)
    meeting_minutes = generate_meeting_minutes(transcription)
    print(meeting_minutes)
    with open("meeting_minutes.txt", "w") as file:
        file.write(meeting_minutes)
    with open("meeting_notes_full.txt", "w") as file:
        file.write(transcription)
    # Here, you can add code to save the meeting minutes to a file