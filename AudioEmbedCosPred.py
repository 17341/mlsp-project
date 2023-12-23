#Facebook's Wav2Vec2
#The base model pretrained and fine-tuned on 960 hours of Librispeech on 16kHz sampled speech audio.
#When using the model make sure that your speech input is also sampled at 16Khz.

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import speech_recognition as sr
import io
from pydub import AudioSegment
import numpy as np

tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

r = sr.Recognizer()
m = sr.Microphone(sample_rate=16000)

number_of_words_to_ban = int(input("Enter the number of words you want to ban : "))
banned_words_tensors = []
banned_words_str = []

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
            res = input("Yes(y)/No(n) : ")
            if res == 'y':
                mean = np.mean(tokens[0].numpy())
                #banned_words_tensors.append(tokens[0].numpy()+mean)
                banned_words_tensors.append(tokens[0].numpy())
                banned_words_str.append(words)
                number_of_words_to_ban -= 1
            elif res == 'n':
                pass
            else:
                print("incorrect value, try again please")


number_of_good_strikes = 0
number_of_miss_strikes = 0
number_of_bad_strikes = 0
nothing = 0
counter = 100
def compare_words_chunks(inputs,words):

    global number_of_good_strikes
    global number_of_miss_strikes
    global number_of_bad_strikes
    global nothing
    global counter

    for i in range(0,len(banned_words_tensors)):
        res = np.dot(inputs,banned_words_tensors[i]) / (np.linalg.norm(inputs) * np.linalg.norm(banned_words_tensors[i]))

        if res >= 0.5:

            if words in banned_words_str:
                #make some noise
                print("the value of the cosine similarity equals ",res)
                print("BAD WORD DETECTED !")
                number_of_good_strikes += 1
                print("the number of good strike(s) equals ", number_of_good_strikes)
                break

            elif words not in banned_words_str:
                print("the value of the cosine similarity equals ", res)
                number_of_bad_strikes += 1
                print("BAD WORD DETECTED but this word should not have been detected. The number of bad strike(s) equals ", number_of_bad_strikes)
                break

        else:
            if words in banned_words_str:
                print("the value of the cosine similarity equals ", res)
                number_of_miss_strikes += 1
                print("This word should have been striked, the number of strikes that have been missed equals ",number_of_miss_strikes)
                break
            else:
                print("all good")
                nothing+=1
                break

    counter -= 1
    print("the counter is equal to ", counter)

with m as source:
    #r.adjust_for_ambient_noise(source)
    print('You can speak now...','\n')
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
            print('\n','Here\'s what has been captured : ', words)
            #compare_words_chunks(tokens[0].numpy()+np.mean(tokens[0].numpy()),words)
            compare_words_chunks(tokens[0].numpy(),words)

            if counter == 0:
                print("End of the evaluation")
                break

print(number_of_good_strikes,number_of_miss_strikes,number_of_bad_strikes,nothing,sep='\n')
