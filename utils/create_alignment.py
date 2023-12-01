import os
import requests
import json

# Need the wav, transcription files and to run the docker container for the alignment model "docker run -P lowerquality/gentle"

# Directory paths
audio_dir = 'wavs'
transcript_dir = 'transcriptions'
alignment_dir= 'alignments'

# Get lists of files in each directory
audio_files = os.listdir(audio_dir)
transcript_files = os.listdir(transcript_dir)
alignment_files = os.listdir(alignment_dir)

# Construct full paths for each file
audio_paths = [os.path.join(audio_dir, file) for file in audio_files]
transcript_paths = [os.path.join(transcript_dir, file) for file in transcript_files]

# URL for POST request
url = "http://localhost:32769/transcriptions?async=false"

# Iterate and send requests
for audio_path in audio_paths:
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    if (base_name + '.json') not in alignment_files:   
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
                with open('alignments/'+ base_name+ '.json', 'w') as file:
                    json.dump(response.json(), file, indent=4)

                # Handle the response
                if response.status_code == 200:
                    print(f"Successfully sent {audio_path} and {transcript_path}")
                else:
                    print(f"Failed to send {audio_path} and {transcript_path}: {response.status_code}, {response.text}")
        else:
            print(f"No corresponding transcript found for {audio_path}")
