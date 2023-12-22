import os
import numpy as np
import scipy.io.wavfile as wav
from sklearn.metrics import mean_squared_error
import math

def add_gaussian_noise(signal, noise_level=0.01):
    noise = np.random.normal(0, noise_level, len(signal))
    return np.clip(signal + noise, -1.0, 1.0)

def process_audio_files(input_folder, output_folder, noise_level=0.01):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            rate, original_data = wav.read(input_path)
            noisy_data = add_gaussian_noise(original_data.astype(np.float32) / 32767.0, noise_level) * 32767.0
            wav.write(output_path, rate, noisy_data.astype(np.int16))


if __name__ == "__main__":
    input_folder = "LJSpeech-1.1/wavs/"
    output_folder = "LJSpeech-1.1/noise/"
    noise_level = 0.01

    process_audio_files(input_folder, output_folder, noise_level)
