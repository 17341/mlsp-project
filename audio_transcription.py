from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import torch
from word_prediction import get_prediction
import sys
from pydub import AudioSegment
from utils.replace_with_beep import replace_with_beep
import numpy as np

def split_waveform(waveform, sample_rate, chunk_duration_ms=200):
    num_samples_per_chunk = int(sample_rate * (chunk_duration_ms / 1000.0))
    total_chunks = len(waveform[0]) // num_samples_per_chunk
    chunks = [waveform[:, i*num_samples_per_chunk:(i+1)*num_samples_per_chunk] for i in range(total_chunks)]
 
    if len(waveform[0]) % num_samples_per_chunk != 0:
        chunks.append(waveform[:, total_chunks*num_samples_per_chunk:])
 
    return chunks

def split_audio(audio_stream, chunk_duration_ms):
    chunks = []

    while chunk_duration_ms < len(audio_stream):
        end_time = min(chunk_duration_ms, len(audio_stream))
        chunk = audio_stream[:end_time]
        chunks.append(chunk)
        chunk_duration_ms += 500 
        t = "test/final_audio"
        t += str(chunk_duration_ms)
        t += ".wav"
    return chunks

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

def check_audio(audio_stream_cut, audio_stream_original, word_list, model, tokenizer):
    transcription = transcribe_audio(audio_stream_cut, model, tokenizer)
    if (transcription == ""):
        return audio_stream_original
    predicted_word = get_prediction(transcription)
    print("Transcription:", transcription)
    print("Word:", predicted_word)
    print("Word need to be bip:", predicted_word in word_list)

    if predicted_word in word_list:
        beep_start_time = audio_stream_cut.duration_seconds * 1000
        print(beep_start_time)
        beep_end_time = audio_stream_cut.duration_seconds * 1000 + 500
        beep_frequency = 1000
        audio_stream_original = replace_with_beep(audio_stream_original, beep_start_time, beep_end_time, beep_frequency)

    return audio_stream_original


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 audio_transcription.py <audio_file_path> <word_list_file>")
        sys.exit(1)
    audio_file_path = sys.argv[1]
    word_list_file = sys.argv[2]
    audio_stream_original = AudioSegment.from_file(audio_file_path, format="wav")
    audio_stream_cut = AudioSegment.from_file(audio_file_path, format="wav")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")


    with open(word_list_file, 'r') as file:
        word_list = [line.strip() for line in file]

    for chunk in split_audio(audio_stream_cut, 500):
        audio_stream_original = check_audio(chunk, audio_stream_original, word_list, model, tokenizer)


    #audio_stream_original = check_audio(audio_stream_cut, audio_stream_original, word_list, model, tokenizer)
    audio_stream_original.export("final_audio.wav", format="wav")
