def split_waveform(waveform, sample_rate, chunk_duration_ms=500):
    num_samples_per_chunk = int(sample_rate * (chunk_duration_ms / 1000.0))
    total_chunks = len(waveform[0]) // num_samples_per_chunk
    chunks = [waveform[:, i*num_samples_per_chunk:(i+1)*num_samples_per_chunk] for i in range(total_chunks)]

    if len(waveform[0]) % num_samples_per_chunk != 0:
        chunks.append(waveform[:, total_chunks*num_samples_per_chunk:])

    return chunks