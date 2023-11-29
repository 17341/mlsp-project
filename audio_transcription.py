from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import torch
from word_prediction import get_prediction
import sys

def transcribe_audio(audio_file_path):
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

    waveform, sampling_rate = torchaudio.load(audio_file_path)
    inputs = tokenizer(waveform.squeeze().numpy(), return_tensors="pt", padding="longest")

    with torch.no_grad():
        logits = model(inputs.input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]

    transcription_sentence_case = transcription[0].upper() + transcription[1:].lower()

    return transcription_sentence_case

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 audio_transcription.py <audio_file_path> <word_list_file>")
        sys.exit(1)

    audio_file_path = sys.argv[1]
    with open(sys.argv[2], 'r') as file:
        word_list = [line.strip() for line in file]

    transcription = transcribe_audio(audio_file_path)
    predicted_word = get_prediction(transcription)
    print("Transcription:", transcription)
    print("Word:", predicted_word)
    print("Word need to be bip:", predicted_word in word_list)
