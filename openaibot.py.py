import speech_recognition as sr
import pyttsx3

import os
OPENAI_KEY='Your open ai Key'

from openai import OpenAI
client=OpenAI(
    api_key=OPENAI_KEY
)

def SpeakText(command):
    engine=pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

r=sr.Recognizer()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                # r.adjust_for_ambient_noise(source2,duration=0.2)

                print('I am listening')

                audio2=r.listen(source2)

                MyText=r.recognize_google(audio2)
                return MyText
            
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occured")

def send_to_ChatGPT(messages,model='gpt-3.5-turbo'):
    response=client.completions.create(
        model=model,
        messages=messages,
        
        temperature=0,
    )   
    message=response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages=[{'role':'system','content':"Act like you are HR of ABC company your name is Mr.khanna and you want to recriut someone on the basis of their skills"}]

while(1):
    text=record_text()
    messages.append({'role':'user',"content":text})
    response=send_to_ChatGPT(messages)
    SpeakText(response)

    print(response)
