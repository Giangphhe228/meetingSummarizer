from pydub import AudioSegment
import os

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def segment(audio,filename):

    # Duration of each segment in milliseconds
    segment_duration = 900000  # e.g., 90 mins

    # Loop through and export each segment
    for i in range(0, len(audio), segment_duration):
        outputfile=f"outputSegment15min/audio_segment_{filename}".replace(".mp3",f"_{int((i/segment_duration)+1)}.mp3")
        if not os.path.exists(outputfile):
            segment = audio[i:i + segment_duration]
            segment.export(outputfile, format="mp3")
            print(f"Converted {filename} to {outputfile}")
        else:
            print(f"{outputfile} already exists, skipping conversion")
    
    print("All audio segments saved successfully.")
    
def convert():
    for file in files("input/"):
        audio=AudioSegment.from_file(f"input/{file}")
        segment(audio,file)

if __name__ == "__main__":
    convert()
