import torch
from torchaudio.transforms import Resample
from transformers import Wav2Vec2FeatureExtractor

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained('facebook/wav2vec2-large-xlsr-53') 

def extract_stft(chunk, sample_rate:int, target_sample_rate:int=22050, fixed_length:int = None):
    # Convert the chunk to a PyTorch tensor and add a new axis to match the expected shape
    waveform = torch.from_numpy(chunk).float()
    waveform = waveform.unsqueeze(0)

    if waveform.shape[0] == 2:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != target_sample_rate:
        resampler = Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
        waveform = resampler(waveform)

    wav_stft = torch.stft(
        waveform,
        n_fft=1024,
        window=torch.hamming_window(1024),
        return_complex=True,
        hop_length=256
    ).abs()
    wav_stft = torch.log1p(wav_stft)
    
    if fixed_length:
        if wav_stft.size(-1) < fixed_length:
            padding = fixed_length - wav_stft.size(-1)
            wav_stft = torch.nn.functional.pad(wav_stft, (0, padding))
        else:
            # Truncate
            wav_stft = wav_stft[..., :fixed_length]

    return wav_stft.squeeze(0)

def extract_embedding(chunk, sample_rate:int):
    waveform = torch.from_numpy(chunk).float()
    waveform = waveform.unsqueeze(0)

    if waveform.shape[0] == 2:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sample_rate != 16000:
        resampler = Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    return feature_extractor(waveform, sampling_rate=16000,  return_tensors="np").input_values