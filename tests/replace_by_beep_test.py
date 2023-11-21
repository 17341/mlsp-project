import unittest
from pydub import AudioSegment
import sys
from pathlib import Path

# Adjust the path to include the directory where your utils package is located
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.replace_with_beep import replace_with_beep

class TestReplaceWithBeep(unittest.TestCase):

    def setUp(self):
        # Setup code: Load the audio file you want to test with
        self.input_audio = AudioSegment.from_file(f"{parent_dir}/data/example1.wav")

    def test_replace_with_beep(self):
        output_audio = replace_with_beep(self.input_audio, 5000, 6000)
        self.assertIsNotNone(output_audio)
        self.assertEqual(len(output_audio), len(self.input_audio))
        if output_audio is not None:
            output_audio.export(
                f"{parent_dir}\\data\\output\\replace_with_beep_test.wav", format="wav")

if __name__ == '__main__':
    unittest.main()
