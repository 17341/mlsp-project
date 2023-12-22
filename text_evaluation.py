import os
from pydub import AudioSegment
import time
import json
from model_prediction import text_model, load_models

if __name__ == "__main__":
    wav2vec2_model, wav2vec2_processor, wav2vec2_tokenizer, bart_model, bart_tokenizer = load_models()

    for i in sorted(os.listdir("./LJSpeech-1.1/word/")):
        print(i)
        audio_stream = AudioSegment.from_file("./LJSpeech-1.1/noise/" + i.replace(".txt", ".wav"), format="wav")
        
        with open("./LJSpeech-1.1/word/" + i, 'r') as file:
            text = file.readline()
        with open("./data/alignments/" + i.replace(".txt", ".json"), 'r') as file:
            data = json.load(file)
        s = time.time()
        results = {
            "audio_words_length": 0,
            "words_to_predict": text,
            "model_prediction": False,
            "time_to_predict": time.time() - s
        }
        for word in data["words"]:
            if "end" in word and word["end"] >= 0.1:
                t = int(word["end"] * 1000)
                res = text_model([text], audio_stream[:t], wav2vec2_model, wav2vec2_processor, wav2vec2_tokenizer, bart_model, bart_tokenizer)
                if res["model_prediction"]:
                    results["model_prediction"] = True
        results["audio_words_length"] = len(data["words"])
        results["time_to_predict"] = time.time() - s
        with open("./exportedData/noise/" + i.replace(".txt", ".json"), 'w') as file:
            json.dump(results, file, indent=4)