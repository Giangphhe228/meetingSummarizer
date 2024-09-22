# README.md

## Overview

This project provides a set of Python scripts for processing audio files and generating meeting transcripts. The scripts perform various tasks including converting audio files, generating transcriptions, rechecking and filling missing transcriptions, and summarizing the meetings. 

## Requirements

Ensure you have the necessary dependencies installed. You can install them using:
```sh
pip install -r requirements.txt
```
Specific is pydub lib, you should search for how to instal it properly.

## How to Use

1. Place the audio files in the input folder.
2. Open gemini.py file and replace "YOUR_API_KEY" variable with the api key from aistudio google.
3. Cd to the folder location and then Run the `convert` script to convert the audio files.
4. Run the `run` script to generate meeting transcripts.
5. Run the `recheck` script to fill in any missing transcriptions.
6. Run the `summarize` script to summarize the meeting transcripts.

## Scripts

### 1. `convert`

**Description**: This script converts audio files from the input folder into a format suitable for transcription.

**Usage**:
```sh
python action.py convert
```

### 2. `run`

**Description**: This script generates meeting transcripts from the converted audio files.

**Usage**:
```sh
python action.py run
```

### 3. `recheck`

**Description**: This script fills in missing transcriptions from the initial run.

**Usage**:
```sh
python action.py recheck
```

### 4. `summarize`

**Description**: This script summarizes the generated meeting transcripts.

**Usage**:
```sh
python action.py summarize
```



## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the FPT Telecom License.


---

Feel free to modify this document to better suit your needs.