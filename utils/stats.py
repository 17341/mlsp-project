from pydub import AudioSegment
import os
import glob
import statistics
import pandas as pd

word_directory = "data/words"
word_folders = [f for f in glob.glob(os.path.join(word_directory, "*")) if os.path.isdir(f)]

all_stats = []

for folder in word_folders:
    word = os.path.basename(folder)
    wav_files = glob.glob(os.path.join(folder, "*.wav"))
    
    durations = []
    
    for wav_file in wav_files:
        try:
            audio = AudioSegment.from_wav(wav_file)
            durations.append(len(audio) / 1000) 
        except Exception as e:
            print(f"Error processing {wav_file}: {e}")

    if durations:
        word_stats = {
            "Word": word,
            "Occurrences": len(wav_files),
            "Total Time": sum(durations),
            "Average Time": statistics.mean(durations),
            "Max Time": max(durations),
            "Min Time": min(durations),
            "Time Variance": statistics.variance(durations) if len(durations) > 1 else 0
        }
    else:
        word_stats = {key: 0 for key in ["Word", "Occurrences", "Total Time", "Average Time", "Max Time", "Min Time", "Time Variance"]}
        word_stats["Word"] = word

    all_stats.append(word_stats)

df = pd.DataFrame(all_stats)
csv_file = "word_statistics.csv"
try:
    df.to_csv(csv_file, index=False)
    print(f"Statistics written to {csv_file}")
except Exception as e:
    print(f"Failed to write CSV: {e}")