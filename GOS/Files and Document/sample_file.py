import tkinter as tk
import tkinter.messagebox
import threading
from PIL import Image, ImageTk

from tkinter import *
from tkinter import ttk
#from commands import MainView
from tkinter.ttk import Progressbar
from PIL import Image
w = Tk()

width_of_window = 527
height_of_window = 350
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width / 2) - (width_of_window / 2)
y_coordinate = (screen_height / 2) - (height_of_window / 2)
w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

w.overrideredirect(1)
photo = PhotoImage(file = "bacgroundsplash.png")
#button = PhotoImage(file = "button.png")
#photoimage = button.subsample(11, 12)
label=Label(w, image=photo).pack()

s = ttk.Style()
s.theme_use('alt')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='#4f4f4f')
progress = Progressbar(w, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=560, mode='determinate')


def bar():
    l4 = Label(w, text='Loading...', fg='white', bg=a)
    lst4 = ('Calibri (Body)', 10)
    l4.config(font=lst4)
    l4.place(x=18, y=310)

    import time
    r = 0
    for i in range(100):
        progress['value'] = r
        w.update_idletasks()
        time.sleep(0.03)
        r = r + 1

    w.destroy()


progress.place(x=-10, y=345)

a = '#6fdc8d'
#Frame(w, width=527, height=341, bg=a).place(x=0, y=0)  # 249794
b1 = Button(w,text='Get Started',
            command=bar, border=0, fg='black',
            font=('bold',8),
            activebackground='#345',activeforeground='red',cursor='hand2')
b1.place(x=230, y=300)


w.mainloop()




root = tk.Tk()

w = 440
h = 550

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title("Virtual Assistant")
#root.overrideredirect(True)
root.config(bg="#249794")
root.iconbitmap("speak-modified.ico")
############################################################################################################################

import datetime
import pickle
import os.path
import shutil
import webbrowser
import sounddevice as sd
#import soundfile as sf
import pyowm
from rom import query
import pyautogui as pg
import pyperclip
import requests
import wolframalpha
from bs4 import BeautifulSoup
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import urllib.request
import urllib.parse
import re
import pyttsx3.drivers.sapi5
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from commands import
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
#from ttkbootstrap import Style
#from pycamera import camera


calendarscope = ['https://www.googleapis.com/auth/calendar']
gmailscope = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIOS = ["rd", "th", "st"]


email_id = "19it34rajesh@mailamengg.com"
email_id_password = "190037@mec"

city = "Villupuram"
startmin = int(datetime.datetime.now().hour)



# For check wheather an internet connection exists or not
def is_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=1)
        return True
    except urllib.request.URLError:
        return False


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# For audio from text input
def speak(text):
    #engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    #animation(count)


# For text from audio input
def get_audio(status_bar=None,status_bar1=None):
    r = sr.Recognizer()
    said = ""
    try:
        with sr.Microphone() as source:
            #print("Please wait. Calibrating your microphone...")
            if status_bar:
                status_bar["text"] = "Please wait. preparing..."
            # listen for 1 seconds and create the ambient noise energy level
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 1
            # Listen from audio source
            #print("Listening...")
            if status_bar:
                status_bar["text"] = "Listening..."
            audio = r.listen(source)
            try:
                said = r.recognize_google(audio)
                """
                word = said

                def go(counter=1):
                    status_bar["text"].config(text=word[:counter])
                    if counter < len(word):
                        root.after(150, lambda: go(counter + 1))
                        """
                #print("You say: " + said)
                if status_bar:
                    status_bar["text"] = "You say: " + said

                sentence = text

                sid_obj = SentimentIntensityAnalyzer()

                sentiment_dict = sid_obj.polarity_scores(sentence)

                string = str(sentiment_dict['neg'] * 100) + "% Negative"
                string = str(sentiment_dict['neu'] * 100) + "% Neutral"
                string = str(sentiment_dict['pos'] * 100) + "% Positive"
                if sentiment_dict['compound'] >= 0.05:
                    string = "Positive"

                    status_bar1['text'] = "Positive"

                elif sentiment_dict['compound'] <= - 0.05:
                    string = "Negative"

                    status_bar1['text'] = "Negative"


                else:
                    string = "Neutral"

                    status_bar1['text'] = "Neutral"

                #print(string)
                #print(text)
                status_bar1['text']=string

            except LookupError as err:
                #print("Opps! could not understand audio: " + str(err))
                if status_bar:
                    status_bar["text"] = "Opps! could not understand audio: " + str(err)
    except:
        pass

    return said


# For google calendar authentication service


