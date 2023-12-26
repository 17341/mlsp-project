import unittest
import torch
import sys
from pathlib import Path
import unittest


parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.split_waveform import split_waveform


class TestSplitWaveform(unittest.TestCase):

    def test_chunk_size(self):
        sample_rate = 16000  # 16 kHz
        duration_sec = 1  # 1 second of audio
        num_samples = duration_sec * sample_rate
        waveform = torch.randn(1, num_samples)

        chunk_duration_ms = 200  # 200 milliseconds
        chunks = split_waveform(waveform, sample_rate, chunk_duration_ms)
        
        num_samples_per_chunk = int(sample_rate * (chunk_duration_ms / 1000.0))
        
        for chunk in chunks[:-1]:  # Test all but the last chunk
            self.assertEqual(chunk.shape[1], num_samples_per_chunk)

        # Test the last chunk (it can be less than or equal to the expected size)
        self.assertTrue(chunks[-1].shape[1] <= num_samples_per_chunk)

if __name__ == '__main__':
    unittest.main()
