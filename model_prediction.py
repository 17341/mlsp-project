from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, Wav2Vec2Tokenizer
import torchaudio
import torch
from bart_prediction import get_prediction, load
import sys
from pydub import AudioSegment
from utils.replace_with_beep import replace_with_beep
import numpy as np
import time
import os
import json
import re

def split_audio_by_silence(audio, silence_info):
    chunks = []

    for i in range(len(silence_info) - 1):
        start_silence, end_silence = silence_info[i]
        chunks.append(audio[0:end_silence])

    return chunks

def remove_cut_ending(audio_stream, model, tokenizer):
    audio_np = np.array(audio_stream.get_array_of_samples())
    waveform = torch.from_numpy(audio_np).unsqueeze(0).float()
    input_values = tokenizer(waveform.squeeze().numpy(), return_tensors="pt").input_values
    with torch.no_grad():
        logits = model(input_values).logits
    res = tokenizer.convert_ids_to_tokens(torch.argmax(logits, dim=-1)[0].cpu().numpy())
    token_time = round(audio_stream.duration_seconds / len(res) * 1000, 1)
    timer = 0
    time = audio_stream.duration_seconds * 1000
    for token in res[::-1]:
        if token == "|":
            time -= timer
            break
        timer += token_time
    return audio_stream[:time]

def transcribe_audio(audio_stream, model, tokenizer):

    audio_np = np.array(audio_stream.get_array_of_samples())
    waveform = torch.from_numpy(audio_np).unsqueeze(0).float()
    #waveform, sampling_rate = torchaudio.load(audio_file_path)
    inputs = tokenizer(waveform.squeeze().numpy(), return_tensors="pt", padding="longest", sampling_rate=16000)

    with torch.no_grad():
        logits = model(inputs.input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)
    if (transcription[0] == ''):
        return ("")
    transcription = transcription[0]
    transcription_sentence_case = transcription[0].upper() + transcription[1:].lower()

    return transcription_sentence_case


def load_models():
    wav2vec2_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    wav2vec2_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    wav2vec2_tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    bart_model, bart_tokenizer = load()
    return wav2vec2_model, wav2vec2_processor, wav2vec2_tokenizer, bart_model, bart_tokenizer


def text_model(words, audio_stream, wav2vec2_model, wav2vec2_processor, wav2vec2_tokenizer, bart_model, bart_tokenizer):
    s = time.time()
    # Can be use to cut the end of the stream if it's not a complete word
    audio_stream = remove_cut_ending(audio_stream, wav2vec2_model, wav2vec2_tokenizer)
    transcription = transcribe_audio(audio_stream, wav2vec2_model, wav2vec2_processor)
    predicted_words = get_prediction(transcription, bart_model, bart_tokenizer)
    # To add a beep on the word
    #if any(word in predicted_words for word in words):
    #    beep_start_time = audio_stream_cut.duration_seconds * 1000
    #    beep_end_time = audio_stream_cut.duration_seconds * 1000 + 500
    #    beep_frequency = 1000
    #    audio_stream_original = replace_with_beep(audio_stream_original, beep_start_time, beep_end_time, beep_frequency)
    results = {
        "audio_words_length": 0,
        "words_to_predict": words,
        "model_prediction": False,
        "time_to_predict": time.time() - s
    }
    results["model_prediction"] = any(word in predicted_words for word in words)
    results["audio_words_length"] = len(transcription.split())
    results["time_to_predict"] = time.time() - s
    return results
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 audio_transcription.py <audio_file_path> <word_list_file>")
        sys.exit(1)
    audio_file_path = sys.argv[1]
    word_list_file = sys.argv[2]
    audio_stream_original = AudioSegment.from_file(audio_file_path, format="wav")
    audio_stream_cut = AudioSegment.from_file(audio_file_path, format="wav")
    with open(word_list_file, 'r') as file:
        words = [line.strip() for line in file]
    wav2vec2_model, wav2vec2_processor, wav2vec2_tokenizer, bart_model, bart_tokenizer = load_models()


    for i in sorted(os.listdir("./LJSpeech-1.1/word/")):
        print(i)
        audio_stream_original = AudioSegment.from_file("./LJSpeech-1.1/wavs/" + i.replace(".txt", ".wav"), format="wav")
        audio_stream_cut = AudioSegment.from_file("./LJSpeech-1.1/wavs/" + i.replace(".txt", ".wav"), format="wav")
        
        with open("./LJSpeech-1.1/word/" + i, 'r') as file:
            text = file.readline()
        word = text
        print(word)
        s = time.time()
        results = {
            "audio_words_length": 0,
            "word_to_predict": word,
            "model_predict": False,
            "time_to_predict": time.time() - s
        }
        transcription = ""
        #for chunk in split_audio(audio_stream_cut, model, tokenizer):
        #    transcription = transcribe_audio(chunk, model, processor)
        #    predicted_word = get_prediction(transcription, ultrafast_model, ultrafast_tokenizer)
        #    if word in predicted_word:
        #        results["model_predict"] = True
        results["audio_words_length"] = len(transcription.split())
        results["time_to_predict"] = time.time() - s
        with open("./exportedData/noise/" + i.replace(".txt", ".json"), 'w') as file:
            json.dump(results, file, indent=4)

