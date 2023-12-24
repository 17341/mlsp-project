# mlsp-project

Dans le cadre de ce projet, nous développerons un modèle de traitement audio innovant visant à détecter des mots spécifiques dans un flux audio en temps réel. Le modèle sera conçu pour accepter des mots en entrée, qu'ils soient fournis ou non. sous forme de texte ou contenu dans de courts fichiers audio. Notre objectif principal est de créer une application permettant aux utilisateurs écouter un flux audio depuis son ordinateur pendant la capture les mots spécifiés en entrée. Pour nos expériences, nous envisageons de Commencez par utiliser un ensemble de données spécifique. Contrairement à certaines solutions existantes, notre modèle se concentrera sur le traitement direct du signal audio, évitant ainsi sa transcription en texte. Nous espérons donc obtenir des résultats expérimentaux démontrant la capacité de notre modèle à détecter efficacement des mots spécifiques dans un flux audio en direct. Nous chercherons à améliorer sa précision et sa réactivité à différentes personnes et bruits de fond. A ce titre, la méthode décrite ici décrit une étape de notre réflexion dans notre volonté de résoudre au mieux ce problème.

# Méthode basée sur une comparaison entre des mots donnés à l'oral par l'utilisateur et des "fenêtres audio" successives d'une seconde à l'aide d'un calcul de similarité cosinus

## Evaluations et présentation des résultats

Le flux audio provenant du microphone est analysé de manière continue et est divisé en "fenêtres audio" d'une seconde chacune. En conséquence de cela, plusieurs "0" font leur apparition dans les structures de données qui représentent chaque fenêtre. En effet, une telle méthode ne garantit pas une analyse complète d'un mot dans son entièreté (depuis son début jusqu'à sà fin). Le mot peut être en fait coupé et des temps morts s'ajouter dans nos structures de données.

Ci-dessous sont donc présentés des résultats sans puis avec un ajout de la moyenne de chaque fenêtre à elle-même.
Ils se présentent de cette manière : % de mots ayant été définis par l'utilisateur et ayant été bien censurés, % de mots ayant été définis par l'utilisateur et n'ayant pas été censurés et % de mots ayant été ayant été censurés alors qu'ils ne devaient pas l'être.

### Résultats sans ajouter la moyenne des audios embeddings sur ces derniers

4%/44.5%/0%

### Résultats en ajoutant la moyenne

3.5%/39%/2.5%

## Commentaires

Globalement, les résultats ne sont pas significativement différents. Cependant, on peut conjecturer le fait que le calcul de similarité cosinus est plus sensible à des données qui contiennent moins de valeurs nulles par rapport à d'autres. Cela se trauduit par le fait qu'avec des données auxquelles on a ajouté une moyenne le modèle va (malgré une censure des mots non nécessaire) globalement en "raté" moins.

(Le résultat des tests présenté ci-dessus a été obtenu de manière expérimentale)
