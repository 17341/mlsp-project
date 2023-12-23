# mlsp-project
 Dans le cadre de ce projet, nous développerons un modèle de traitement audio innovant visant à détecter des mots spécifiques dans un flux audio en temps réel. Le modèle sera conçu pour accepter des mots en entrée, qu'ils soient fournis ou non. sous forme de texte ou contenu dans de courts fichiers audio. Notre objectif principal est de créer une application permettant aux utilisateurs écouter un flux audio depuis son ordinateur pendant la capture les mots spécifiés en entrée. Pour nos expériences, nous envisageons de Commencez par utiliser un ensemble de données spécifique. Contrairement à certaines solutions existantes, notre modèle se concentrera sur le traitement direct du signal audio, évitant ainsi sa transcription en texte. Nous espérons donc obtenir des résultats expérimentaux démontrant la capacité de notre modèle à détecter efficacement des mots spécifiques dans un flux audio en direct. Nous chercherons à améliorer sa précision et sa réactivité à différentes personnes et bruits de fond.


# Méthode basée sur une comparaison de fenêtres audios entre des mots ayant été renseignés à l'oral par l'utilisateur et un flux audio constant d'une seconde
## La comparaison entre les fenêtres s'effectue à l'aide d'un calcul de similarité cosinus

### Résultats

#BAG BOOK WHICH 50 Atempts -> 1/23/0 (sans means added sur les tensors pour pallier aux nombreux zéros recorded)
#TRAIN SKY FIRE 100 Atempts -> 6/43/0 (sans means added sur les tensors pour pallier aux nombreux zéros recorded)
#------------------------Résultats sans ajouter la moyenne des audios embeddings sur ces derniers------------------------
#8/89/0 ---> 4%/44.5%/0%

#PAIN GLASS CARD 50 Atempts -> 1/18/1 (means added sur les tensors pour pallier aux nombreux zéros recorded) dot and norm
#BED MOUSE GAME 100 Atempts -> 5/42/3 (means added sur les tensors pour pallier aux nombreux zéros recorded) dot and norm
#------------------------Résultats en ajoutant la moyenne------------------------
#7/78/5 ---> 3.5%/39%/2.5%
