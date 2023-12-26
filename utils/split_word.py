from pydub import AudioSegment
import json
import os
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

audio_dir = f"{parent_dir}\data\wavs"
alignment_dir= f"{parent_dir}\data\\alignments"
words_dir = f"{parent_dir}\data\words"

audio_files = os.listdir(audio_dir)
alignment_files = os.listdir(alignment_dir)

word_count = {}

for i, wav_file in enumerate(audio_files):
    audio = AudioSegment.from_wav(f"{audio_dir}\{wav_file}")
    alignment = alignment_files[i]

    with open(f"{alignment_dir}\{alignment}", 'r') as jf:
        data = json.load(jf)

    for word_info in data["words"]:
        try:
            start_ms = word_info["start"] * 1000  
            end_ms = word_info["end"] * 1000     
            word_text = word_info["word"]
            
            if word_text not in word_count:
                word_count[word_text] = 1
            else:
                word_count[word_text] += 1

            word_dir = os.path.join(words_dir, word_text)
            if not os.path.exists(word_dir):
                os.makedirs(word_dir)

            filename = f"{word_dir}/{word_text}_{word_count[word_text]}.wav"

            segment = audio[start_ms:end_ms]
            segment.export(filename, format="wav")
        except :
            print('Error: ',wav_file, word_info)