# For events from google calendar
def get_events(date, service, status_bar=None):
    # Call the Calendar API
    start_date = datetime.datetime.combine(date, datetime.datetime.min.time())  # Ex. 2019-11-07 00:00:00
    end_date = datetime.datetime.combine(date, datetime.datetime.max.time())  # Ex. 2019-11-07 23:59:59.999999

    events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat() + 'Z',
                                          timeMax=end_date.isoformat() + 'Z', singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('Sorry, You have no upcoming events on this day.')
        if status_bar:
            status_bar["text"] = "Sorry, You have no upcoming events on this day."

    else:
        event_num = len(events)
        if event_num > 1:
            speak(f"You have {event_num} events, on this day.")
            print("Your events are:")
        else:
            speak(f"You have only {event_num} event, on this day.")
            print("Your event is:")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])

            if int(start_time.split(":")[0]) < 12:
                start_time = start_time.split(":")[0] + ":" + start_time.split(":")[1]
                start_time += "am"
                print(start_time)
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + ":" + start_time.split(":")[1]
                start_time += "pm"
                print(start_time)

            speak(event['summary'] + ", at " + start_time)


# For a date that contains in a string
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIOS:
                found = word.find(ext)  # ex. 12th
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year += 1
    if day < today.day and day != -1 and month == -1:
        month += month
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # 0-6
        diff = day_of_week - current_day_of_week

        if diff < 0:
            diff += 7
            if text.count("next") >= 1:
                diff += 7

        return today + datetime.timedelta(diff)  # Ex. 2019-11-07 + 7 days, 0:00:00

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)



def read():
    pg.hotkey("ctrl", 'c')
    tobespoken = pyperclip.paste()
    speak(tobespoken)


def openafile():
    query = text.split("play")
    speak(f"searching for {query[1]} in my database")
    dir_path = os.path.dirname(os.path.realpath(__file__))

    try:
        for root, dirs, files in os.walk("G:\\VCS\\music"):
            for file in files:
                file_name = query[1]
                if file.startswith(file_name):
                    path = "C:" + '\\' + str(file)
                    speak(f"opening {file_name}")
                    os.startfile(path)
    except:
        speak(f"no music named: {file_name}")

def langtranslator():
    try:
        trans = Translator()

        speak("Say the language to translate in")
        language = get_audio().replace(" ", "")

        speak("what to translate")
        content = get_audio()

        t = trans.translate(text=content, dest=language)
        speak(f"{t.origin} in {t.dest} is{t.text}")

    except:
        speak("error")


# For make a note from text input
def make_note(text):
    date = datetime.datetime.now()
    if not os.path.exists('notes'):
        os.makedirs('notes')
    file_name = "notes/" + str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def convert():
    trans = Translator()

    speak("Say the language to translate in")
    language = get_audio().replace(" ", "")
    pg.hotkey("ctrl", 'c')
    tobespoken = pyperclip.paste()
    content = tobespoken

    t = trans.translate(text=content, dest=language)
    speak(f"{t.origin} in {t.dest} is{t.text}")

text=get_audio()

def database():
    Exception
    if "what do I have" in text:
        get_audio()
    client = wolframalpha.Client('your_client')
    speak(f"Searching for {text} in my database")
    try:
        res = client.query(text)
        result = next(res.result).text
        speak(result)
    except:
        #speak(f"Sir, your query {text} does not match any of the datani my data base.")
        #speak("Try asking other things..")
        #speak("sorry for in convinience sir")
        pass

def locate():
    place = query[1]
    speak(f"according to my data base {place} lies here")
    webbrowser.open_new_tab("https://www.google.com/maps/place/" + place)


def weather_at_place():
    owm = pyowm.OWM('your-api-key')
    location = owm.weather_at_place(f'{city}')
    weather = location.get_weather()
    temp = weather.get_temperature('celsius')
    humidity = weather.get_humidity()
    date = datetime.datetime.now().strftime("%A:%d:%B:%Y")
    current_temp = temp['temp']
    maximum_temp = temp['temp_max']
    min_temp = temp['temp_min']
    speak(f'The current temperature on {city} is {current_temp} degree celsius ')
    speak(f'The estimated maximum temperature for today {date} on {city} is {maximum_temp} degree celcius')
    speak(f'The estimated minimum temperature for today {date} on {city} is {min_temp} degree celcius')
    speak(f'The air is {humidity}% humid today on {city}')


def usrname():
    speak("What should i call you sir")
    uname = get_audio()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))

    speak("How can i Help you, Sir")

def onewordeans():
    speak("i'm listening")
    user_query = get_audio()

    URL = "https://www.google.co.in/search?q=" + user_query

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_='Z0LcW XcVN5d').get_text()
    print(result)
    speak(result)


