from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import speech_recognition as sr
import pyttsx3


r=sr.Recognizer()

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def chat(user_input):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)
    bot_input = {"input_ids": input_ids}
    chat_response = model.generate(**bot_input, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    bot_output = tokenizer.decode(chat_response[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_output

def SpeakText(commnad):
    engine=pyttsx3.init()
    rate=engine.getProperty('rate')
    engine.setProperty('rate',rate)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say(commnad)
    engine.runAndWait()




# while True:
#     user_input = input("User: ")
#     if user_input.lower() == "bye":
#         print("Bot: Goodbye! Take care. 🤗")
#         break
#     bot_response = chat(user_input)
#     print("Bot:", bot_response)


while(True):

    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2,duration=.4)

            audio=r.listen(source2)

            MyText=r.recognize_google(audio_data=audio)
            MyText=MyText.lower()
            if MyText=='bye':
                SpeakText('Goodbye Sir')
                break
            bot_response=chat(MyText)

            print("Your question:",MyText)
            SpeakText(bot_response)
            print("Bot:",bot_response)
    
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occured")