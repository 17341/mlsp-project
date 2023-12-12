#Facebook's Wav2Vec2

#The base model pretrained and fine-tuned on 960 hours of Librispeech on 16kHz sampled speech audio.
#When using the model make sure that your speech input is also sampled at 16Khz.

import torch
from scipy import spatial
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
import speech_recognition as sr
import io
from pydub import AudioSegment
import numpy
from numpy import dot
from numpy.linalg import norm
from datasets import load_dataset
from sklearn.model_selection import train_test_split

tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# --------------- train model with added noise ----------------------------------------------------------
#dataset = load_dataset('LJSpeech-1.1/LJSpeech-1.1/wavs')['train']
#dataset.shuffle()
#noise = np.random.normal(-0.5*min(dataset[i]['audio']['array']),0.5*max(dataset[i]['audio']['array']),len(dataset[i]['audio']['array']))

#tokenized_datasets = tokenizer([dataset['train'][i]['audio']['array'] for i in range(1000)])
#tensors_audios = [torch.FloatTensor(dataset[i]['audio']['array']) for i in range(0,1000)]

#X_train, X_valid, y_train, y_valid = train_test_split(tokenized_datasets, full_y_train, test_size=0.1, random_state=42)

#vectorizer = CountVectorizer(lowercase=True)
#full_X_train = vectorizer.fit_transform(training_corpus.data)
#full_y_train = training_corpus.target

# On le divise en données d'entraînement et de validation
#X_train, X_valid, y_train, y_valid = train_test_split(full_X_train, full_y_train, test_size=0.1, random_state=42)
# ------------------------------------------- training -------------------------------------------------

#EleutherAI = 'EleutherAI/gpt-neo-125M'
#fb="facebook/opt-350m"
#generator = pipeline('text-generation', model=fb)

r = sr.Recognizer()
m = sr.Microphone(sample_rate=16000)

number_of_words_to_ban = int(input("Enter the number of words you want to ban : "))
banned_words_tensors = []

while number_of_words_to_ban != 0:
    print("Please say out loud the word that you want to ban")
    with m as source:
        audio = r.listen(source) #pyaudio object
        data = io.BytesIO(audio.get_wav_data())  # list of bytes
        clip = AudioSegment.from_file(data)  # numpy array
        x = torch.FloatTensor(clip.get_array_of_samples()[:15360])  # tensor
        inputs = tokenizer(x, sampling_rate=16000, return_tensors='pt', padding='longest').input_values
        logits = model(inputs).logits
        tokens = torch.argmax(logits, axis=-1)
        words = str(tokenizer.batch_decode(tokens)[0]).lower()

        if words != '':
            print('You said : ', words, 'is this correct ?')
            res = input("Yes(y) No(n) : ")
            if res == 'y':
                mean = numpy.mean(tokens[0].numpy())
                #var = numpy.var(tokens[0].numpy())
                #banned_words_tensors.append((tokens[0].numpy()+mean)/var)
                banned_words_tensors.append(tokens[0].numpy()+mean)
                number_of_words_to_ban -= 1
            elif res == 'n':
                pass
            else:
                print("incorrect value, try again please")

def compare_words_chunks(inputs):
    for i in range(0,len(banned_words_tensors)):
        res = 1 - spatial.distance.cosine(inputs, banned_words_tensors[i])
        print(res)
        if res >= 0.5:
            #make some noise
            print("BAD WORD DETECTED !!!!!!")
        else:
            print("all good")

with m as source:

    print('You can speak now...')
    while True:
        audio = r.record(source,duration=1) #pyaudio object
        data = io.BytesIO(audio.get_wav_data()) #list of bytes
        clip = AudioSegment.from_file(data) #numpy array
        x = torch.FloatTensor(clip.get_array_of_samples()) #tensor
        inputs = tokenizer(x, sampling_rate=16000,return_tensors='pt', padding='longest').input_values
        logits = model(inputs).logits
        tokens = torch.argmax(logits, axis=-1)
        words = str(tokenizer.batch_decode(tokens)[0]).lower()

        if words != '':
            #var = numpy.var(tokens[0].numpy())
            #compare_words_chunks((tokens[0].numpy()+numpy.mean(tokens[0].numpy()))/var)
            compare_words_chunks(tokens[0].numpy()+numpy.mean(tokens[0].numpy()))

            print('\n','Here\'s what has been captured : ',words)
            #generated_text = generator(words, min_length=20)
            #predictions = generator(words)[0]['generated_text']
            #print("here's what's next : ",predictions)
