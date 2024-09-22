import argparse
from convert_file import convert, files
import google.generativeai as genai
from gemini import YOUR_API_KEY
from gemini import run
from recheck import recheck
from summarize import summarize
import os
import time



def clear():
    os.environ["GOOGLE_API_KEY"] = YOUR_API_KEY
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    for files in genai.list_files():
        files.delete()
    print('*** Deleted files in Gemini storage ***')

def auto():
    clear()
    convert()
    run() 
    audio_path = ""
    for file in files("output/"):
        if file.endswith(".mp3"):
            audio_path = f"output/{file}"
    if not audio_path:
        print("No .mp3 file found in the output directory.")
        return

    txt_time = getTxtLastline()
    time.sleep(30)
    while ("Kết thúc cuộc họp!!!!" in txt_time):
      clear()
      time.sleep(30)
      recheck()
      txt_time = getTxtLastline()
    
    clear()
    time.sleep(30)
    summarize()


def getTxtLastline():
    txt_path = ""
    for file in files("output/"):
        if file.endswith(".txt"):
            txt_path = f"output/{file}"
    if not txt_path:
        print("No .txt file found in the output directory.")
        return
    
    with open(txt_path, "r") as file:
        contents = file.read()

    lines = contents.split('\n')
    last_line = lines[-1]
    return last_line

def action(act):
    if act == "convert":
        convert()
    elif act == "run":
        clear()
        run()
    elif act == "recheck":
        clear()
        recheck()
    elif act == "summarize":
        clear()
        summarize()
    elif act == "auto":
        auto()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform actions: convert, run, recheck , summarize or auto.')
    parser.add_argument('act', choices=['convert', 'run', 'recheck', 'summarize', 'auto'], help='The action to perform')
    args = parser.parse_args()
    action(args.act)

