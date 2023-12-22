import os
import json

directory_export = "exportedData/noise"

recapitulatif = {
    "total_audio": 0,
    "total_time": 0.0,
    "15_words_or_less": {
        "nb": 0,
        "average_time": 0.0,
        "ratio_predicted": 0.0
    },
    "more_than_15_words": {
        "nb": 0,
        "average_time": 0.0,
        "ratio_predicted": 0.0
    }
}

for fichier in os.listdir(directory_export):
    if fichier.endswith(".json"):
        chemin_fichier = os.path.join(directory_export, fichier)

        with open(chemin_fichier, "r") as f:
            data = json.load(f)

        recapitulatif["total_audio"] += 1
        recapitulatif["total_time"] += data["time_to_predict"]

        if data["audio_words_length"] <= 15:
            recapitulatif["15_words_or_less"]["nb"] += 1
            recapitulatif["15_words_or_less"]["average_time"] += data["time_to_predict"]
            if data["model_prediction"]:
                recapitulatif["15_words_or_less"]["ratio_predicted"] += 1
        else:
            recapitulatif["more_than_15_words"]["nb"] += 1
            recapitulatif["more_than_15_words"]["average_time"] += data["time_to_predict"]
            if data["model_prediction"]:
                recapitulatif["more_than_15_words"]["ratio_predicted"] += 1

if recapitulatif["total_audio"] > 0:

    if recapitulatif["15_words_or_less"]["nb"] > 0:
        recapitulatif["15_words_or_less"]["average_time"] /= recapitulatif["15_words_or_less"]["nb"]
        recapitulatif["15_words_or_less"]["ratio_predicted"] /= recapitulatif["15_words_or_less"]["nb"]

    if recapitulatif["more_than_15_words"]["nb"] > 0:
        recapitulatif["more_than_15_words"]["average_time"] /= recapitulatif["more_than_15_words"]["nb"]
        recapitulatif["more_than_15_words"]["ratio_predicted"] /= recapitulatif["more_than_15_words"]["nb"]

exportedFileName = "analyses_noise_prediction.json"

with open("./exportedData/" + exportedFileName, "w") as f_recap:
    json.dump(recapitulatif, f_recap, indent=2)

print("Récapitulatif des analyses créé avec succès. Fichier './exportedData/" + exportedFileName + "'")
