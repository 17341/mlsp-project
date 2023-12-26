import pyaudio
import numpy as np
import torchaudio
import torch
import sys
from pathlib import Path

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.extract_features import extract_stft, extract_embedding

# PyAudio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 22050  # Sample rate
CHUNK = 1024  # Number of audio frames per buffer
DURATION = 0.5  # Duration to capture audio, in seconds

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Streaming started...")

frames = []
try:
    while True:
        # Read data from the stream
        data = stream.read(CHUNK)
        frames.append(data)

        # Check if 1 second has passed
        if len(frames) * CHUNK >= RATE * DURATION:
            # Combine all frames
            all_data = b''.join(frames)
            frames = []  # Clear the frames list for the next second

            # Convert byte data to NumPy array
            numpy_data = np.frombuffer(all_data, dtype=np.int16)

            # features = extract_stft(numpy_data.copy(), RATE, fixed_length=100)
            features = extract_embedding(numpy_data.copy(), RATE)
            print(features.squeeze(0).squeeze(0))

except KeyboardInterrupt:
    # Stop stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Streaming stopped")
