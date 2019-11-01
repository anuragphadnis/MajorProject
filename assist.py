import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
#import vlc
import urllib 
from urllib.request import urlopen
# import urllib2
import json
from bs4 import BeautifulSoup as soup
#from urllib import urlopen
import wikipedia
import random
from time import strftime
from gtts import gTTS 

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand()
    return command

def sofiaResponse(audio):
    print(audio)
    tts = gTTS(text=audio, lang='en')
    tts.save("audio.mp3")
    os.system('mpg321 audio.mp3 -quiet')
    #for line in audio.splitlines():
    #    os.system("say " + audio)

def assistant(command):
    #---------------------------------------------------------------------
    if 'open reddit' in command:                                         #|
        reg_ex = re.search('open reddit (.*)', command)                  #|
        url = 'https://www.reddit.com/'                                  #|
        if reg_ex:                                                       #|
            subreddit = reg_ex.group(1)                                  #|
            url = url + 'r/' + subreddit                                 #|
        webbrowser.open(url)                                             #|
        sofiaResponse('The Reddit content has been opened for you Sir.') #|
    #---------------------------------------------------------------------|
    #-------------------------------------------------------------------------------------
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            sofiaResponse(domain + 'has been opened for you Sir.')
        else:
            pass
    #--------------------------------------------------------------------------------------
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            sofiaResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
    #-----------------------------------------------------------------------------
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        sofiaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
    #--------------------------------------------------------------------------------
    elif 'change wallpaper' in command:
        folder = '/home/brainiac/Documents/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
        f = urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        urllib.urlretrieve(photo, folder) # Location where we download the image to.
        subprocess.call(["killall Dock"], shell=True)
        sofiaResponse('wallpaper changed successfully')
    #------------------------------------------------------------------------------
    elif 'hello' in command:
        day_time = int(strftime('%H'))
        if day_time < 12:
            sofiaResponse('Hello Sir. Good morning')
        elif 12 <= day_time < 18:
            sofiaResponse('Hello Sir. Good afternoon')
        else:
            sofiaResponse('Hello Sir. Good evening')
    #to terminate the program
    elif 'shutdown' in command:
        sofiaResponse('Bye bye Sir. Have a nice day')
        sys.exit()
while True:
    assistant(myCommand())