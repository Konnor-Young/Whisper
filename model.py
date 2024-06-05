from openai import OpenAI
from transformers import GPT2Tokenizer
import os

# Load the API key from the .env file
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def get_last_tokens(text, num_tokens=224):
    """
    Extracts the last num_tokens tokens from the given text using GPT-2 tokenizer.

    Parameters:
    - text (str): The text from which to extract tokens.
    - num_tokens (int): The number of tokens to extract from the end of the text.

    Returns:
    - str: The extracted text corresponding to the last num_tokens tokens.
    """

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    tokens = tokenizer.encode(text)
    last_tokens_ids = tokens[-num_tokens:]
    last_tokens_text = tokenizer.decode(last_tokens_ids, skip_special_tokens=True)
    
    return last_tokens_text
# Example usage
# previous_segment_text = "Your previous segment's transcription goes here..."
# last_tokens_text = get_last_tokens(previous_segment_text)
# print("Last 224 tokens as text:", last_tokens_text)

def transcribe_audio(file_path, previous_transcript=None):
    """
    Transcribes an audio file using OpenAI's Whisper model, with an option to include
    the transcription of a previous segment for better context preservation.

    Parameters:
    - file_path (str): The path to the audio file to be transcribed.
    - previous_transcript (str, optional): The transcription of the previous audio segment,
      used to maintain context in the transcription process. Default is None.

    Returns:
    - str: The transcription of the audio file.
    """
    request_params = {
        "model": "whisper-1",
        "file": file_path,
        "response_format": "text",
        "language": "en",
    }
    if previous_transcript is not None:
        request_params["prompt"] = previous_transcript

    transcript = client.audio.transcriptions.create(**request_params)

    return transcript

def generate_meeting_minutes(transcription):
    """
    Generates a summary of meeting minutes from the provided transcription text using GPT-4.

    This function sends the transcription to GPT-4, instructing it to act as a helpful assistant
    that summarizes all important information from the meeting notes. The summarization aims to
    condense the content into key points, making it easier to understand the crucial aspects of the
    meeting without needing to go through the entire transcription.

    Parameters:
    - transcription (str): The transcription text of the meeting, which will be summarized.

    Returns:
    - str: The summarized text of the meeting minutes.
    """
    try:
        prompt = f"""
        The Following Transcription is from a class the transcription might include comments from both the instructor and the students, but they will not be labeled. Do you best to summarize the class discussion separating the teacher's comments from the students answers/questions.
        You should output your summary of the class in a JSON format that makes sense with the keys: Teachers Note (a summary of how the class went and what was covered), Student Questions (a summary of the questions asked by students), AI notes (here you can make comments on whether or not you felt certain questions were answered in a way that the students understood.)
        
        Transcription:
        "{transcription}"

        JSON Format:
        """ 
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Generate the JSON object."}
            ],
            seed=45,
            temperature=0.2,  # Adjust based on desired variability
        )
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            return "No summary could be generated."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error generating summary."