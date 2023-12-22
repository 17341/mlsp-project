# MLSP-Project
 Dans le cadre de ce projet, nous développerons un modèle de traitement audio innovant visant à détecter des mots spécifiques dans un flux audio en temps réel réel. Le modèle sera conçu pour accepter des mots en entrée, qu'ils soient fournis ou non. sous forme de texte ou contenu dans de courts fichiers audio. Notre objectif principal est de créer une application permettant aux utilisateurs écouter un flux audio depuis son ordinateur pendant la capture les mots spécifiés en entrée. Pour nos expériences, nous envisageons de Commencez par utiliser un ensemble de données spécifique. Contrairement à certaines solutions existantes, notre modèle se concentrera sur le traitement direct du signal audio, évitant ainsi sa transcription en texte. Nous espérons donc obtenir des résultats expérimentaux démontrant la capacité de notre modèle pour détecter efficacement des mots spécifiques dans un flux audio en direct. Nous chercherons à améliorer sa précision, sa réactivité à différentes personnes et bruits de fond.

## Prédiction de texte
### Modèles utilisés
Ce projet utilise les modèles suivants pour différentes tâches liées à l'audio et à la transcription :

#### 1. Wav2Vec2
Modèle : [facebook/wav2vec2-base-960h](https://huggingface.co/facebook/wav2vec2-base-960h)  
Processor : facebook/wav2vec2-base-960h  
Tokenizer : facebook/wav2vec2-base-960h  
Description : Ce modèle est utilisé pour la transcription audio en texte.  
#### 2. BART
Modèle : [facebook/bart-large](https://huggingface.co/facebook/bart-large)  
Tokenizer : facebook/bart-large  
Description : Ce modèle est utilisé pour la prédiction de mots basée sur la transcription audio. 

#### 3. UltraFastBERT - Plus utilisé
Modèle : [pbelcak/UltraFastBERT-1x11-long](https://huggingface.co/pbelcak/UltraFastBERT-1x11-long)  
Tokenizer : pbelcak/UltraFastBERT-1x11-long  
Description : Ce modèle est utilisé pour la prédiction de mots basée sur la transcription audio, il est sorti en fin 2023 et est bien plus rapide en utilisant que 0.3% des neurones de BERT. Nous avons décidé de ne finalement plus l'utilisé à cause des résulats peu satisfaisants mais nous tenions à en parler. Il est disponible dans le dossier [UltraFastBERT](./UltraFastBERT/)

### Fonctionnement
Le code est composé de plusieurs fichiers :

#### 1. [add_noise.py](./add_noise.py)
Ce script ajoute un bruit gaussien à des fichiers audio WAV, ce qui va permettre de tester le modèle avec du bruit.
Il prend en entrée un dossier d'origine, ajoute du bruit aux fichiers audio qu'il contient, et enregistre les résultats dans un nouveau dossier.
#### 2. [model_prediction.py](./model_prediction.py)
Ce script est le corps principal du modèle, il déclare le modèle Wav2Vec2, il récupère supprime le dernier mot si celui si est pas complet, il transcrit le stream audio et prédit le prochain mot, et pour finir renvoie un objet avec les résultats.
#### 3. [bart_prediction.py](./bart_prediction.py)
Ce script contient des fonctions pour charger et utiliser le modèle BART.
Il offre une fonction pour obtenir des prédictions de mots basées sur un texte donné.
#### 4. [ultrafast_prediction.py](./ultrafast_prediction.py)
Ce script contient des fonctions pour charger et utiliser le modèle UltraFastBERT.
Il offre une fonction pour obtenir des prédictions de mots basées sur un texte donné.
Ce modèle n'est plus utilisé dans le corps du modèle.

### Evaluation
L'évaluation est composé de plusieurs fichiers :

#### 1. [text_evaluation.py](./text_evaluation.py)
Ce script évalue les performances de la prédiction de texte en testant le modèle sur 100 audio différents puis pour chaque audio il génère un fichier JSON avec le nombre de mots dans l'audio, les mots à prédire, si le modèle à prédit le mot dans l'audio et le temps que ça lui a pris.
#### 2. [evaluation_prediction.py](./evaluation_prediction.py)
Ce script effectue permet de faire un récapitulatif des fichiers JSON générés précedemment pour en sortir le nombre d'audios, le temps total en secondes, puis les recapitulatifs pour 15 mots et moins et pour plus de 15 mots, du nombre de mots, du temps moyen et du ratio de mots prédis.

Le dossier [exportedData](./exportedData/) contient les résultats de l'évaluation, notamment les fichier [analyses_noise_prediction.json](./analyses_noise_prediction.json) et [analyses_prediction.json](./analyses_prediction.json). Ce fichier récapitule les performances du modèle sur l'ensemble des données, fournissant des informations sur la durée moyenne de prédiction, le ratio de prédictions correctes, etc.

Pour utiliser ces scripts, assurez-vous d'avoir installé les dépendances nécessaires spécifiées dans les fichiers. Vous pouvez ajuster les paramètres selon vos besoins, tels que le niveau de bruit ajouté ou les modèles utilisés.
