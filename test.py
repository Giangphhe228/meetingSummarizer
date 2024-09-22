from convert_file import files
import os
import re

def extract_index(filename):
    match = re.search(r'_(\d+)\.txt$', filename)  # Adjust pattern based on file format
    return int(match.group(1)) if match else float('inf') 

key = extract_index
# Sort files based on the extracted index
sorted_files = sorted(files, key)

# Loop through the sorted files
for file in sorted_files:
    file_path = os.path.join("outputSegment9min/", file)
    print(f"Processing file: {file_path}")
    