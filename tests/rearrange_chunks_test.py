import unittest
import sys
from pathlib import Path
from pydub import AudioSegment

parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.rearrange_chunks import rearrange_chunks

class TestRearrangeChunks(unittest.TestCase):

    def setUp(self):
        self.segment1 = AudioSegment.from_file(f"{parent_dir}/data/example1.wav")
        self.segment2 = AudioSegment.from_file(f"{parent_dir}/data/example1.wav")
        self.segments = [
            {'start_time': 0, 'end_time': 2000, 'audio_segment': self.segment1},
            {'start_time': 2000, 'end_time': 10000, 'audio_segment': self.segment2}
        ]

    def test_rearrange_chunks(self):
        combined_audio = rearrange_chunks(self.segments)

        # Assertions
        self.assertIsNotNone(combined_audio)
        self.assertTrue(len(combined_audio) > 0)
        combined_audio.export(f"{parent_dir}\data\output\combined_audio_test.wav", format="wav")

if __name__ == '__main__':
    unittest.main()