# For playing a song from online (Youtube)
def play_from_online(text, status_bar=None):
    os.add_dll_directory(r'C:\Program Files (x86)\VideoLAN\VLC')
    import vlc, pafy

    # song name from user
    song = urllib.parse.urlencode({"search_query": text})
    print(song)

    # fetch the ?v=query_string
    result = urllib.request.urlopen("https://www.youtube.com/results?" + song)

    # make the url of the first result song
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})',
                                result.read().decode())  # 11 is the number of characters of each video
    print(search_results)

    # make the final url of song selects the very first result from youtube result
    url = "https://www.youtube.com/watch?v=" + search_results[0]

    # Play the song using vlc and pafy (dependency youtube-dl module)
    # modules which opens the video
    video = pafy.new(url)
    best = video.getbest()
    media = vlc.MediaPlayer(best.url)
    media.play()
    # Take time to open vlc
    while not media.is_playing():
        time.sleep(1)


def repeatmyspeech():
    speak("Okay starting to listen")
    speak(f"{name} {gender} start speaking")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(" I am Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        said = r.recognize_google(audio, language='en-in')
        speak(f"{name} {gender} said: {said}\n")
        print(f"{name} {gender} hre is ur repetition by me {said}\n")
        try:
            speak("should i save the file?")
            ans = get_audio()
            if "yes" in ans:
                try:
                    speak("What should i keep the file name")
                    filename = get_audio().lower
                    said.save(filename + ".mp3")
                    speak("File saved sucessfully")
                    try:
                        speak("Do you want me to show it?")
                        reply = get_audio()
                        if "yes" in reply:
                            os.startfile(filename + ".mp3")
                            speak("here it is")

                    except:
                        if "no" in reply:
                            speak("Never mind")

                except:
                    speak("Error in keeping filename")

        except:
            speak("Okay")

    except:
        return "None"
    return said


def recsound():
    fs = 44100
    speak("what should be the length of your sound wave Plz answer in seconds")
    ans = int(get_audio())
    seconds = ans

    recorded = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    speak("sucessfully recoreded")
    speak("what should i keep the file name")
    filename = get_audio()
    pg.write(filename + '.mp3', fs, recorded)
    speak("sucessfully saved")
    reply = get_audio()
    try:
        speak("should i show you")

        if "yes" in reply:
            os.startfile(filename + ".mp3")

    except:
        if "no" in reply:
            speak("okay next command sir")


def Screenshot():
    image = pg.screenshot()
    speak("screen shot taken")
    speak("what do you want to save it as?")
    filename = get_audio()
    image.save(filename + ".png")
    speak("do you want me to show it")
    ans = get_audio()
    if "yes" in ans:
        os.startfile(filename + ".png")
    else:
        speak("never mind")

def reads():
    pg.hotkey("ctrl", 'c')
    tobespoken = pyperclip.paste()
    speak(tobespoken)
"""
def capture():
    cam=camera.Camera(0)
    snap=cam.snap()
    files=[('All Files','*.*'),("Image Files",'*.jpg'),("Image Files",'*.png')]
    file=asksaveasfilename(filetypes=files,defaultextension=files)
    snap.save(file)
"""
def voice():
    fs=48000
    ans = int(get_audio())
    duration=ans
    myrecording=sd.rec(int(duration * fs), samplerate=fs,channels=2)
    sd.wait()
    #return sf.write('my_audio.flac',myrecording,fs)

############################################################################################################################

############################################################################################################################
############################################################################################################################

############################################################################################################################

import os
import random
import sys
import webbrowser
import time
import playsound
import pyautogui as pg
import wikipedia
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import re
import configparser
import threading
import datetime
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PIL import Image, ImageTk, ImageSequence
from multiprocessing import Process
from time import strftime
from ttkwidgets.font import askfont

#from package2 import (takecommand,detect_sentiment)

EVENTS_REMINDER_SERVICE = False
QUERY_SERVICE = False
assistant='Sister'
name='Rajesh'
gender='Bro'
btnState = False

# For displaying a popup window that contains an error message
def show_error_message(title, message):
    tkinter.messagebox.showerror(title, message)


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self):
        # lift a particular window above the others
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.events_reminder_service_var = tk.IntVar()
        self.query_service_var = tk.IntVar()

        self.initiate_service()

    def initiate_service(self):
        global EVENTS_REMINDER_SERVICE
        global NOTE_MAKING_SERVICE
        config = configparser.ConfigParser()

        # Get data from files
        if bool(config.read("config.ini")):
            if bool(int(config.get("DEFAULT", "events_reminder_service"))):
                self.events_reminder_service_var.set(1)
                EVENTS_REMINDER_SERVICE = True
            else:
                self.events_reminder_service_var.set(0)

            if bool(int(config.get("DEFAULT", "query_service"))):
                self.query_service_var.set(1)
                QUERY_SERVICE = True
            else:
                self.query_service_var.set(0)
        else:
            config['DEFAULT'] = {
                'events_reminder_service': "1",
                'query_service': "1"
            }
            # Write into config file
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    def active_service(self):
        global EVENTS_REMINDER_SERVICE
        global QUERY_SERVICE
        config = configparser.ConfigParser()
        config.read("config.ini")

        if self.events_reminder_service_var.get():
            config["DEFAULT"]["events_reminder_service"] = "1"
            EVENTS_REMINDER_SERVICE = True
        else:
            config["DEFAULT"]["events_reminder_service"] = "0"
            EVENTS_REMINDER_SERVICE = False

        if self.query_service_var.get():
            config["DEFAULT"]["query_service"] = "1"
            QUERY_SERVICE = True
        else:
            config["DEFAULT"]["query_service"] = "0"
            QUERY_SERVICE = False

        # Write into config file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assistant_strings_var = tk.StringVar()
        self.events_reminder_strings_var = tk.StringVar()
        self.query_service_strings_var = tk.StringVar()
        # Call the response_strings_form when Page2 initialized




