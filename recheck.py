import google.generativeai as genai
from convert_file import files
from gemini import YOUR_API_KEY
import os

# Safety settings for the generative model
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Function to upload a file to the generative AI service
def upload_file(file_path):
    print("*** Uploading file ***")
    upload_file = genai.upload_file(path=file_path, display_name=os.path.splitext(os.path.basename(file_path))[0])
    print(f"Uploaded file '{upload_file.display_name}' as: {upload_file.uri}")
    return upload_file

# Main function to perform the recheck process
def recheck():
    os.environ["GOOGLE_API_KEY"] = YOUR_API_KEY
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    file_path = ""
    for file in files("output/"):
        if file.endswith(".txt"):
            file_path = f"output/{file}"
            break

    if not file_path:
        print("No .txt file found in the output directory.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read()

    lines = contents.split('\n')
    previous_last_line = lines[-2] if len(lines) > 1 else ""
    last_line = lines[-1]
    document = f"{previous_last_line}\n{last_line}"

    prompt = (
        "You are a transcript analyst. Review the provided audio log, which includes transcripts and speaker information for each transcript, sorted by the time they occurred." 
        "Ensure that the new entries follow the chronological order and maintain the same format."
        "If the content is exhausted, add more last line , this string must include the content 'HH:mm:ss-HH:mm Kết thúc cuộc họp!!!!' where HH:mm represents the last time of the audio file."
        f"Using the template: 'HH:mm:ss-HH:mm Speaker1: content\n', continue the transcript of the meeting starting from the time of this last line {document}."
    )

    result = upload_file(file_path)

    print("*** Getting transcription ***")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content([result, prompt], safety_settings=safety_settings)
    print("*** Completed getting transcription ***")

    with open(file_path, "a", encoding="utf-8") as text_file:
        text_file.write(response.text)
    print(f"*** Completed writing transcription to {file_path} ***")

if __name__ == "__main__":
    recheck()
