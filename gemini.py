import google.generativeai as genai
from convert_file import files
import os
import re


YOUR_API_KEY = "API key from aistudio.google.com"
# Safety settings for the generative model
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def clear():
    os.environ["GOOGLE_API_KEY"] = YOUR_API_KEY
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    for files in genai.list_files():
        files.delete()
    print('*** Deleted files in Gemini storage ***')

# Function to upload a file to the generative AI service
def upload_file(file_path):
    print("*** Uploading file ***")
    upload_file = genai.upload_file(path=file_path, display_name=os.path.splitext(os.path.basename(file_path))[0])
    print(f"Uploaded file '{upload_file.display_name}' as: {upload_file.uri}")
    return upload_file

# Function to extract the index from the filename
def extract_index(filename):
    # Assuming the index is the number after the last underscore and before the extension
    try:
        # Split the filename by underscores and take the last part before the file extension
        return int(filename.split('_')[-1].split('.')[0])
    except ValueError:
        return float('inf')  # Assign an infinite value for files that don't match the pattern



# Main function to run the transcription process
def run():
    os.environ["GOOGLE_API_KEY"] = YOUR_API_KEY
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    prompt = (
        "Generate audio diarization, including transcriptions and speaker information for each segment of this meeting. "
        "Organize the transcriptions by the time they occurred. "
        "Format it using the template: 'HH:mm:ss-HH:mm:ss Speaker1: content\n'"
        "If the content is exhausted, add more last line , this string must include the content 'HH:mm:ss-HH:mm Kết thúc file !!!!' where HH:mm represents the last time of the audio file."
    )
    # Get a list of files in the folder
    filelist = os.listdir("outputSegment15min/")
    # Sort files based on the extracted index
    # Filter only the files that match the expected format
    filtered_files = [file for file in filelist if file.startswith("audio_segment_") and file.endswith(".mp3")]
    # Sort files based on the extracted index
    sorted_files = sorted(filtered_files, key=extract_index)

    for file in sorted_files:
        file_path = f"outputSegment15min/{file}"
        clear()
        print(f"*** upload transcription for file {file_path}***")
        result = upload_file(file_path)

        print("*** Getting transcription ***")
        model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        response = model.generate_content([result, prompt], safety_settings=safety_settings)
        print("*** Completed getting transcription ***")

        # Writing the transcription to a text file
        for appendfile in files("input/"):
            if appendfile.replace(".mp3", "") in file:
                transcribe_output_path = f"output/{appendfile}.txt".replace(".mp3", "")
                with open(transcribe_output_path, 'a', encoding="utf-8") as text_file:
                    # print("giá trị:", text_file)
                    text_file.write(response.text)
                print(f"*** Completed writing transcription to {transcribe_output_path} ***")
                break

if __name__ == "__main__":
    run()
