from openai import OpenAI
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import pytesseract
import extract_msg
import os
import json

client = OpenAI()

def get_text(file):
    reader = PdfReader(file)
    # number_of_pages = len(reader.pages)
    text=''
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_gpt_input(file, input):
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        response_format={"type": "json_object"},
        messages=[{
        "role": "system", "content": """You are an Experienced CPCU working for a risk managment company. We have some insurance companies that will send us information from time to time. 
        Because of your experience in the risk managment/insurance field you have been studying how vector stores work in an attempt to make a chat bot. 
        You are going to work with the user to create a vector store to be use with a RAG chat bot. 
        The user will give you a single document These documents will be from varying sources and purposes. 
        You job will be to look through the text given to you and pull out any information that should be stored as meta-data for the vector store entry. 
        The meta-data will be used for search purposes beyond similarity searches so the meta-data should be information that someone might be trying to find about the insurance company from the text. 
        Then clean up the text by formatting it and removing any excess information.  Be sure that the text retains all important information. 
        The meta-data key should be an object with specific fields the fields you are looking for are: Company Name, Date of communication, and subject.
        You then should set your 'content' key to be the content of the message cleaned and formatted.
        You should no other text besides the json object with the data, ready to be store in a vector store."""},
        {"role": "user", "content": input}
        ]
    )
    with open('text.json', 'r') as json_file:
        data = json.load(json_file)
    data.append(json.loads(response.choices[0].message.content))
    print(data)
    with open('text.json', 'w') as json_file:
        json.dump(data, json_file)

def main():
    text=''
    gen_place=''
    for folder in os.listdir('/mnt/c/Users/konno/Desktop/PDF4LMX'):
        gen_place = folder
        folder_path = os.path.join('/mnt/c/Users/konno/Desktop/PDF4LMX', folder)
        if os.path.isdir(folder_path):
            # Iterate through each file in the current folder
            for file_name in os.listdir(folder_path):
                text=''
                file = os.path.join(folder_path, file_name)
                if os.path.isfile(file):
                    try:
                        reader = PdfReader(file)
                        for page in reader.pages:
                            text += page.extract_text()
                        if(len(text.split())==0):
                            pages = convert_from_path(file)
                            for page in pages:
                                text += pytesseract.image_to_string(page)
                                input = "Here is the document text: "+text+", and here is the folder I got the file from"+gen_place
                                get_gpt_input(file, input)
                        else:
                            input = "Here is the document text: "+text+", and here is the folder I got the file from"+gen_place
                            get_gpt_input(file, input)
                    except:
                        with extract_msg.Message(file) as msg:
                            # subject = msg.subject
                            # body = msg.body
                            text += msg.subject+" "+msg.body
                            input = "Here is the document text: "+text+", and here is the folder I got the file from"+gen_place
                            get_gpt_input(file, input)
                else:
                    print(file)
                    print("is not file")
    
main()