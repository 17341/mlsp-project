import os
import requests
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Need the wav, transcription files and to run the docker container for the alignment model "docker run -P lowerquality/gentle"

# Directory paths
audio_dir = f"{parent_dir}\data\wavs"
transcript_dir = f"{parent_dir}\data\\transcriptions"
alignment_dir= f"{parent_dir}\data\\alignments"

# Get lists of files in each directory
audio_files = os.listdir(audio_dir)
transcript_files = os.listdir(transcript_dir)
alignment_files = os.listdir(alignment_dir)

# Construct full paths for each file
audio_paths = [os.path.join(audio_dir, file) for file in audio_files]
transcript_paths = [os.path.join(transcript_dir, file) for file in transcript_files]

# URL for POST request
url = "http://localhost:32768/transcriptions?async=false"

# Iterate and send requests
for audio_path in audio_paths[8000:]:
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    if (base_name + '.json') not in alignment_files:   
        logging.info(f'Aligning file : {base_name}')

        transcript_path = os.path.join(transcript_dir, base_name + '.txt')

        # Check if the corresponding transcript file exists
        if os.path.isfile(transcript_path):
            with open(audio_path, 'rb') as audio, open(transcript_path, 'rb') as transcript:
                files = {
                    'audio': (os.path.basename(audio_path), audio),
                    'transcript': (os.path.basename(transcript_path), transcript)
                }
                response = requests.post(url, files=files)

                # Writing the dictionary to a file as JSON
                with open(f"{parent_dir}\data\\alignments\{base_name}.json", 'w') as file:
                    json.dump(response.json(), file, indent=4)

                # Handle the response
                if response.status_code == 200:
                    logging.info(f"Successfully sent {audio_path} and {transcript_path}")
                else:
                    logging.error(f"Failed to send {audio_path} and {transcript_path}: {response.status_code}, {response.text}")
        else:
            logging.warning(f"No corresponding transcript found for {audio_path}")
