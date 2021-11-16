import nltk
from nltk.corpus import wordnet
from PyDictionary.test_pydictionary import dictionary
from random import randint
import speech_recognition as sr
from pyaudio import *
import pyttsx3 as p
import os
import re

#'''''''''''''''
r = sr.Recognizer()
engine = p.init()
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', en_voice_id)
engine.setProperty('rate', 130)
def speak(audio):
    print(f"{audio}")
    engine.say(audio)
    engine.runAndWait()
    
def randomword():
    s=''
    with open('dictionary.txt') as f:
        s = f.readlines()
    s=''.join(s)
    dic=s.split(',')
    t=True
    while t:
        p=dic[randint(0,len(dic))]
        sn=wordnet.synsets(p)
        if len(sn)!=0:
        # print(p,':',sn[0].definition())
            synonym=set()
            antonym=set()
            for syn in wordnet.synsets(p):
                for l in syn.lemmas():
                    synonym.add(l.name())
                    if l.antonyms():
                        antonym.add(l.antonyms()[0].name())
            # print('synonyms: ',list(set(synonym)))
            # print('antonyms: ',list(antonym))
            # print('example: ',sn[0].examples())
            t=False
    parts=[]
    synonym=list(synonym)
    antonym=list(antonym)
    for m,pos in dictionary.meaning(p).items():
        parts.append({m:pos[0]})
    for i in range(len(synonym)):
        synonym[i]=re.sub('[^a-z]',' ',synonym[i].lower())
    for i in range(len(antonym)):
        antonym[i]=re.sub('[^a-z]',' ',antonym[i].lower())
    resultword={
    'Word':p,
    'parts of speech':parts,
    'example':sn[0].examples(),
    'synonyms':list(set(synonym)),
    'antonyms':list(set(antonym))
    }
    return resultword
rand_word=randomword()
for dat,value in rand_word.items():
    if dat=='Word':
        speak("Word of the Day is {}".format(value))
        k=value
    elif dat=='parts of speech':
        speak("{} of {} ".format(dat,k))
        for i in value:
            for pos,mea in i.items():
                speak("{} meaning is {} ".format(pos,mea))
    elif len(value)!=0:
        speak("{} of {} is {} ".format(dat,k,value))
    
    
