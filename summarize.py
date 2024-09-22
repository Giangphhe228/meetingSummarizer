import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
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

# Main function to perform the summarize process
def summarize():
    os.environ["GOOGLE_API_KEY"] = YOUR_API_KEY
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    file_path = ""
    summarize_file_path = ""
    for file in files("output/"):
        if file.endswith(".txt"):
            file_path = f"output/{file}"
            summarize_file_path = f"output/summarize_{file}"
            break

    if not file_path:
        print("No .txt file found in the output directory.")
        return

    prompt = (
        "Hoạt động như một trợ lý hữu ích. Nhiệm vụ của bạn là tạo các ghi chú cuộc họp ngắn gọn, có tổ chức và chứa nhiều thông tin từ [bản ghi cuộc họp] được cung cấp."
        "Những ghi chú này phải nắm bắt chính xác các điểm chính, quyết định, mục hành động và mọi vấn đề chưa được giải quyết được thảo luận trong cuộc họp. Đảm bảo rằng các ghi chú rõ ràng và có cấu trúc sao cho dễ đọc và tham khảo."
        "Ngoài ra, các ghi chú nên bao gồm một bản tóm tắt hoặc tổng quan ngắn gọn về mục tiêu và kết quả chính của cuộc họp để tham khảo nhanh."

        "Tóm tắt file theo hướng dẫn phía trên"
    )
    result = upload_file(file_path)
    file_name = result.name

    print("*** Getting transcription ***")

    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
    myfile = genai.get_file(file_name)
    response = model.generate_content([myfile, prompt], safety_settings=safety_settings)
 
    print("*** Completed getting transcription ***", response)

    with open(summarize_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(response.text)
    print(f"*** Completed writing transcription to {file_path} ***")

if __name__ == "__main__":
    summarize()