class MainView(Page):
    def __init__(self, root=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.top_frame = tk.Frame(self)
        self.container = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)

        self.p1.config(bg="#249794")
        self.p2.config(bg="#249794")

        self.top_frame.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)
        self.bottom_frame.pack(side="bottom", fill="x", expand=False)
        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        # Add menus
        menu = tk.Menu(root)
        root.config(menu=menu)


        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.destroy)
        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Settings", command=self.p2.show)
        home_menu = tk.Menu(menu)
        menu.add_cascade(label="Home", menu=home_menu)
        home_menu.add_command(label="Main", command=self.p1.show)



        def switch():
            global btnState
            if btnState:
                btn.config(image=offImg, bg="#249794", activebackground="#249794")
                self.p2.config(bg="#249794")
                self.p1.config(bg="#249794")
                self.lbl.config(bg="#249794", activebackground="#249794")
                self.label.config(bg="#249794")
                #txt.config(text="Dark Mode: OFF", bg="#CECCBE")
                self.status_bar.config(bg="white",fg='black')
                #self.gif_label.config(bg='#249794')
                btnState = False
            else:
                btn.config(image=onImg, bg="#2B2B2B", activebackground="#2B2B2B")
                self.p1.config(bg="#2B2B2B")
                self.p2.config(bg="#2B2B2B")
                self.lbl.config(bg="#2B2B2B", activebackground="#2B2B2B",fg="white")
                self.label.config(bg="#2B2B2B")
                #txt.config(text="Dark Mode: ON", bg="#2B2B2B")
                self.status_bar.config( bg="gray",fg='white')
                #self.gif_label.config(bg='#2B2B2B')
                btnState = True

        # loading the switch images:
        onImg = PhotoImage(file=r"Untitled1.png")
        offImg = PhotoImage(file=r"Untitled2.png")

        # Night mode label:

        # switch widget:
        btn = tk.Button(self.p2, text="OFF", border=0, command=switch, bg="#249794", activebackground="#249794", cursor="hand2")
        # btn.place(relx=0.5, rely=0.15, anchor="center")
        btn.place(x=300,y=20)
        btn.config(image=offImg)



        self.lbl = tk.Label(self.p1, font=('DS-DIGIB.TTF', 10, 'bold'),anchor="w", bg="#249794")

        self.lbl.pack(anchor='center')

        def clcktime():
            string = strftime('%I:%M:%S %p')
            self.lbl.config(text=string)
            self.lbl.after(1000, clcktime)

        # Styling the label widget so that clock
        # will look more attractive

        clcktime()

        def font():
            res = askfont()
            if res[0] is not None:
                self.status_bar.configure(font=res[0])
                self.label.configure(font=res[0])
            #print(res)

        #window = tk.Tk()
        self.label = tk.Label(self.p2, text='Fonts', bg="#249794")
        self.label.place(x=20,y=80)
        tk.Button(self.p2, text="Pick a font", command=font).place(x=300,y=80)

        tk.Label(self.p2, text="Light or Dark Mode", font=font).place(x=20, y=20)


        self.top_frame.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)
        self.bottom_frame.pack(side="bottom", fill="x", expand=False)
        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)


        # Code for container Frame
        self.p1.show()

        #volume

        self.a = IntVar()
        self.a.set(49)
        self.s = Scale(self.p2, from_=0, to=100, length=100, width=20,variable=self.a, orient=HORIZONTAL)
        self.s.place(x=300,y=160)

        tk.Label(self.p2,text="Volume",font=font).place(x=20,y=160)


        # Service start button
        self.service_start_btn_var = tk.StringVar()
        self.service_start_btn_var.set("Run")
        service_start_btn = tk.Button(self.p1, textvariable=self.service_start_btn_var,
                                      font=("arial", 12,'bold'), bg="#066DBA", fg="#fff", cursor="hand2",
                                      command=self.service_listener,border=0) # GROOVE, RIDGE, SUNKEN, RAISED
        service_start_btn.pack(side="top", pady=25)

        # Assistant respone text lable
        response_text = ""
        with open("assistant_strings.txt", "r") as file:
            response_text = file.read()
        assistant_response_var = tk.StringVar()
        assistant_response_var.set("Say, \"" + response_text + "\" for response.")
        self.assistant_response_label = tk.Label(self.p1, textvariable=assistant_response_var, font=("arial", 12),
                                                 fg="#444444",relief='solid')


        self.status_bar = tk.Label(self.p1,text='Get Start...', wraplength=300,
                                   anchor="w", relief='solid',
                                   font=(font))
        self.status_bar.pack(side='top')

    #def __init__(self, parent):
        self.parent = self.p1
        self.canvas = tkinter.Canvas(self.p1,width=127,height=132)
        self.canvas.place(x=150,y=300)
        self.sequence = [ImageTk.PhotoImage(img)
                            for img in ImageSequence.Iterator(
                                    Image.open(
                                    r'speak.gif'))]
        self.image = self.canvas.create_image(65,92, image=self.sequence[0])
        #self.animate(1)
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        self.tvks=self.parent.after(160, lambda: self.animate((counter+1) % len(self.sequence)))


    def service_listener(self):
        self.service_start_btn_var.set("Running...")
        self.assistant_response_label.pack(side="top", pady=26)
        assitant_thread = threading.Thread(target=self.get_assistant)
        assitant_thread.start()

    #lists=listen



    def ani(self):

        pk2 = Process(target=self.animate(counter=1))


    def stop_ani(self):
        self.p1.after_cancel(self.tvks)
        #return self.text



    def get_assistant(self):

        #p1 = Process(target=usrname)
        #p1.start()
        #p2.start()




        with open("assistant_strings.txt", "r") as file:

            awake = file.read()

        try:
            #print("Say '" + awake + "' for response")
            self.status_bar["text"] = "Say '" + awake + "' for response"

            while True:
                #self.voice_data = get_audio()  # get the voice input


                if get_audio(status_bar=self.status_bar).lower().count(awake) > 0 :
                    self.ani()
                    speak("i'm listening")
                    self.stop_ani()
                    # self.status_bar["text"] = f"Recognizing...."
                    text = get_audio(status_bar=self.status_bar).lower()
                    #self.text = get_audio(status_bar=self.status_bar).lower()
                    recognize = False
                    today = datetime.date.today()
                    #self.detect_sentiment()

                    if 'stop it' in text:
                        self.stop_ani()

                    if "change my name to" in text:
                        query = query.replace("change my name to", "")
                        assname = query

                    elif "change name" in text:
                        self.ani()
                        speak(f"What would you like to call me, Sir ")
                        self.stop_ani()
                        assname = get_audio()
                        self.ani()
                        speak("Thanks for naming me")
                        self.stop_ani()

                    if "what do I have" in text or "do I have plans" in text or "am I busy on" in text:
                        service = "no" #authenticate_google()
                        date = get_date(text)
                        if date:
                            get_events(date, service)
                            assistant + get_audio()
                        else:
                            assistant + get_audio()

                    if "wikipedia" in text or "Wikipedia" in text or "let me tell" in text:
                        self.status_bar["text"] = f"{assistant}: Searching wikipedia..."
                        self.ani()
                        speak("Searching wikipedia...")
                        self.stop_ani()
                        text = text.replace("wikipedia", "")
                        results = wikipedia.summary(text, sentences=3)
                        self.status_bar["text"] = f"{assistant}: According to wikipedia"
                        self.ani()
                        speak("According to wikipedia")
                        self.stop_ani()
                        print(results)
                        self.status_bar["text"] = results + '\n'
                        self.ani()
                        speak(results + '\n')
                        self.stop_ani()

                    if 'search' in text:
                        try:
                            onewordeans()
                            self.status_bar["text"] = onewordeans()
                        except Exception:
                            #print('Sorry no result, please be clear')
                            self.status_bar["text"] = 'Sorry no result, please be clear'

                    if "don't listen" in text or "stop listening" in text:
                        speak("for how much time you want to stop jarvis from listening commands")
                        a = int(get_audio())
                        time.sleep(a)
                        #print(a)

                    if "search for" in text:
                        test = text.replace("search for", "")
                        database()

                    if "what" in text or "What" in text:
                        database()

                    if "who" in text or "Who" in text:
                        database()

                    if "why" in text or "Who" in text:
                        database()

                    if "where" in text or "Where" in text:
                        database()

                    if "play music" in text:
                        music_dir = "G:\\vcs\\music"
                        songs = os.listdir(music_dir)
                        #print(songs)
                        os.startfile(os.path.join(music_dir, songs[0]))

                    if "open youtube" in text:
                        self.status_bar["text"] = f"{assistant}: Opening youtube"
                        self.ani()
                        speak("Opening youtube")
                        self.stop_ani()
                        webbrowser.open_new_tab("youtube.com")

                    if "open discord" in text:
                        self.status_bar["text"] = f"{assistant}: Opening Discord"
                        self.ani()
                        speak("Opening Discord")
                        self.stop_ani()
                        webbrowser.open_new_tab("discord.com")

                    if "open discord app" in text:
                        discord = input("Enter the path of discord: ")
                        os.startfile("explorer.exe")
                        os.startfile(discord)

                    if "open terminal" in text or 'open command prompt' in text or 'open cmd' in text:
                        os.startfile("cmd")

                    if "what is the time" in text or 'what time is it' in text or 'time please' in text:
                        #self.status_bar1["text"] = detect_sentiment()
                        strTime = datetime.datetime.now().strftime("%I:%M:%p")
                        self.ani()
                        speak(f"the time is {strTime}")
                        self.stop_ani()
                        self.status_bar["text"] = f"{assname}:the time is {strTime}"


                    if "what is today's date" in text or "today's date" in text:
                        date = datetime.datetime.now().strftime("%A:%d:%B:%Y")
                        self.status_bar["text"] = f"{assistant}: Today is {date}"
                        self.ani()
                        speak(f"Today is {date} ")
                        self.stop_ani()

                    if "sister" in text or "hey" in text or "hello sister" in text:
                        stMsgs = [f'{assistant}: on your command sir', f'{assistant}: yes {name}', f'hello {name}',
                                  f'{assistant}: Waiting for your command sir']
                        self.status_bar["text"] = random.choice(stMsgs)
                        self.ani()
                        speak(random.choice(stMsgs))
                        self.stop_ani()

                    if "Thank You" in text  or "thank you" in text or "thanks" in text:
                        rep = ['Welcome', 'Well you know Rajesh im cool', 'Dont mention',
                               'By the way I should thank you for creating me']
                        self.status_bar["text"] = random.choice(
                            [f'{assistant}: Welcome', f'{assistant}: Well you know {name} im cool',
                             f'{assistant}: Dont mention',
                             f'{assistant}: By the way I should thank you for creating me'])
                        self.ani()
                        speak(random.choice(rep))
                        self.stop_ani()

                    if "say something" in text or "say anything" in text:
                        self.status_bar["text"] = f"{assistant}: what's your name?"
                        self.ani()
                        speak("what's your name?")
                        self.stop_ani()

                    if "when was your project started" in text or "when you programmed" in text\
                            or " when you started" in text or " when you process started" in text:
                        #self.status_bar1["text"] = get_audio

                        self.status_bar["text"] = f"{assistant}: My journey started on eleventh of april on 2020"
                        self.ani()
                        speak("my journey started on eleventh of april on 2020")
                        self.stop_ani()

                    if "who made you" in text or "who created you" in text:
                        self.status_bar["text"] = f"{assistant}: I was created by {name} on eleventh of april on 2020"
                        self.ani()
                        speak("I was created by Rajesh on eleventh of april on 2020")
                        self.stop_ani()


                    if "how were you developed" in text or "can i see your source code" in text\
                            or "show me a source code" in text:
                        self.status_bar["text"] = f"{assistant}: Sorry brother I am not allowed to reveval all my secrets"
                        self.ani()
                        speak("Sorry brother  I am not allowed to discuss or show all my secrets  ")
                        self.stop_ani()

                    if "how are you developed" in text:
                        self.status_bar["text"] = f"{assistant}: Sorry boss I am not allowed to reveval all my secrets"
                        self.ani()
                        speak("Sorry boss  I am not allowed to reveval all of my secrets  ")
                        self.stop_ani()

                    if "tell me a joke" in text or "Crack a joke" in text or "crack a joke" in text:
                        jokes = [
                            "A Doctor said to a patient , I'm sorry but you suffer from a terminal illness and have only 10 to live , then the Patient said What do you mean, 10, 10 what, Months, Weeks, and the Doctor said Nine.",
                            "Once my Brother who never used to drink was arrested for over drinking,When I lates had gone and asked him why were you arressted, He replied he had not brushed since a week",
                            "A Teacher said Kids, what does the chicken give you? The Student replied Meat Teacher said  Very good Now what does the pig give you? Student said BaconTeacher said  Great  And what does the fat cow give you? Student said Homework!",
                            "A child asked his father, How were people born? So his father said, Adam and Eve made babies, then their babies became adults and made babies, and so on  The child then went to his mother, asked her the same question and she told him, We were monkeys then we evolved to become like we are now  The child ran back to his father and said, You lied to me  His father replied, No, your mom was talking about her side of the family."]
                        self.status_bar["text"] = random.choice(jokes)
                        self.ani()
                        speak(random.choice(jokes))
                        self.stop_ani()
                        self.status_bar["text"] = "Do you want more?"
                        self.ani()
                        speak("Do you want more?")
                        self.stop_ani()
                        ans = get_audio()
                        if "yes" in ans:
                            self.status_bar["text"] = random.choice(jokes)
                            self.ani()
                            speak(random.choice(jokes))
                            self.stop_ani()

                        if "no" in ans:
                            self.status_bar["text"] = random.choice(jokes)
                            self.ani()
                            speak(random.choice(jokes))
                            self.stop_ani()

                    if "who is your brother" in text:
                        self.status_bar[
                            "text"] = f"{name} is my developer my teacher the one who taught me how be a good wise smart and a intelligent person assistant was previously his name And since he left the hacking world he gave this name to me and started programming with python then created me  Now i Am proud to be assistant at last  "
                        self.ani()
                        speak(
                            f"{name} is my developer my teacher the one who taught me how be a good wise smart and a intelligent person assistant was previously his name And since he left the hacking world he gave this name to me and started programming with python then created me  Now i Am proud to be assistant at last  ")
                        self.stop_ani()

                    if "good morning" in text:
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        self.status_bar[
                            "text"] = f"Good morning {name} {gender} it is {strTime} now,Hope you had a good sleep."
                        self.ani()
                        speak(f"Good morning {name} {gender} it is {strTime} now,Hope you had a good sleep.")
                        self.stop_ani()

                    if "good night" in text:
                        strTime = datetime.datetime.now().strftime("%X").replace(":", " ")
                        gtime = strTime.replace(":", " ")
                        self.status_bar["text"] = f"Good night {name} {gender} it is {gtime} sleep tight.."
                        self.ani()
                        speak(f"Good night {name} {gender} it is {gtime} sleep tight..")
                        self.stop_ani()

                    if "open my inbox" in text:
                        self.ani()
                        speak('opening inbox')
                        self.stop_ani()
                        webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")

                    if "open my sent mail" in text:
                        self.ani()
                        speak('opening sent mail')
                        self.stop_ani()
                        webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#sent")

                    if "open youtube and search for" in text:
                        query = text.split("open youtube and search for")
                        self.status_bar["text"] = "opening youtube"
                        self.ani()
                        speak("opening youtube")
                        self.stop_ani()
                        webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query[1]}")

                    if "repeat my speech" in text:
                        repeatmyspeech()

                    if "close chrome" in text:
                        os.system('TASKKILL /F /IM Google Chrome.exe')

                    if "close task manager" in text:
                        os.system('TASKKILL /F /IM Taskmgr.exe')

                    if "delete" in text:
                        final = text.split("delete")
                        os.system("del " + final[1])

                    if "shutdown" in text:
                        self.status_bar["text"] = "okay, shutting down your pc"
                        self.ani()
                        speak("okay,shutting down your pc")
                        self.stop_ani()
                        os.system('shutdown/s')

                    if "restart my pc" in text:
                        self.status_bar["text"] = "okay, restarting your pc"
                        self.ani()
                        speak("okay, restarting your pc")
                        self.stop_ani()
                        os.system('shutdown/r')

                    if "record my voice" in text:
                        recsound()

                    if "record voice" in text:
                        voice()

                    if "take a screenshot" in text:
                        Screenshot()

                    if "exit" in text:
                        self.status_bar[
                            "text"] = f"Thank you {name} for giving \n your time i had fun \n serving you,have a good time"
                        self.ani()
                        speak(f"Thank you {name} for \n giving your time i had \n fun serving you,have \n a good time")
                        self.stop_ani()
                        self.status_bar["text"] = "closing engine"
                        self.ani()
                        speak("closing engine")
                        self.stop_ani()
                        self.status_bar["text"] = "closing required application"
                        self.ani()
                        speak("closing required applications")
                        self.stop_ani()
                        endTime = int(datetime.datetime.now().hour)
                        f = open("goodnight.txt", "w+")
                        end = int(datetime.datetime.now().hour)
                        f.write(str(end))
                        f.close()
                        quit()

                    if "text" in text:
                        self.status_bar["text"] = f"okay i am listening speak{name} {gender}"
                        self.ani()
                        speak(f"okay i am listening speak{name} {gender}")
                        self.stop_ani()
                        pg.typewrite(get_audio())

                    if "select all" in text:
                        pg.hotkey('ctrl', 'a')

                    if "close this window" in text:
                        pg.hotkey('alt', 'f4')

                    if "open a new tab" in text:
                        pg.hotkey('ctrl', 'n')

                    if "open a new incognito window" in text:
                        pg.hotkey('ctrl', 'shift', 'n')

                    if "copy" in text:
                        pg.hotkey('ctrl', 'c')
                        self.status_bar["text"] = "text copied to clipboard"
                        self.ani()
                        speak('text copied to clipboard')
                        self.stop_ani()

                    if "paste" in text:
                        pg.hotkey('ctrl', 'v')

                    if "undo" in text:
                        pg.hotkey('ctrl', 'z')

                    if "redo" in text:
                        pg.hotkey('ctrl', )

                    if "save this file" in text:
                        pg.hotkey('ctrl', 's')

                    if "open computer" in text:
                        pg.hotkey('windows logo key', 'e')

                    if 'activate' in text:
                        quert=get_audio()
                        try:
                            if "back" in quert:
                                pg.hotkey('browserback')

                            if "go up" in quert:
                                pg.hotkey('pageup')

                            if "go left" in quert:
                                pg.hotkey('end')

                            if "go right" in quert:
                                pg.hotkey('home')

                            if "go down" in quert:
                                pg.hotkey('pagedown')
                        except Exception:
                            #print('Sorry no result, please be clear')
                            self.status_bar["text"] = 'Sorry no result, please be clear'

                    if "read" in text:
                        try:
                            read()
                        except:
                            self.status_bar["text"] = "no text selected plz select a text"
                            self.ani()
                            speak("no text selected plz select a text")
                            self.stop_ani()

                    if "translate to" in text:
                        query = text.split("translate to")
                        dest = query[1]
                        langtranslator()

                    if "introduce yourself" in text or "tell me about yourself" in text:
                        self.status_bar["text"] = "Okay,Let me start by The time I was born,,"
                        self.ani()
                        speak("Okay,Let me start by The time I was born,,")
                        self.stop_ani()
                        self.status_bar["text"] = "I was a dream of a boy dreaming to make a perfect virtual assistant"
                        self.ani()
                        speak("I was a dream of a boy dreaming to make a perfect virtual assistant")
                        self.stop_ani()
                        self.status_bar["text"] = "He soon established the company named assistant"
                        self.ani()
                        speak("He soon established the company named assistant")
                        self.stop_ani()
                        self.status_bar["text"] = "Slowly,I came to life"
                        self.ani()
                        speak("Slowly,I came to life")
                        self.stop_ani()
                        self.status_bar[
                            "text"] = "I started learning various things like calculations,General knowledge etc etc"
                        self.ani()
                        speak("I started learning various things like calculations,General knowledge etc etc")
                        self.stop_ani()
                        self.status_bar[
                            "text"] = "Now I am capable of doing various things like Beatboxing,opening applications,Cracking jokes,Playing music etc."
                        self.ani()
                        speak(
                            "Now I am capable of doing various things like Beatboxing,opening applications,Cracking jokes,Playing music etc.")
                        self.stop_ani()
                        self.status_bar["text"] = "Okay,thats a wrap I wont say more "
                        self.ani()
                        speak("Okay,thats a wrap I wont say more ")
                        self.stop_ani()

                    if "translate" in text:
                        langtranslator()

                    if "in" in text:
                        query = text.split("in")
                        text = query[0]
                        dest = [1]

                    if "convert selected " in text:
                        convert()

                    if "I am sad" in text:
                        playsound.playsound("hopetone.mp3")
                        playsound.playsound("alarm.mp3")
                        playsound.playsound("hopetone.mp3")
                        playsound.playsound("alarm.mp3")
                        playsound.playsound("hopetone.mp3")
                        playsound.playsound("alarm.mp3")

                    if "remind me" in text:
                        os.system("python pyautogui1.py")

                    if "play" in text:
                        openafile()

                    if "locate" in text:
                        query = text.split("locate")
                        locate()

                    if "where is" in text:
                        query = text.split("where is")
                        locate()

                    if "none" in text:
                        get_audio()

                    if "I know that" in text:
                        self.status_bar["text"] = "ya, you are right"
                        self.ani()
                        speak("Ya, ure right")
                        self.stop_ani()

                    if "take picture" in text:
                        self.status_bar['text']='ok'
                        self.ani()
                        speak('ok')
                        #capture()

                    if "make a note" in text or "write this down" in text or "remember this" in text:
                        NOTE_STRS = ["make a note", "write this down", "remember this"]
                        for phrase in NOTE_STRS:
                            if phrase in text:
                                self.status_bar["text"] = "What would you like me to write down?"
                                self.ani()
                                speak("What would you like me to write down? ")
                                self.stop_ani()
                                write_down = get_audio()
                                make_note(write_down)
                                self.status_bar["text"] = "I've made a note of that."
                                self.ani()
                                speak("I've made a note of that.")
                                self.stop_ani()
                            break



        except:
            pass

        #self.service_start_btn_var.set("Start Service")



############################################################################################################################
if __name__ == "__main__":
    main_view = MainView(root)
    main_view.pack(side="top", fill="both", expand=True)

    root.mainloop()