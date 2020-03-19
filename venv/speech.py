import speech_recognition as sr
import webbrowser as wb
import datetime
from gtts import gTTS
import tkinter
import winsound
#import cv2, time
import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import playsound
from email.message import EmailMessage
import pyowm
import geocoder
import re
import pyautogui
import smtplib
import pygame

output= gTTS(text= "Hello! I'm Alexa, your personal assistant",lang="en-au",slow=False)
output.save("output.mp3")
print("Hello! I'm Alexa, your personal assistant")
playsound.playsound('output.mp3')
os.remove('output.mp3')

def web():
    first_frame = None
    status_list = [None, None]
    times = []
    df = pandas.DataFrame(columns=["Start", "End"])

    video = cv2.VideoCapture(0)

    def screen_short():
        myscreenshot = pyautogui.screenshot()
        myloc = r'C:\Users\nEW u\Pictures\Screenshots'
        fn = str(datetime.datetime.now().timestamp()).split('.')[0] + ".png"
        myscreenshot.save(myloc + '\\' + fn)
        msg = EmailMessage()
        msg['Subject'] = 'Alert! There is an intruder'
        msg['From'] = 'sinhaaditya1@hotmail.com'
        msg['To'] = '1606341@kiit.ac.in'
        msg.set_content('Image attached...')

        with open(myloc + '\\' + fn, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
            print(myloc + '\\' + fn)
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        with smtplib.SMTP('smtp.live.com', 587) as smtp:
            print("c")
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            try:
                smtp.login("sinhaaditya1@hotmail.com", "lxgiwyl123")
                smtp.send_message(msg)
                print("sent")
            except Exception as e:
                print(e)
            smtp.close()
    c = 0
    while True:
        check, frame = video.read()
        status = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        if thresh_frame.sum() > 100:
            print('movement detected')
            if (c == 10):
                screen_short()
                break
            else:
                c = c + 1
        else:
            print('No movement')

        (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            status = 1

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        status_list.append(status)

        status_list = status_list[-2:]

        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.now())

        cv2.imshow("Gray Frame", gray)
        cv2.imshow("Delta Frame", delta_frame)
        cv2.imshow("Threshold Frame", thresh_frame)
        cv2.imshow("Color Frame", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            if status == 1:
                times.append(datetime.now())
            break

    print(status_list)
    print(times)

    for i in range(0, len(times), 2):
        df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)
    df.to_csv("Times.csv")
    video.release()
    cv2.destroyAllWindows

def VoiceRecognition():
    pygame.mixer.init()
    pygame.mixer.music.load(r'C:\Users\nEW u\PycharmProjects\Speech\venv\ping.mp3')
    owm = pyowm.OWM('8a954916f1766a056c995e33ae0e3eac')
    r1 = sr.Recognizer()
    r2 = sr.Recognizer()
    r3 = sr.Recognizer()
    r4 = sr.Recognizer()
    maildict = {'Akshit': '1606172@kiit.ac.in', 'Arunansh': '1606341@kiit.ac.in', 'Aditya': '1606169@kiit.ac.in'}
    condition = 'start'
    tran = re.compile('translate')
    temp = re.compile('temperature')
    loc = re.compile('locate')
    screenshot = re.compile('screenshot')
    mail = re.compile('email')
    play = re.compile('play')
    news = re.compile('news')
    headlines = re.compile('headlines')
    detect= re.compile('motion detector')
    while('stop' not in condition):
        try:
            with sr.Microphone() as source:
                print('speak now')
                audio= r3.listen(source)
                condition= r3.recognize_google(audio)

            if 'Alexa' in condition:
                try:
                    pygame.mixer.music.play()
                except Exception as e:
                    print(e)

                output = gTTS(text="Yes", lang="en-au", slow=False)
                output.save("output.mp3")
                playsound.playsound('output.mp3')
                os.remove('output.mp3')
                r3= sr.Recognizer()
                with sr.Microphone() as source:
                    print('Now listening....')
                    audio= r4.listen(source)
                    try:
                        get= r4.recognize_google(audio)
                        print('You said: '+get)
                        if 'what is your name' in get:
                            output = gTTS(text="You can call me Alexa.", lang="en", slow=False)
                            output.save("output1.mp3")
                            playsound.playsound('output1.mp3')
                            os.remove('output1.mp3')

                        elif temp.search(get)!=None:
                            get = get.split()
                            ind = get.index('temperature')
                            get = get[ind + 2:]
                            city = ""
                            for i in get:
                                city = city + i + " "
                            if city=='':
                                city= 'Bhubaneshwar'
                            try:
                                g = geocoder.ip('me')
                                obs= owm.weather_at_place(city)
                                weather= obs.get_weather()
                                tem= weather.get_temperature('celsius')['temp']
                                tem= str(tem)
                                output = gTTS(text="Right now, the temperature in "+city+" is "+tem+" degrees celsius", lang="en", slow=False)
                                output.save("output.mp3")
                                playsound.playsound('output.mp3')
                                os.remove('output.mp3')
                            except Exception:
                                output = gTTS(text="Sorry. I could not find that",lang="en", slow=False)
                                output.save("output.mp3")
                                playsound.playsound('output.mp3')
                                os.remove('output.mp3')

                        elif loc.search(get)!=None:
                            url= 'https://www.google.co.in/maps/place/'
                            get = get.split()
                            get = get[1:]
                            l=0
                            place = ""
                            for s in get:
                                place = place + s+" "
                            l = len(place)
                            place = place[:l - 1]
                            wb.open_new(url+place)

                        elif screenshot.search(get)!=None:
                            myscreenshot= pyautogui.screenshot()
                            myloc= r'C:\Users\nEW u\PycharmProjects\Speech\venv\Screenshots'
                            fn= str(datetime.datetime.now().timestamp()).split('.')[0]+".png"
                            myscreenshot.save(myloc+'\\'+fn)
                            print("Screenshot taken")
                            output = gTTS(text="Do you want to view the screenshot?",lang="en", slow=False)
                            output.save("output.mp3")
                            playsound.playsound('output.mp3')
                            os.remove('output.mp3')
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                audio = r.listen(source)
                                g = r.recognize_google(audio)
                                if 'yes' in g:
                                    print('Opening file...')
                                    os.startfile(myloc+'\\'+fn)

                        elif mail.search(get)!=None:
                            output = gTTS(text="Who do you want to send the email to?", lang="en", slow=False)
                            output.save("output.mp3")
                            print('Who do you want to send the email to?')
                            playsound.playsound('output.mp3')
                            os.remove('output.mp3')
                            r = sr.Recognizer()
                            with sr.Microphone() as source:
                                audio= r.listen(source)
                                receiver= r.recognize_google(audio)
                                print('You said: '+receiver)
                                print('Sending mail to '+receiver)
                                output = gTTS(text="What is the message?", lang="en", slow=False)
                                output.save("output.mp3")
                                print('What is the message?')
                                playsound.playsound('output.mp3')
                                os.remove('output.mp3')
                                r1 = sr.Recognizer()
                                with sr.Microphone() as source:
                                    aud= r1.listen(source)
                                    message= r1.recognize_google(aud)
                                    print('You said: '+message)
                                    try:
                                        try:
                                            email= smtplib.SMTP('smtp.live.com',587)
                                        except Exception:
                                            print('Connection Failed')
                                        email.ehlo()
                                        email.starttls()
                                        email.ehlo()
                                        try:
                                            email.login('sinhaaditya1@hotmail.com','lxgiwyl123')
                                        except Exception:
                                            print('Login Failed')
                                        if receiver in maildict.keys():
                                            subject= 'Email from Python Assistant'
                                            msg= f'Subject: {subject}\n\n{message}'
                                            print(maildict[receiver])
                                            email.sendmail('sinhaaditya1@hotmail.com',maildict[receiver],msg)
                                        else:
                                            output = gTTS(text="Sorry I could not find "+receiver+" in your address book", lang="en", slow=False)
                                            output.save("output.mp3")
                                            print('Sorry I could not find '+receiver+' in your address book')
                                            playsound.playsound('output.mp3')
                                            os.remove('output.mp3')
                                        output = gTTS(text="Email sent successfully!",lang="en", slow=False)
                                        print("Email sent successfully!")
                                        output.save("output.mp3")
                                        playsound.playsound('output.mp3')
                                        os.remove('output.mp3')
                                    except Exception as e:
                                        print(e)
                                        output = gTTS(text="Sorry. The process could not be completed at this moment.", lang="en", slow=False)
                                        output.save("output.mp3")
                                        playsound.playsound('output.mp3')
                                        os.remove('output.mp3')
                                    email.close()

                        elif play.search(get)!=None:
                            print('You said: '+get)
                            output = gTTS(text="Which song would you like me to play?", lang="en", slow=False)
                            output.save("output.mp3")
                            print('Which song would you like me to play?')
                            playsound.playsound('output.mp3')
                            os.remove('output.mp3')
                            r= sr.Recognizer()
                            with sr.Microphone() as source:
                                audio= r.listen(source)
                                sname= r.recognize_google(audio)
                                query = urllib.parse.quote(sname)
                                url = "https://www.youtube.com/results?search_query=" + query
                                try:
                                    response = urllib.request.urlopen(url)
                                    html = response.read()
                                    soup = BeautifulSoup(html, 'html.parser')
                                    song=""
                                    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}, limit=1):
                                        song= 'https://www.youtube.com' + vid['href']
                                    output = gTTS(text="Alright. Opening youtube.", lang="en", slow=False)
                                    output.save("output.mp3")
                                    print("Alright. Opening youtube...")
                                    playsound.playsound('output.mp3')
                                    os.remove('output.mp3')
                                    wb.open_new(song)
                                except Exception:
                                    output = gTTS(text="Sorry. I could not find that", lang="en", slow=False)
                                    output.save("output.mp3")
                                    print("Sorry. I could not find that")
                                    playsound.playsound('output.mp3')
                                    os.remove('output.mp3')
                        elif news.search(get)!=None or headlines.search(get)!=None:
                            try:
                                output = gTTS(text="Top news headlines from inshorts.com", lang="en", slow=False)
                                print('Alright. Top news headlines from inshorts.com')
                                output.save("output.mp3")
                                playsound.playsound('output.mp3')
                                os.remove('output.mp3')
                                def print_headlines(response_text):
                                    soup = BeautifulSoup(response_text, 'lxml')
                                    headlines = soup.find_all(attrs={"itemprop": "headline"},limit=5)
                                    for headline in headlines:
                                        output = gTTS(text=headline.text, lang="en", slow=False)
                                        print(headline.text)
                                        output.save("output.mp3")
                                        playsound.playsound('output.mp3')
                                        os.remove('output.mp3')

                                url = 'https://inshorts.com/en/read'
                                response = requests.get(url)
                                print_headlines(response.text)
                            except Exception:
                                output = gTTS(text="Sorry. I could not find that", lang="en", slow=False)
                                print('Sorry. I could not find that')
                                output.save("output.mp3")
                                playsound.playsound('output.mp3')
                                os.remove('output.mp3')

                        elif detect.search(get)!=None:
                            output = gTTS(text="Alright. Opening Motion Detector Camera.", lang="en", slow=False)
                            print('Alright. Opening Motion Detector Camera.')
                            output.save("output.mp3")
                            playsound.playsound('output.mp3')
                            os.remove('output.mp3')
                            web()
                        else:
                            output = gTTS(text="Showing search results from Google", lang="en", slow=False)
                            output.save("output.mp3")
                            playsound.playsound('output.mp3')
                            os.remove('output.mp3')
                            url= 'https://www.google.com/search?q='
                            wb.open_new(url+get)

                    except sr.UnknownValueError:
                        print('Could not understand')
                    except sr.RequestError as e:
                        print('failed to get results'.format(e))
        except sr.UnknownValueError:
            print('Could not understand')

VoiceRecognition()