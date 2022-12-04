
import pickle
from multiprocessing import Process


class UserData:
	def __init__(self):
		self.name = 'None'
		self.gender = 'None'
		self.userphoto = 0

	def extractData(self):
		with open('userData/userData.pck', 'rb') as file:
			details = pickle.load(file)
			self.name, self.gender, self.userphoto = details['name'], details['gender'], details['userphoto']

	def updateData(self, name, gender, userphoto):
		with open('userData/userData.pck', 'wb') as file:
			details = {'name': name, 'gender': gender, 'userphoto': userphoto}
			pickle.dump(details, file)

	def getName(self):
		return self.name

	def getGender(self):
		return self.gender

	def getUserPhoto(self):
		return self.userphoto

def UpdateUserPhoto(avatar):
	u = UserData()
	u.extractData()
	u.updateData(u.getName(), u.getGender(), avatar)


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from os.path import isfile, join
from threading import Thread
#from userHandler import UserData

import FACE_UNLOCKER as FU

background, textColor = 'black', '#F6FAFB'
background, textColor = textColor, background

avatarChoosen = 0
choosedAvtrImage = None
user_name = ''
user_gender = ''

try:
    face_classifier = cv2.CascadeClassifier('Cascade/haarcascade_frontalface_default.xml')
except Exception as e:
    print('Cascade File is missing...')
    raise SystemExit

if os.path.exists('userData') == False:
    os.mkdir('userData')
if os.path.exists('userData/faceData') == False:
    os.mkdir('userData/faceData')


###### ROOT1 ########
def startLogin():
    try:
        result = FU.startDetecting()
        if result:
            user = UserData()
            user.extractData()
            userName = user.getName().split()[0]
            welcLbl['text'] = 'Hi ' + userName + ',\nWelcome to the world of\nScience & Technology'
            loginStatus['text'] = 'UNLOCKED'
            loginStatus['fg'] = 'green'
            faceStatus['text'] = '(Logged In)'
            #os.system('python GUIASSISTANT.py')
            root.after(3000,lambda:root.destroy())
        else:
            print('Error Occurred')

    except Exception as e:
        print(e)


####### ROOT2 ########
def trainFace():
    data_path = 'userData/faceData/'
    onlyfiles = [f for f in os.listdir(data_path) if isfile(join(data_path, f))]

    Training_data = []
    Labels = []

    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        Training_data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)

    model = cv2.face_LBPHFaceRecognizer.create()
    model.train(np.asarray(Training_data), np.asarray(Labels))

    print('Model Trained Successfully !!!')
    model.save('userData/trainer.yml')
    print('Model Saved !!!')


def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return None

    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]

    return cropped_face


cap = None
count = 0


def startCapturing():
    global count, cap
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        file_name_path = 'userData/faceData/img' + str(count) + '.png'
        cv2.imwrite(file_name_path, face)
        print(count)
        progress_bar['value'] = count

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    else:
        pass

    if count == 100:
        progress_bar.destroy()
        lmain['image'] = defaultImg2
        statusLbl['text'] = '(Face added successfully)'
        cap.release()
        cv2.destroyAllWindows()
        Thread(target=trainFace).start()
        addBtn['text'] = '        Next        '
        addBtn['command'] = lambda: raise_frame(root3)
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    frame = cv2.flip(frame, 1)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, startCapturing)


def Add_Face():
    global cap, user_name, user_genderb
    user_name = nameField.get()
    user_gender = r.get()
    if user_name != '' and user_gender != 0:
        if agr.get() == 1:
            cap = cv2.VideoCapture(0)
            startCapturing()
            progress_bar.place(x=20, y=273)
            statusLbl['text'] = ''
        else:
            statusLbl['text'] = '(Check the Condition)'
    else:
        statusLbl['text'] = '(Please fill the details)'


def SuccessfullyRegistered():
    if avatarChoosen != 0:
        gen = 'Male'
        if user_gender == 2: gen = 'Female'
        u = UserData()
        u.updateData(user_name, gen, avatarChoosen)
        usernameLbl['text'] = user_name
        raise_frame(root4)


def selectAVATAR(avt=0):
    global avatarChoosen, choosedAvtrImage
    avatarChoosen = avt
    i = 1
    for avtr in (avtb1, avtb2, avtb3, avtb4, avtb5, avtb6, avtb7, avtb8):
        if i == avt:
            avtr['state'] = 'disabled'
            userPIC['image'] = avtr['image']
        else:
            avtr['state'] = 'normal'
        i += 1


################################################# GUI ###############################


def raise_frame(frame):
    frame.tkraise()

if __name__ == '__main__':
    root = Tk()
    root.title('G.O.S.')
    w_width, w_height = 400, 650
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))  # center location of the screen
    root.configure(bg=background)
    # root.attributes('-toolwindow', True)

    root1 = Frame(root, bg=background)
    root2 = Frame(root, bg='#484646')
    root3 = Frame(root, bg=background)
    root4 = Frame(root, bg=background)

    for f in (root1, root2, root3, root4):
        f.grid(row=0, column=0, sticky='news')

    ################################
    ########  MAIN SCREEN  #########
    ################################
    img = PhotoImage(file="reg_pg1.png")
    wins = Label(root1, image=img)
    wins.pack()

    """image1 = Image.open('extrafiles/images/speak.gif')
    image1 = image1.resize((127, 132))
    defaultImg1 = ImageTk.PhotoImage(image1)

    dataFrame1 = Frame(root1, bd=10, bg=background)
    dataFrame1.pack()
    logo = Label(dataFrame1, width=127, height=132, image=defaultImg1)
    logo.pack(padx=10, pady=10)"""

    # welcome label
    welcLbl = Label(root1, text="Hello I'm G.O.S.\nWelcome to,\nour Technology World", font=('Arial Bold', 13),fg='white', bg="#484646")
    welcLbl.place(x=107,y=180)

    # add face
    loginStatus = Label(root1, text='LOCKED', font=('Arial Bold', 13), bg='#484646', fg='white')
    loginStatus.place(x=80,y=550)

    if os.path.exists('userData/trainer.yml') == False:
        loginStatus['text'] = 'Click to register your account'
        addFace = Button(root1, text='   Register Account   ', font=('Arial', 12), bg='#185c08', fg='white', relief=FLAT,
                         command=lambda: raise_frame(root2))
        addFace.place(x=125,y=500)
    else:
        # pass
        Thread(target=startLogin).start()

    # status of add face
    faceStatus = Label(root1, text="(Ready to enter into the future)", font=('Arial 10'), fg=textColor, bg=background)
    faceStatus.pack(pady=5)

    ##################################
    ########  FACE ADD SCREEN  #######
    ##################################

    #img1 = PhotoImage(file="reg_pg2.png")
    #wins1 = Label(root2, image=img1)
    #wins1.pack()

    image2 = Image.open('extrafiles/images/scanpic.png')
    image2 = image2.resize((300, 250))
    defaultImg2 = ImageTk.PhotoImage(image2)

    dataFrame2 = Frame(root2, bd=10, bg='#484646')
    dataFrame2.pack(fill=X)
    lmain = Label(dataFrame2, width=300, height=250, image=defaultImg2)
    lmain.pack(padx=10, pady=10)

    # Details
    detailFrame2 = Frame(root2, bd=10, bg='#484646')
    detailFrame2.pack(fill=X)
    userFrame2 = Frame(detailFrame2, bd=10, width=300, height=250, relief=FLAT, bg='#484646')
    userFrame2.pack(padx=10, pady=10)

    # progress
    progress_bar = ttk.Progressbar(root2, orient=HORIZONTAL, length=303, mode='determinate')

    # name
    nameLbl = Label(userFrame2, text='Name', font=('Arial Bold', 12), fg='white', bg='#484646')
    nameLbl.place(x=10, y=10)
    nameField = Entry(userFrame2, bd=5, font=('Arial Bold', 10), width=25, relief=FLAT, bg='#D4D5D7')
    nameField.focus()
    nameField.place(x=80, y=10)

    genLbl = Label(userFrame2, text='Gender', font=('Arial Bold', 12), fg='white', bg='#484646')
    genLbl.place(x=10, y=50)
    r = IntVar()
    s = ttk.Style()
    s.configure('Wild.TRadiobutton', background='#484646', foreground=textColor, font=('Arial Bold', 10),
                focuscolor=s.configure(".")["background"])
    genMale = ttk.Radiobutton(userFrame2, text='Male', value=1, variable=r, style='Wild.TRadiobutton', takefocus=False)
    genMale.place(x=80, y=52)
    genFemale = ttk.Radiobutton(userFrame2, text='Female', value=2, variable=r, style='Wild.TRadiobutton',
                                takefocus=False)
    genFemale.place(x=150, y=52)

    # agreement
    agr = IntVar()
    sc = ttk.Style()
    sc.configure('Wild.TCheckbutton', background='#484646', foreground='white', font=('Arial Bold', 10),
                 focuscolor=sc.configure(".")["background"])
    # agree = Checkbutton(userFrame2, text='I agree to use my face for Security purpose', fg=textColor, bg=background, activebackground=background, activeforeground=textColor)
    agree = ttk.Checkbutton(userFrame2, text='I agree to use my Face for Security', style='Wild.TCheckbutton',
                            takefocus=False, variable=agr)
    agree.place(x=28, y=100)
    # add face
    addBtn = Button(userFrame2, text='    Add Face    ', font=('Arial Bold', 12), bg='#01933B', fg='white',
                    command=Add_Face, relief=FLAT)
    addBtn.place(x=90, y=150)

    # status of add face
    statusLbl = Label(userFrame2, text='', font=('Arial 10'), fg=textColor, bg='#484646')
    statusLbl.place(x=80, y=190)

    ##########################
    #### AVATAR SELECTION ####
    ##########################

    Label(root3, text="Choose Your Avatar", font=('arial', 15), bg='#484646', fg='white').pack()

    avatarContainer = Frame(root3, bg='#484646', width=300, height=500)
    avatarContainer.pack(pady=10)
    size = 100

    avtr1 = Image.open('extrafiles/images/avatars/a1.png')
    avtr1 = avtr1.resize((size, size))
    avtr1 = ImageTk.PhotoImage(avtr1)
    avtr2 = Image.open('extrafiles/images/avatars/a2.png')
    avtr2 = avtr2.resize((size, size))
    avtr2 = ImageTk.PhotoImage(avtr2)
    avtr3 = Image.open('extrafiles/images/avatars/a3.png')
    avtr3 = avtr3.resize((size, size))
    avtr3 = ImageTk.PhotoImage(avtr3)
    avtr4 = Image.open('extrafiles/images/avatars/a4.png')
    avtr4 = avtr4.resize((size, size))
    avtr4 = ImageTk.PhotoImage(avtr4)
    avtr5 = Image.open('extrafiles/images/avatars/a5.png')
    avtr5 = avtr5.resize((size, size))
    avtr5 = ImageTk.PhotoImage(avtr5)
    avtr6 = Image.open('extrafiles/images/avatars/a6.png')
    avtr6 = avtr6.resize((size, size))
    avtr6 = ImageTk.PhotoImage(avtr6)
    avtr7 = Image.open('extrafiles/images/avatars/a7.png')
    avtr7 = avtr7.resize((size, size))
    avtr7 = ImageTk.PhotoImage(avtr7)
    avtr8 = Image.open('extrafiles/images/avatars/a8.png')
    avtr8 = avtr8.resize((size, size))
    avtr8 = ImageTk.PhotoImage(avtr8)

    avtb1 = Button(avatarContainer, image=avtr1, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(1))
    avtb1.grid(row=0, column=0, ipadx=25, ipady=10)

    avtb2 = Button(avatarContainer, image=avtr2, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(2))
    avtb2.grid(row=0, column=1, ipadx=25, ipady=10)

    avtb3 = Button(avatarContainer, image=avtr3, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(3))
    avtb3.grid(row=1, column=0, ipadx=25, ipady=10)

    avtb4 = Button(avatarContainer, image=avtr4, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(4))
    avtb4.grid(row=1, column=1, ipadx=25, ipady=10)

    avtb5 = Button(avatarContainer, image=avtr5, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(5))
    avtb5.grid(row=2, column=0, ipadx=25, ipady=10)

    avtb6 = Button(avatarContainer, image=avtr6, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(6))
    avtb6.grid(row=2, column=1, ipadx=25, ipady=10)

    avtb7 = Button(avatarContainer, image=avtr7, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(7))
    avtb7.grid(row=3, column=0, ipadx=25, ipady=10)

    avtb8 = Button(avatarContainer, image=avtr8, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(8))
    avtb8.grid(row=3, column=1, ipadx=25, ipady=10)

    Button(root3, text='         Submit         ', font=('Arial Bold', 15), bg='#01933B', fg='white', bd=0, relief=FLAT,
           command=SuccessfullyRegistered).pack()

    #########################################
    ######## SUCCESSFULL REGISTRATION #######
    #########################################

    userPIC = Label(root4, bg=background, image=avtr1)
    userPIC.pack(pady=(40, 10))
    usernameLbl = Label(root4, text="Rajesh", font=('Arial Bold', 15), bg=background, fg='#85AD4F')
    usernameLbl.pack(pady=(0, 70))

    Label(root4, text="Your account has been successfully activated!", font=('Arial Bold', 15), bg=background,
          fg='#303E54', wraplength=300).pack(pady=10)
    Label(root4, text="Launch the APP again to get started the conversation with your Personal Assistant",
          font=('arial', 13), bg=background, fg='#A3A5AB', wraplength=350).pack()

    Button(root4, text='     OK     ', bg='#0475BB', fg='white', font=('Arial Bold', 18), bd=0, relief=FLAT,
           command=lambda: quit()).pack(pady=50)

    root.iconbitmap('extrafiles/images/logo.ico')
    raise_frame(root1)
    root.mainloop()

###########################################################################################################################
###########################################################################################################################


########################################################################################################################
########################################################################################################################

from difflib import get_close_matches
import json
from random import choice
import datetime


class DateTime:
    def currentTime(self):
        time = datetime.datetime.now()
        x = " A.M."
        if time.hour > 12: x = " P.M."
        time = str(time)
        time = time[11:16] + x
        return time

    def currentDate(self):
        now = datetime.datetime.now()
        day = now.strftime('%A')
        date = str(now)[8:10]
        month = now.strftime('%B')
        year = str(now.year)
        result = f'{day}, {date} {month}, {year}'
        return result


def wishMe():
    now = datetime.datetime.now()
    hr = now.hour
    if hr < 12:
        wish = "Good Morning"
    elif hr >= 12 and hr < 16:
        wish = "Good Afternoon"
    else:
        wish = "Good Evening"
    return wish


def isContain(text, lst):
    for word in lst:
        if word in text:
            return True
    return False


def chat(text):
    dt = DateTime()
    result = ""
    if isContain(text, ['good']):
        result = wishMe()
    elif isContain(text, ['time']):
        result = "Current Time is: " + dt.currentTime()
    elif isContain(text, ['date', 'today', 'day', 'month']):
        result = dt.currentDate()

    return result


data = json.load(open('extrafiles/NormalChat.json', encoding='utf-8'))


def reply(query):
    if query in data:
        response = data[query]
    else:
        query = get_close_matches(query, data.keys(), n=2, cutoff=0.6)
        if len(query) == 0: return "None"
        return choice(data[query[0]])

    return choice(response)


def lang_translate(text, language):
    from googletrans import Translator, LANGUAGES
    if language in LANGUAGES.values():
        translator = Translator()
        result = translator.translate(text, src='en', dest=language)
        return result
    else:
        return "None"


########################################################################################################################
########################################################################################################################

import math
def basicOperations(text):
	if 'root' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return round(math.sqrt(num),2)

	text = text.replace('plus', '+')
	text = text.replace('minus', '-')
	text = text.replace('x', '*')
	text = text.replace('multiplied by', '*')
	text = text.replace('multiply', '*')
	text = text.replace('divided by', '/')
	text = text.replace('to the power', '**')
	text = text.replace('power', '**')
	result = eval(text)
	return round(result,2)

def bitwiseOperations(text):
	if 'right shift' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return num>>1
	elif 'left shift' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return num<<1
	text = text.replace('and', '&')
	text = text.replace('or', '|')
	text = text.replace('not of', '~')
	text = text.replace('not', '~')
	text = text.replace('xor', '^')
	result = eval(text)
	return result

def conversions(text):
	temp = text.rfind(' ')
	num = int(text[temp+1:])
	if 'bin' in text:
		return eval('bin(num)')[2:]
	elif 'hex' in text:
		return eval('hex(num)')[2:]
	elif 'oct' in text:
		return eval('oct(num)')[2:]

def trigonometry(text):
	temp = text.replace('degree','')
	temp = text.rfind(' ')
	deg = int(text[temp+1:])
	rad = (deg * math.pi) / 180
	if 'sin' in text:
		return round(math.sin(rad),2)
	elif 'cos' in text:
		return round(math.cos(rad),2)
	elif 'tan' in text:
		return round(math.tan(rad),2)

def factorial(n):
	if n==1 or n==0: return 1
	else: return n*factorial(n-1)

def isHaving(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def perform(text):
	text = text.replace('math','')
	if "factorial" in text: return str(factorial(int(text[text.rfind(' ')+1:])))
	elif isHaving(text, ['sin','cos','tan']): return str(trigonometry(text))
	elif isHaving(text, ['bin','hex','oct']): return str(conversions(text))
	elif isHaving(text, ['shift','and','or','not']): return str(bitwiseOperations(text))
	else: return str(basicOperations(text))


########################################################################################################################
########################################################################################################################

# import pyscreenshot as ImageGrab
import time
import os
import subprocess
from pynput.keyboard import Key, Controller

#import psutil

class SystemTasks:
    def __init__(self):
        self.keyboard = Controller()

    def openApp(self, appName):
        appName = appName.replace('paint', 'mspaint')
        appName = appName.replace('wordpad', 'write')
        appName = appName.replace('word', 'write')
        appName = appName.replace('calculator', 'calc')
        try:
            subprocess.Popen('C:\\Windows\\System32\\' + appName[5:] + '.exe')
        except:
            pass

    def write(self, text):
        text = text[5:]
        for char in text:
            self.keyboard.type(char)
            time.sleep(0.02)

    def select(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(Key.ctrl)

    def hitEnter(self):
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def delete(self):
        self.keyboard.press(Key.backspace)
        self.keyboard.release(Key.enter)

    def save(self, text):
        if "don't" in text:
            self.keyboard.press(Key.right)
        else:
            self.keyboard.press(Key.ctrl)
            self.keyboard.press('s')
            self.keyboard.release('s')
            self.keyboard.release(Key.ctrl)
        self.hitEnter()


class TabOpt:
    def __init__(self):
        self.keyboard = Controller()

    def switchTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.ctrl)

    def closeTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('w')
        self.keyboard.release('w')
        self.keyboard.release(Key.ctrl)

    def newTab(self):
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('n')
        self.keyboard.release('n')
        self.keyboard.release(Key.ctrl)


class WindowOpt:
    def __init__(self):
        self.keyboard = Controller()

    def openWindow(self):
        self.maximizeWindow()

    def closeWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.f4)
        self.keyboard.release(Key.f4)
        self.keyboard.release(Key.alt_l)

    def minimizeWindow(self):
        for i in range(2):
            self.keyboard.press(Key.cmd)
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            self.keyboard.release(Key.cmd)
            time.sleep(0.05)

    def maximizeWindow(self):
        self.keyboard.press(Key.cmd)
        self.keyboard.press(Key.up)
        self.keyboard.release(Key.up)
        self.keyboard.release(Key.cmd)

    def moveWindow(self, operation):
        self.keyboard.press(Key.cmd)

        if "left" in operation:
            self.keyboard.press(Key.left)
            self.keyboard.release(Key.left)
        elif "right" in operation:
            self.keyboard.press(Key.right)
            self.keyboard.release(Key.right)
        elif "down" in operation:
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
        elif "up" in operation:
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)
        self.keyboard.release(Key.cmd)

    def switchWindow(self):
        self.keyboard.press(Key.alt_l)
        self.keyboard.press(Key.tab)
        self.keyboard.release(Key.tab)
        self.keyboard.release(Key.alt_l)

    def takeScreenShot(self):
        from random import randint
        im = ImageGrab.grab()
        im.save(f'Files and Document/ss_{randint(1, 100)}.jpg')


def isContain(text, lst):
    for word in lst:
        if word in text:
            return True
    return False


def Win_Opt(operation):
    w = WindowOpt()
    if isContain(operation, ['open']):
        w.openWindow()
    elif isContain(operation, ['close']):
        w.closeWindow()
    elif isContain(operation, ['mini']):
        w.minimizeWindow()
    elif isContain(operation, ['maxi']):
        w.maximizeWindow()
    elif isContain(operation, ['move', 'slide']):
        w.moveWindow(operation)
    elif isContain(operation, ['switch', 'which']):
        w.switchWindow()
    elif isContain(operation, ['screenshot', 'capture', 'snapshot']):
        w.takeScreenShot()
    return


def Tab_Opt(operation):
    t = TabOpt()
    if isContain(operation, ['new', 'open', 'another', 'create']):
        t.newTab()
    elif isContain(operation, ['switch', 'move', 'another', 'next', 'previous', 'which']):
        t.switchTab()
    elif isContain(operation, ['close', 'delete']):
        t.closeTab()
    else:
        return


def System_Opt(operation):
    s = SystemTasks()
    if 'delete' in operation:
        s.delete()
    elif 'save' in operation:
        s.save(operation)
    elif 'type' in operation:
        s.write(operation)
    elif 'select' in operation:
        s.select()
    elif 'enter' in operation:
        s.hitEnter()
    elif isContain(operation, ['notepad', 'paint', 'calc', 'word']):
        s.openApp(operation)
    elif isContain(operation, ['music', 'video']):
        s.playMusic(operation)
    else:
        open_website(operation)
        return


###############################
###########  VOLUME ###########
###############################

keyboard = Controller()


def mute():
    for i in range(50):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)


def full():
    for i in range(50):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)


def volumeControl(text):
    if 'full' in text or 'max' in text:
        full()
    elif 'mute' in text or 'min' in text:
        mute()
    elif 'incre' in text:
        for i in range(5):
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)
    elif 'decre' in text:
        for i in range(5):
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)


def systemInfo():
    import wmi
    c = wmi.WMI()
    my_system_1 = c.Win32_LogicalDisk()[0]
    my_system_2 = c.Win32_ComputerSystem()[0]
    info = ["Total Disk Space: " + str(round(int(my_system_1.Size) / (1024 ** 3), 2)) + " GB",
            "Free Disk Space: " + str(round(int(my_system_1.Freespace) / (1024 ** 3), 2)) + " GB",
            "Manufacturer: " + my_system_2.Manufacturer,
            "Model: " + my_system_2.Model,
            "Owner: " + my_system_2.PrimaryOwnerName,
            "Number of Processors: " + str(my_system_2.NumberOfProcessors),
            "System Type: " + my_system_2.SystemType]
    return info


def batteryInfo():
    import psutil
    usage = str(psutil.cpu_percent(interval=0.1))
    battery = psutil.sensors_battery()
    pr = str(battery.percent)
    if battery.power_plugged:
        return "Your System is currently on Charging Mode and it's " + pr + "% done."
    return "Your System is currently on " + pr + "% battery life."


def OSHandler(query):
    if isContain(query, ['system', 'info']):
        return ['Here is your System Information...', '\n'.join(systemInfo())]
    elif isContain(query, ['cpu', 'battery']):
        return batteryInfo()


from difflib import get_close_matches
import json
from random import choice
import webbrowser

data = json.load(open('extrafiles/websites.json', encoding='utf-8'))


def open_website(query):
    query = query.replace('open', '')
    if query in data:
        response = data[query]
    else:
        query = get_close_matches(query, data.keys(), n=2, cutoff=0.5)
        if len(query) == 0: return "None"
        response = choice(data[query[0]])
    webbrowser.open(response)


########################################################################################################################
########################################################################################################################

import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import smtplib
import urllib.request
import os


#from geopy.geocoders import Nominatim
#from geopy.distance import great_circle

class COVID:
    def __init__(self):
        self.total = 'Not Available'
        self.deaths = 'Not Available'
        self.recovered = 'Not Available'
        self.totalIndia = 'Not Available'
        self.deathsIndia = 'Not Available'
        self.recoveredIndia = 'Not Available'

    def covidUpdate(self):
        URL = 'https://www.worldometers.info/coronavirus/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.total, self.deaths, self.recovered = temp[0], temp[1], temp[2]

    def covidUpdateIndia(self):
        URL = 'https://www.worldometers.info/coronavirus/country/india/'
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        temp = []
        divs = soup.find_all('div', class_='maincounter-number')
        for div in divs:
            temp.append(div.text.strip())
        self.totalIndia, self.deathsIndia, self.recoveredIndia = temp[0], temp[1], temp[2]

    def totalCases(self, india_bool):
        if india_bool: return self.totalIndia
        return self.total

    def totalDeaths(self, india_bool):
        if india_bool: return self.deathsIndia
        return self.deaths

    def totalRecovery(self, india_bool):
        if india_bool: return self.recoveredIndia
        return self.recovered

    def symptoms(self):
        symt = ['1. Fever',
                '2. Coughing',
                '3. Shortness of breath',
                '4. Trouble breathing',
                '5. Fatigue',
                '6. Chills, sometimes with shaking',
                '7. Body aches',
                '8. Headache',
                '9. Sore throat',
                '10. Loss of smell or taste',
                '11. Nausea',
                '12. Diarrhea']
        return symt

    def prevention(self):
        prevention = ['1. Clean your hands often. Use soap and water, or an alcohol-based hand rub.',
                      '2. Maintain a safe distance from anyone who is coughing or sneezing.',
                      '3. Wear a mask when physical distancing is not possible.',
                      '4. Don’t touch your eyes, nose or mouth.',
                      '5. Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.',
                      '6. Stay home if you feel unwell.',
                      '7. If you have a fever, cough and difficulty breathing, seek medical attention.']
        return prevention


def wikiResult(query):
    query = query.replace('wikipedia', '')
    query = query.replace('search', '')
    if len(query.split()) == 0: query = "wikipedia"
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return "Desired Result Not Found"


class WEATHER:
    def __init__(self):
        # Currently in Lucknow, its 26 with Haze
        self.tempValue = ''
        self.city = ''
        self.currCondition = ''
        self.speakResult = ''

    def updateWeather(self):
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        # URL = 'https://weather.com/en-IN/weather/today/l/'+data['loc']
        URL = 'https://weather.com/en-IN/weather/today/'
        result = requests.get(URL)
        src = result.content

        soup = BeautifulSoup(src, 'html.parser')

        city = ""
        for h in soup.find_all('h1'):
            cty = h.text
            cty = cty.replace('Weather', '')
            self.city = cty[:cty.find(',')]
            break

        spans = soup.find_all('span')
        for span in spans:
            try:
                if span['data-testid'] == "TemperatureValue":
                    self.tempValue = span.text[:-1]
                    break
            except Exception as e:
                pass

        divs = soup.find_all('div', class_='CurrentConditions--phraseValue--2xXSr')
        for div in divs:
            self.currCondition = div.text
            break

    def weather(self):
        from datetime import datetime
        today = datetime.today().strftime('%A')
        self.speakResult = "Currently in " + self.city + ", its " + self.tempValue + " degree, with a " + self.currCondition
        return [self.tempValue, self.currCondition, today, self.city, self.speakResult]


c = COVID()
w = WEATHER()


def dataUpdate():
    c.covidUpdate()
    c.covidUpdateIndia()
    w.updateWeather()


##### WEATHER #####
def weather():
    return w.weather()


### COVID ###
def covid(query):
    if "india" in query:
        india_bool = True
    else:
        india_bool = False

    if "statistic" in query or 'report' in query:
        return ["Here are the statistics...",
                ["Total cases: " + c.totalCases(india_bool), "Total Recovery: " + c.totalRecovery(india_bool),
                 "Total Deaths: " + c.totalDeaths(india_bool)]]

    elif "symptom" in query:
        return ["Here are the Symptoms...", c.symptoms()]

    elif "prevent" in query or "measure" in query or "precaution" in query:
        return ["Here are the some of preventions from COVID-19:", c.prevention()]

    elif "recov" in query:
        return "Total Recovery is: " + c.totalRecovery(india_bool)

    elif "death" in query:
        return "Total Deaths are: " + c.totalDeaths(india_bool)

    else:
        return "Total Cases are: " + c.totalCases(india_bool)


def latestNews(news=5):
    URL = 'https://indianexpress.com/latest-news/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    headlineLinks = []
    headlines = []

    divs = soup.find_all('div', {'class': 'title'})

    count = 0
    for div in divs:
        count += 1
        if count > news:
            break
        a_tag = div.find('a')
        headlineLinks.append(a_tag.attrs['href'])
        headlines.append(a_tag.text)

    return headlines, headlineLinks


def maps(text):
    text = text.replace('maps', '')
    text = text.replace('map', '')
    text = text.replace('google', '')
    openWebsite('https://www.google.com/maps/place/' + text)


def giveDirections(startingPoint, destinationPoint):
    from geopy import Nominatim
    geolocator = Nominatim(user_agent='assistant')
    if 'current' in startingPoint:
        res = requests.get("https://ipinfo.io/")
        data = res.json()
        startinglocation = geolocator.reverse(data['loc'])
    else:
        startinglocation = geolocator.geocode(startingPoint)

    destinationlocation = geolocator.geocode(destinationPoint)
    startingPoint = startinglocation.address.replace(' ', '+')
    destinationPoint = destinationlocation.address.replace(' ', '+')

    openWebsite('https://www.google.co.in/maps/dir/' + startingPoint + '/' + destinationPoint + '/')

    startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)
    destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
    """total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km  # .mile
    return str(round(total_distance, 2)) + 'KM'"""


def openWebsite(url='https://www.google.com/'):
    webbrowser.open(url)


def jokes():
    URL = 'https://icanhazdadjoke.com/'
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    try:
        p = soup.find('p')
        return p.text
    except Exception as e:
        raise e


'''def youtube(query):
    from youtube_search import YoutubeSearch
    query = query.replace('play', ' ')
    query = query.replace('on youtube', ' ')
    query = query.replace('youtube', ' ')
    print("Pahuch Gya")
    results = YoutubeSearch(query, max_results=1).to_dict()
    print("Link mil gya")
    webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
    return "Enjoy Sir..."
'''

def googleSearch(query):
    if 'image' in query:
        query += "&tbm=isch"
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    webbrowser.open("https://www.google.com/search?q=" + query)
    return "Here you go..."


def sendWhatsapp(phone_no='', message=''):
    phone_no = '+91' + str(phone_no)
    webbrowser.open('https://web.whatsapp.com/send?phone=' + phone_no + '&text=' + message)
    import time
    from pynput.keyboard import Key, Controller
    time.sleep(10)
    k = Controller()
    k.press(Key.enter)

sender_address="rajeshgvr02@gmail.com"
sender_pass="Raj02@gvr"
def email(rec_email=None, text="Hello, It's G.O.S. here...", sub='G.O.S.'):
    if '@gmail.com' not in rec_email: return
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_address, sender_pass)  # eg, abc@gmail.com (email) and ****(pass)
    message = 'Subject: {}\n\n{}'.format(sub, text)
    s.sendmail("senderEmail", rec_email, message)
    print("Sent")
    s.quit()


def downloadImage(query, n=4):
    query = query.replace('images', '')
    query = query.replace('image', '')
    query = query.replace('search', '')
    query = query.replace('show', '')
    URL = "https://www.google.com/search?tbm=isch&q=" + query
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')
    imgTags = soup.find_all('img', class_='yWs4tf')  # old class name -> t0fcAb (Update this)

    if os.path.exists('Downloads') == False:
        os.mkdir('Downloads')

    count = 0
    for i in imgTags:
        if count == n: break
        try:
            urllib.request.urlretrieve(i['src'], 'Downloads/' + str(count) + '.jpg')
            count += 1
            print('Downloaded', count)
        except Exception as e:
            raise e


########################################################################################################################
########################################################################################################################

from difflib import get_close_matches
import json
from random import choice

data = json.load(open('extrafiles/dict_data.json', encoding='utf-8'))

def getMeaning(word):
	if word in data:
		return word, data[word], 1
	elif len(get_close_matches(word, data.keys())) > 0:
		word = get_close_matches(word, data.keys())[0]
		return word, data[word], 0
	else:
		return word, ["This word doesn't exists in the dictionary."], -1

def translate(query):
	query = query.replace('dictionary', '')
	if 'meaning' in query:
		ind = query.index('meaning of')
		word = query[ind+10:].strip().lower()
	elif 'definition' in query:
		try:
			ind = query.index('definition of')
			word = query[ind+13:].strip().lower()
		except:
			ind = query.index('definition')
			word = query[ind+10:].strip().lower()
	else: word = query

	word, result, check = getMeaning(word)
	result = choice(result)

	if check==1:
		return ["Here's the definition of \"" +word.capitalize()+ '"', result]
	elif check==0:
		return ["I think you're looking for \"" +word.capitalize()+ '"', "It's definition is,\n" + result]
	else:
		return [result, '']


########################################################################################################################
########################################################################################################################

from datetime import datetime
import os

file = "userData/toDoList.txt"


def createList():
    f = open(file, "w")
    present = datetime.now()
    dt_format = present.strftime("Date: " + "%d/%m/%Y" + " Time: " + "%H:%M:%S" + "\n")
    f.write(dt_format)
    f.close()


def toDoList(text):
    if os.path.isfile(file) == False:
        createList()

    f = open(file, "r")
    x = f.read(8)
    f.close()
    y = x[6:]
    yesterday = int(y)
    present = datetime.now()
    today = int(present.strftime("%d"))
    if (today - yesterday) >= 1:
        createList()
    f = open(file, "a")
    dt_format = present.strftime("%H:%M")
    print(dt_format)
    f.write(f"[{dt_format}] : {text}\n")
    f.close()


def showtoDoList():
    if os.path.isfile(file) == False:
        return ["It looks like that list is empty"]

    f = open(file, 'r')

    items = []
    for line in f.readlines():
        items.append(line.strip())

    speakList = [f"You have {len(items) - 1} items in your list:\n"]
    for i in items[1:]:
        speakList.append(i.capitalize())
    return speakList    


########################################################################################################################
########################################################################################################################

import subprocess
# import wmi
import os
import sys
import webbrowser

if os.path.exists('Files and Document') == False:
    os.mkdir('Files and Document')
path = 'Files and Document/'


def isContain(text, list):
    for word in list:
        if word in text:
            return True
    return False


def createFile(text):
    # change the applocation as per your system path
    appLocation = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"

    if isContain(text, ["ppt", "power point", "powerpoint"]):
        file_name = "sample_file.ppt"
        appLocation = "C:\\Program Files (x86)\\Microsoft Office\\Office15\\POWERPNT.exe"

    elif isContain(text, ['excel', 'spreadsheet']):
        file_name = "sample_file.xsl"
        appLocation = "C:\\Program Files (x86)\\Microsoft Office\\Office15\\EXCEL.EXE"

    elif isContain(text, ['word', 'document']):
        file_name = "sample_file.docx"
        appLocation = "C:\\Program Files (x86)\\Microsoft Office\\Office15\\WINWORD.EXE"

    elif isContain(text, ["text", "simple", "normal"]):
        file_name = "sample_file.txt"
    elif "python" in text:
        file_name = "sample_file.py"
    elif "css" in text:
        file_name = "sample_file.css"
    elif "javascript" in text:
        file_name = "sample_file.js"
    elif "html" in text:
        file_name = "sample_file.html"
    elif "c plus plus" in text or "c + +" in text:
        file_name = "sample_file.cpp"
    elif "java" in text:
        file_name = "sample_file.java"
    elif "json" in text:
        file_name = "sample_file.json"
    else:
        return "Unable to create this type of file"

    file = open(path + file_name, 'w')
    file.close()
    subprocess.Popen([appLocation, path + file_name])
    return "File is created.\nNow you can edit this file"


def CreateHTMLProject(project_name='Sample'):
    if os.path.isdir(path + project_name):
        webbrowser.open(os.getcwd() + '/' + path + project_name + "\\index.html")
        return 'There is a same project which is already created, look at this...'
    else:
        os.mkdir(path + project_name)

    os.mkdir(path + project_name + '/images')
    os.mkdir(path + project_name + '/videos')

    htmlContent = '<html>\n\t<head>\n\t\t<title> ' + project_name + ' </title>\n\t\t<link rel="stylesheet" type="text/css" href="style.css">\n\t</head>\n<body>\n\t<p id="label"></p>\n\t<button id="btn" onclick="showText()"> Click Me </button>\n\t<script src="script.js"></script>\n</body>\n</html>'

    htmlFile = open(path + project_name + '/index.html', 'w')
    htmlFile.write(htmlContent)
    htmlFile.close()

    cssContent = '* {\n\tmargin:0;\n\tpadding:0;\n}\nbody {\n\theight:100vh;\n\tdisplay:flex;\n\tjustify-content:center;\n\talign-items:center;\n}\n#btn {\n\twidth:200px;\n\tpadding: 20px 10px;\n\tborder-radius:5px;\n\tbackground-color:red;\n\tcolor:#fff;\n\toutline:none;border:none;\n}\np {\n\tfont-size:30px;\n}'

    cssFile = open(path + project_name + '/style.css', 'w')
    cssFile.write(cssContent)
    cssFile.close

    jsContent = 'function showText() {\n\tdocument.getElementById("label").innerHTML="Successfully Created ' + project_name + ' Project";\n\tdocument.getElementById("btn").style="background-color:green;"\n}'

    jsFile = open(path + project_name + '/script.js', 'w')
    jsFile.write(jsContent)
    jsFile.close()

    # change the applocation as per your system path
    appLocation = "C:\\Program Files\\Sublime Text 3\\sublime_text.exe"
    # subprocess.Popen([appLocation, path + project_name])
    subprocess.Popen([appLocation, path + project_name + "/index.html"])
    subprocess.Popen([appLocation, path + project_name + "/style.css"])
    subprocess.Popen([appLocation, path + project_name + "/script.js"])

    webbrowser.open(os.getcwd() + '/' + path + project_name + "\\index.html")

    return f'Successfully Created {project_name} Project'


########################################################################################################################
########################################################################################################################


import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        frames = []
        if isinstance(im, str):
            im = Image.open(im)

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

#demo :
#root = tk.Tk()
def gify():
    global lbl
    lbl = ImageLabel(root1,bg='black')
    lbl.place(x=36, y=570)
    lbl.load('extrafiles/images/textField.gif')
def del_click():
   lbl.after(1000, lbl.destroy())

########################################################################################################################
########################################################################################################################

import mysql.connector
from tkinter import *
import tkinter.messagebox

"""con = mysql.connector.connect(host="localhost",port='3308', user="root", password="", database="storedata")


def insert(com_name, data):
    res = con.cursor()
    sql = "insert into data (com_name,data) values (%s,%s)"
    user = (com_name, data)
    res.execute(sql, user)
    con.commit()
    print("Data Insert Success")
    tkinter.messagebox.showinfo("Success", "Data Insert Success")


def update(com_name, data, id):
    res = con.cursor()
    sql = "update data set com_name=%s,data=%s where id=%s"
    user = (com_name, data, id)
    res.execute(sql, user)
    con.commit()
    print("Data Update Success")
    tkinter.messagebox.showinfo("Success", "Data Update Success")


def select():
    res = con.cursor()
    sql = "SELECT id,com_name,data from data"
    res.execute(sql)
    result = res.fetchall()
    attachTOframe(result, True)
    #print(result)
    #Label(root, text=result).pack()


def delete(id):
    res = con.cursor()
    sql = "delete from data where id=%s"
    user = (id,)
    res.execute(sql, user)
    con.commit()
    print("Data Delete")


def database1():
        print("1.Insert Data")
        print("2.Update Data")
        print("3.Select Data")
        print("4.Delete Data")
        print("5.Exit")
        listofdata=(
            "1.Insert Data\n",
            "2.Update Data\n",
            "3.Select Data\n",
            "4.Delete Data\n",
            "5.Exit"
        )
        attachTOframe(listofdata,True)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(" I am Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            print('Recognizing.....')
            said = r.recognize_google(audio)
            choice=said
            if choice == 'insert':
                speak('say subject or company')
                com_name = record()
                speak('say data or password')
                data = record()
                insert(com_name, data)
                speak('Successfully updated')
            elif choice == 'update':
                speak('say id')
                id = record()
                speak('say subject or company')
                com_name = record()
                speak('say data or password')
                data = record()
                update(com_name, data, id)
                speak('Successfully updated')
            elif choice == 'select':
                speak('select the table')
                select()
            elif choice == 'delete':
                speak('say id')
                id = record()
                delete(id)
                speak('deleted')
            elif choice == 'exit':
                quit()
            else:
                print("Invalid Selection . Please Try Again !")
        except:
            return 'None'"""

########################################################################################################################
########################################################################################################################

########################################################################################################################
########################################################################################################################
from PIL import Image, ImageTk, ImageGrab
import cv2
import numpy as np
import threading

p = ImageGrab.grab()
a, b = p.size
filename=(f'temp_vid.mp4')
fourcc = cv2.VideoWriter_fourcc(*'X264')
frame_rate = 10
out = cv2.VideoWriter()

def screen_capturing():

    global capturing
    capturing = True

    while capturing:

        img = ImageGrab.grab()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)

def start_screen_capturing():

    if not out.isOpened():

        out.open(filename,fourcc, frame_rate,(a,b))
    speak('start recording')
    print(' rec started')
    t1=threading.Thread(target=screen_capturing, daemon=True)
    t1.start()

def stop_screen_capturing():
    global capturing
    capturing = False
    out.release()
    speak('recording completed successfully')
    print('complete')

########################################################################################################################
########################################################################################################################
#########################
# GLOBAL VARIABLES USED #
#########################
ai_name = 'G.O.S.:'.lower()
EXIT_COMMANDS = ['bye', 'exit', 'quit', 'shut down', 'shutdown']

rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "black"
botChatText = "white"
userChatTextBg = "black"
btncolor = 'black'


chatBgColor = 'black'
background = 'black'
textColor = 'white'
AITaskStatusLblBG = 'black'
KCS_IMG = 1  # 0 for light, 1 for dark
voice_id = 0  # 0 for female, 1 for male
ass_volume = 1  # max volume
ass_voiceRate = 200  # normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
    #import normalChat
    #import math_function
    import appControl
    #import webScrapping
    #import game
    #from userHandler import UserData
    import timer
    from FACE_UNLOCKER import clickPhoto, viewPhoto
    #import dictionary
    #import ToDo
    #import fileHandler
except Exception as e:
    raise e

""" System Modules """
try:
    import os
    import speech_recognition as sr
    import pyttsx3
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import colorchooser
    from PIL import Image, ImageTk, ImageGrab
    from time import sleep
    from threading import Thread
except Exception as e:
    print(e)

########################################## LOGIN CHECK ##############################################
try:
    user = UserData()
    user.extractData()
    ownerName = user.getName().split()[0]
    ownerDesignation = "Sir"
    if user.getGender() == "Female": ownerDesignation = "Ma'am"
    ownerPhoto = user.getUserPhoto()
except Exception as e:
    print("You're not Registered Yet !\nSo please register your Account.")
    raise SystemExit

########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
    import pickle
    global background, textColor, chatBgColor,btncolor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
    setting = {'background': background,
               'textColor': textColor,
               'chatBgColor': chatBgColor,
               'btncolor':btncolor,
               'AITaskStatusLblBG': AITaskStatusLblBG,
               'KCS_IMG': KCS_IMG,
               'botChatText': botChatText,
               'botChatTextBg': botChatTextBg,
               'userChatTextBg': userChatTextBg,
               'voice_id': voice_id,
               'ass_volume': ass_volume,
               'ass_voiceRate': ass_voiceRate
               }
    if write:
        with open('userData/settings.pck', 'wb') as file:
            pickle.dump(setting, file)
        return
    try:
        with open('userData/settings.pck', 'rb') as file:
            loadSettings = pickle.load(file)
            background = loadSettings['background']
            textColor = loadSettings['textColor']
            chatBgColor = loadSettings['chatBgColor']
            AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
            KCS_IMG = loadSettings['KCS_IMG']
            botChatText = loadSettings['botChatText']
            botChatTextBg = loadSettings['botChatTextBg']
            userChatTextBg = loadSettings['userChatTextBg']
            voice_id = loadSettings['voice_id']
            ass_volume = loadSettings['ass_volume']
            ass_voiceRate = loadSettings['ass_voiceRate']
    except Exception as e:
        pass


if os.path.exists('userData/settings.pck') == False:
    ChangeSettings(True)

def getChatColor():
    global chatBgColor
    chatBgColor = myColor[1]
    colorbar['bg'] = chatBgColor
    chat_frame['bg'] = chatBgColor
    root1['bg'] = chatBgColor


def changeTheme():
    global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText,btncolor,botChatTextBg, userChatTextBg, chatBgColor
    if themeValue.get() == 1:
        background, textColor, AITaskStatusLblBG,btncolor, KCS_IMG = "black", "white", "black",'black', 1
        cbl['image'] = cblDarkImg
        #kbBtn['image'] = kbphDark
        settingBtn['image'] = sphDark
        AITaskStatusLbl['bg'] = AITaskStatusLblBG
        botChatText, botChatTextBg, userChatTextBg = "white", "black", "black"
        chatBgColor = "black"
        colorbar['bg'] = chatBgColor
    else:
        background, textColor, AITaskStatusLblBG,btncolor, KCS_IMG = "white", "black", "black",'black', 0
        cbl['image'] = cblLightImg
        #kbBtn['image'] = kbphLight
        settingBtn['image'] = sphLight
        AITaskStatusLbl['bg'] = AITaskStatusLblBG
        botChatText, botChatTextBg, userChatTextBg = "black", "white", "white"
        chatBgColor = "white"
        colorbar['bg'] = '#E8EBEF'

    root['bg'], root2['bg'] = background, background
    settingsFrame['bg'] = background
    settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl[
        'fg'], chooseChatLbl[
        'fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
    settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl[
        'bg'], chooseChatLbl[
        'bg'] = background, background, background, background, background, background, background, background
    s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
    volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
    chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
    userPhoto['activebackground'] = background
    ChangeSettings(True)


def changeVoice(e):
    global voice_id
    voice_id = 0
    if assVoiceOption.get() == 'Male': voice_id = 1
    engine.setProperty('voice', voices[voice_id].id)
    ChangeSettings(True)


def changeVolume(e):
    global ass_volume
    ass_volume = volumeBar.get() / 100
    engine.setProperty('volume', ass_volume)
    ChangeSettings(True)


def changeVoiceRate(e):
    global ass_voiceRate
    temp = voiceOption.get()
    if temp == 'Very Low':
        ass_voiceRate = 100
    elif temp == 'Low':
        ass_voiceRate = 150
    elif temp == 'Fast':
        ass_voiceRate = 250
    elif temp == 'Very Fast':
        ass_voiceRate = 300
    else:
        ass_voiceRate = 200
    print(ass_voiceRate)
    engine.setProperty('rate', ass_voiceRate)
    ChangeSettings(True)


ChangeSettings()

############################################ SET UP VOICE ###########################################
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)  # male
    engine.setProperty('volume', ass_volume)
except Exception as e:
    print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='e', pady=0)
    if display: attachTOframe(text, True)
    print('\n' + ai_name.upper() + ': ' + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Try not to type more...")


####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
    Process(target=gify())
    print('\nListening...')
    AITaskStatusLbl['text'] = 'Listening...'
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    #Process(target=del_click())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            #gify()
            #Process(target=gify())
            AITaskStatusLbl['text'] = 'Processing...'
            Process(target=del_click())
            said = r.recognize_google(audio)
            print(f"\nUser said: {said}")
            #os.remove(gifer)
            #os.remove(lbl)

            if clearChat:
                clearChatScreen()
                pass
            if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
            attachTOframe(said)

        except Exception as e:
            print(e)
            # speak("I didn't get it, Say that again please...")
            if "connection failed" in str(e):
                speak("Your System is Offline...", True, True)
            return 'None'
    return said.lower()


def voiceMedium():
    while True:
        query = record()
        if query == 'None': continue
        if isContain(query, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
            break
        else:
            main(query.lower())
    Win_Opt('close')

def keyboardInput(e):
    user_input = UserField.get().lower()
    if user_input != "":
        clearChatScreen()

        if isContain(user_input, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye " + ownerDesignation + "!", True, True)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e', pady=0)
            attachTOframe(user_input.capitalize())
            Thread(target=main, args=(user_input,)).start()
        UserField.delete(0, END)

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False

import cv2
import numpy as np
import os
from os.path import isfile, join

def clickPhoto():
    global imageName
    if os.path.exists('Camera') == False:
        os.mkdir('Camera')

    from time import sleep
    import playsound
    from datetime import datetime

    cam = cv2.VideoCapture(0)
    _, frame = cam.read()
    playsound.playsound('extrafiles/audios/photoclick.mp3')
    imageName = 'Camera/Camera_' + str(datetime.now())[:19].replace(':', '_') + '.png'
    cv2.imwrite(imageName, frame)
    cam.release()
    cv2.destroyAllWindows()


def viewPhoto():
    from PIL import Image
    img = Image.open(imageName)
    img.show()


def main(text):
    if "project" in text:
        if isContain(text, ['make', 'create']):
            speak("What do you want to give the project name ?", True, True)
            projectName = record(False, False)
            speak(CreateHTMLProject(projectName.capitalize()), True)
            return

    if "create" in text and "file" in text:
        speak(createFile(text), True, True)
        return
    if 'start screen record' in text:
        start_screen_capturing()
        return
    if 'stop recording' in text:
        stop_screen_capturing()
        return

    if "translate" in text:
        speak("What do you want to translate?", True, True)
        sentence = record(False, False)
        speak("Which langauage to translate ?", True)
        langauage = record(False, False)
        result = lang_translate(sentence, langauage)
        if result == "None":
            speak("This langauage doesn't exists")
        else:
            speak(f"In {langauage.capitalize()} you would say:", True)
            if langauage == "hindi":
                attachTOframe(result.text, True)
                speak(result.pronunciation)
            else:
                speak(result.text, True)
        return

    if 'list' in text:
        if isContain(text, ['add', 'create', 'make']):
            speak("What do you want to add?", True, True)
            item = record(False, False)
            toDoList(item)
            speak("Alright, I added to your list", True)
            return
        if isContain(text, ['show', 'my list']):
            items = showtoDoList()
            if len(items) == 1:
                speak(items[0], True, True)
                return
            attachTOframe('\n'.join(items), True)
            speak(items[0])
            return

    if isContain(text, ['battery', 'system info']):
        result = OSHandler(text)
        if len(result) == 2:
            speak(result[0], True, True)
            attachTOframe(result[1], True)
        else:
            speak(result, True, True)
        return

    if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
        result = translate(text)
        speak(result[0], True, True)
        if result[1] == '': return
        speak(result[1], True)
        return

    if 'selfie' in text or ('click' in text and 'photo' in text):
        speak("Sure " + ownerDesignation + "...", True, True)
        clickPhoto()
        speak('Do you want to view your clicked photo?', True)
        query = record(False)
        if isContain(query, ['yes', 'sure', 'yeah', 'show me']):
            Thread(target=viewPhoto).start()
            speak("Ok, here you go...", True, True)
        else:
            speak("No Problem " + ownerDesignation, True, True)
        return

    if 'volume' in text:
        volumeControl(text)
        Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w', pady=0)
        attachTOframe('Volume Settings Changed', True)
        return

    if isContain(text, ['timer', 'countdown']):
        Thread(target=timer.startTimer, args=(text,)).start()
        speak('Ok, Timer Started!', True, True)
        return

    if 'whatsapp' in text:
        speak("Sure " + ownerDesignation + "...", True, True)
        speak('Whom do you want to send the message?', True)
        WAEMPOPUP("WhatsApp", "Phone Number")
        attachTOframe(rec_phoneno)
        speak('What is the message?', True)
        message = record(False, False)
        Thread(target=sendWhatsapp, args=(rec_phoneno, message,)).start()
        speak("Message is on the way. Do not move away from the screen.")
        attachTOframe("Message Sent", True)
        return

    """if 'database' in text:
        speak('opening database')
        database1()"""

    if 'email' in text:
        speak('Whom do you want to send the email?', True, True)
        WAEMPOPUP("Email", "E-mail Address")
        attachTOframe(rec_email)
        speak('What is the Subject?', True)
        subject = record(False, False)
        speak('What message you want to send ?', True)
        message = record(False, False)
        Thread(target=email, args=(rec_email, message, subject,)).start()
        speak('Email has been Sent', True)
        return

    if isContain(text, ['covid', 'virus']):
        result = covid(text)
        if 'str' in str(type(result)):
            speak(result, True, True)
            return
        speak(result[0], True, True)
        result = '\n'.join(result[1])
        attachTOframe(result, True)
        return

    '''if isContain(text, ['youtube', 'video']):
        speak("Ok " + ownerDesignation + ", here a video for you...", True, True)
        try:
            speak(youtube(text), True)
        except Exception as e:
            speak("Desired Result Not Found", True)
        return'''

    if isContain(text, ['search', 'image']):
        if 'image' in text and 'show' in text:
            Thread(target=showImages, args=(text,)).start()
            speak('Here are the images...', True, True)
            return
        speak(googleSearch(text), True, True)
        return

    if isContain(text, ['map', 'direction']):
        if "direction" in text:
            speak('What is your starting location?', True, True)
            startingPoint = record(False, False)
            speak("Ok " + ownerDesignation + ", Where you want to go?", True)
            destinationPoint = record(False, False)
            speak("Ok " + ownerDesignation + ", Getting Directions...", True)
            try:
                distance = giveDirections(startingPoint, destinationPoint)
                speak('You have to cover a distance of ' + distance, True)
            except:
                speak("I think location is not proper, Try Again!")
        else:
            maps(text)
            speak('Here you go...', True, True)
        return

    if isContain(text, ['factorial', 'log', 'value of', 'math', ' + ', ' - ', ' x ', 'multiply', 'divided by', 'binary',
                        'hexadecimal', 'octal', 'shift', 'sin ', 'cos ', 'tan ']):
        try:
            speak(('Result is: ' + perform(text)), True, True)
        except Exception as e:
            return
        return

    if "joke" in text:
        speak('Here is a joke...', True, True)
        speak(jokes(), True)
        return

    if isContain(text, ['news']):
        speak('Getting the latest news...', True, True)
        headlines, headlineLinks = latestNews(2)
        for head in headlines: speak(head, True)
        speak('Do you want to read the full news?', True)
        text = record(False, False)
        if isContain(text, ["no", "don't"]):
            speak("No Problem " + ownerDesignation, True)
        else:
            speak("Ok " + ownerDesignation + ", Opening browser...", True)
            openWebsite('https://indianexpress.com/latest-news/')
            speak("You can now read the full news from this website.")
        return

    if isContain(text, ['weather']):
        data = weather()
        speak('', False, True)
        showSingleImage("weather", data[:-1])
        speak(data[-1])
        return

    if isContain(text, ['screenshot']):
        Thread(target=Win_Opt, args=('screenshot',)).start()
        speak("Screen Shot Taken", True, True)
        return

    if isContain(text, ['window', 'close that']):
        Win_Opt(text)
        return

    if isContain(text, ['tab']):
        Tab_Opt(text)
        return

    if isContain(text, ['setting']):
        raise_frame(root2)
        clearChatScreen()
        return

    if isContain(text, ['open', 'type', 'save', 'delete', 'select', 'press enter']):
        System_Opt(text)
        return

    if isContain(text, ['wiki', 'who is']):
        Thread(target=downloadImage, args=(text, 1,)).start()
        speak('Searching...', True, True)
        result = wikiResult(text)
        showSingleImage('wiki')
        speak(result, True)
        return

    """if isContain(text, ['game']):
        speak("Which game do you want to play?", True, True)
        attachTOframe(game.showGames(), True)
        text = record(False)
        if text == "None":
            speak("Didn't understand what you say?", True, True)
            return
        if 'online' in text:
            speak("Ok " + ownerDesignation + ", Let's play some online games", True, True)
            openWebsite('https://www.agame.com/games/mini-games/')
            return
        if isContain(text, ["don't", "no", "cancel", "back", "never"]):
            speak("No Problem " + ownerDesignation + ", We'll play next time.", True, True)
        else:
            speak("Ok " + ownerDesignation + ", Let's Play " + text, True, True)
            os.system(f"python -c \"import game; game.play('{text}')\"")
        return

    if isContain(text, ['coin', 'dice', 'die']):
        if "toss" in text or "roll" in text or "flip" in text:
            speak("Ok " + ownerDesignation, True, True)
            result = play(text)
            if "Head" in result:
                showSingleImage('head')
            elif "Tail" in result:
                showSingleImage('tail')
            else:
                showSingleImage(result[-1])
            speak(result)
            return"""

    if isContain(text, ['time', 'date']):
        speak(chat(text), True, True)
        return

    """if isContain(text, ['database', 'data']):
        database1()
        return"""

    if 'my name' in text:
        speak('Your name is, ' + ownerName, True, True)
        return

    if isContain(text, ['voice']):
        global voice_id
        try:
            if 'female' in text:
                voice_id = 0
            elif 'male' in text:
                voice_id = 1
            else:
                if voice_id == 0:
                    voice_id = 1
                else:
                    voice_id = 0
            engine.setProperty('voice', voices[voice_id].id)
            ChangeSettings(True)
            speak("Hello " + ownerDesignation + ", I have changed my voice. How may I help you?", True, True)
            assVoiceOption.current(voice_id)
        except Exception as e:
            print(e)
        return

    if isContain(text, ['morning', 'evening', 'noon']) and 'good' in text:
        speak(chat("good"), True, True)
        return

    result = reply(text)
    if result != "None":
        speak(result, True, True)
    else:
        speak("Here's what I found on the web... ", True, True)
        googleSearch(text)


##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
    result = messagebox.askquestion('Alert', 'Are you sure you want to delete your Face Data ?')
    if result == 'no': return
    messagebox.showinfo('Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
    import shutil
    shutil.rmtree('userData')
    root.destroy()


#####################
####### GUI #########
#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text, bot=False):
    global botchat,userchat
    if bot:
        botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250,
                        font=('Montserrat', 9, 'bold'))
        botchat.pack(anchor='e', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='red', justify=RIGHT, wraplength=250,
                         font=('Montserrat', 9, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)

from ttkwidgets.font import askfont

'''def font():
    res = askfont()
    if res[0] is not None:
        botchat.configure(font=res[0])
        userchat.configure(font=res[0])
        labels.configure(font=res[0])
    # print(res)'''

# window = tk.Tk()

def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()


### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()
    clearChatScreen()


################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None


def showSingleImage(type, data=None):
    global img0, img1, img2, img3, img4
    try:
        img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90, 110), Image.ANTIALIAS))
    except:
        pass
    img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220, 200), Image.ANTIALIAS))
    img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220, 200), Image.ANTIALIAS))
    img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

    if type == "weather":
        weather = Frame(chat_frame)
        weather.pack(anchor='e')
        Label(weather, image=img4, bg=chatBgColor).pack()
        Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65, y=45)
        Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78, y=110)
        Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78, y=140)
        Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60, y=160)

    elif type == "wiki":
        Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='e')
    elif type == "head":
        Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='e')
    elif type == "tail":
        Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='e')
    else:
        img3 = ImageTk.PhotoImage(
            Image.open('extrafiles/images/dice/' + type + '.jpg').resize((200, 200), Image.ANTIALIAS))
        Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')


def showImages(query):
    global img0, img1, img2, img3
    downloadImage(query)
    w, h = 150, 110
    # Showing Images
    imageContainer = Frame(chat_frame, bg='#EAEAEA')
    imageContainer.pack(anchor='e')
    # loading images
    img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w, h), Image.ANTIALIAS))
    img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w, h), Image.ANTIALIAS))
    img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w, h), Image.ANTIALIAS))
    img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w, h), Image.ANTIALIAS))
    # Displaying
    Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
    Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
    Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
    Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
    global rec_phoneno, rec_email
    data = WAEMEntry.get()
    rec_email, rec_phoneno = data, data
    WAEMEntry.delete(0, END)
    Win_Opt('close')


def send(e):
    sendWAEM()


def WAEMPOPUP(Service='None', rec='Reciever'):
    global WAEMEntry
    PopUProot = Tk()
    PopUProot.title(f'{Service} Service')
    PopUProot.configure(bg='white')

    if Service == "WhatsApp":
        PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
    else:
        PopUProot.iconbitmap("extrafiles/images/email.ico")
    w_width, w_height = 410, 200
    s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    PopUProot.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))  # center location of the screen
    Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
    WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
    WAEMEntry.pack()
    WAEMEntry.focus()

    SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white',
                     command=sendWAEM)
    SendBtn.pack(pady=20, ipadx=10)
    PopUProot.bind('<Return>', send)
    PopUProot.mainloop()


######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
    global chatBgColor
    global myColor
    myColor = colorchooser.askcolor()
    if myColor[1] is None: return
    chatBgColor = myColor[1]
    colorbar['bg'] = chatBgColor
    chat_frame['bg'] = chatBgColor
    root1['bg'] = chatBgColor
    ChangeSettings(True)


chatMode = 1


def changeChatMode():
    global chatMode
    if chatMode == 1:
        appControl.volumeControl('mute')
        VoiceModeFrame.pack_forget()
        TextModeFrame.pack(fill=BOTH)
        UserField.focus()
        chatMode = 0
    else:

        appControl.volumeControl('full')
        TextModeFrame.pack_forget()
        VoiceModeFrame.pack(fill=BOTH)
        root.focus()
        chatMode = 1
from tkinter import filedialog

def add_photo():
    image_path = filedialog.askopenfilename()
    image_name = os.path.basename(image_path)
    image_extension = image_name[image_name.rfind('.')+1:]

    if image_path:
        user_image = Image.open(image_path)
        user_image = user_image.resize((150, 140), Image.ANTIALIAS)
        user_image.save('resized'+image_name)
        user_image.close()

        image_path = 'resized'+image_name
        user_image = Image.open(image_path)

        user_image = ImageTk.PhotoImage(user_image)
        #profile_label.image = user_image
        #profile_label.config(image=user_image)

#####################################################################################################
########################################################################################################
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from pynput.keyboard import Key, Controller
import userHandler
from userHandler import UserData

def selectpics():
    u = UserData()
    u.extractData()
    avatarChoosen = u.getUserPhoto()


    def closeWindow():
        keyboard = Controller()
        keyboard.press(Key.alt_l)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt_l)


    def SavePhoto():
        userHandler.UpdateUserPhoto(avatarChoosen)
        closeWindow()


    def selectAVATAR(avt=0):
        global avatarChoosen
        avatarChoosen = avt

        i = 1
        for avtr in (
        avtb1, avtb2, avtb3, avtb4, avtb5, avtb6, avtb7, avtb8, avtb9, avtb10, avtb11, avtb12, avtb13, avtb14, avtb15):
            if i == avt:
                avtr['state'] = 'disabled'
            else:
                avtr['state'] = 'normal'
            i += 1


    background = '#F6FAFB'
    avtrRoot = Tk()
    avtrRoot.title("Choose Avatar")
    avtrRoot.configure(bg=background)
    w_width, w_height = 500, 450
    s_width, s_height = avtrRoot.winfo_screenwidth(), avtrRoot.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    avtrRoot.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))

    Label(avtrRoot, text="Choose Your Avatar", font=('arial bold', 15), bg=background, fg='#303E54').pack(pady=10)

    avatarContainer = Frame(avtrRoot, bg=background)
    avatarContainer.pack(pady=10, ipadx=50, ipady=20)
    size = 100

    # create a main frame
    main_frame = Frame(avatarContainer)
    main_frame.pack(fill=BOTH, expand=1)

    # create a canvas
    my_canvas = Canvas(main_frame, bg=background)
    my_canvas.pack(side=LEFT, expand=1, fill=BOTH)

    # add a scrollbar to the canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    # configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    # create another frame inside the canvas
    second_frame = Frame(my_canvas)

    # add that new frame to a window in the canvas
    my_canvas.create_window((0, 0), window=second_frame, anchor='nw')

    avtr1 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a1.png').resize((size, size)), Image.ANTIALIAS)
    avtr2 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a2.png').resize((size, size)), Image.ANTIALIAS)
    avtr3 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a3.png').resize((size, size)), Image.ANTIALIAS)
    avtr4 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a4.png').resize((size, size)), Image.ANTIALIAS)
    avtr5 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a5.png').resize((size, size)), Image.ANTIALIAS)
    avtr6 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a6.png').resize((size, size)), Image.ANTIALIAS)
    avtr7 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a7.png').resize((size, size)), Image.ANTIALIAS)
    avtr8 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a8.png').resize((size, size)), Image.ANTIALIAS)
    avtr9 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a9.png').resize((size, size)), Image.ANTIALIAS)
    avtr10 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a10.png').resize((size, size)), Image.ANTIALIAS)
    avtr11 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a11.png').resize((size, size)), Image.ANTIALIAS)
    avtr12 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a12.png').resize((size, size)), Image.ANTIALIAS)
    avtr13 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a13.png').resize((size, size)), Image.ANTIALIAS)
    avtr14 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a14.png').resize((size, size)), Image.ANTIALIAS)
    avtr15 = ImageTk.PhotoImage(Image.open('extrafiles/images/avatars/a15.png').resize((size, size)), Image.ANTIALIAS)

    avtb1 = Button(second_frame, image=avtr1, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(1))
    avtb2 = Button(second_frame, image=avtr2, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(2))
    avtb3 = Button(second_frame, image=avtr3, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(3))
    avtb4 = Button(second_frame, image=avtr4, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(4))
    avtb5 = Button(second_frame, image=avtr5, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(5))
    avtb6 = Button(second_frame, image=avtr6, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(6))
    avtb7 = Button(second_frame, image=avtr7, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(7))
    avtb8 = Button(second_frame, image=avtr8, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(8))
    avtb9 = Button(second_frame, image=avtr9, bg=background, activebackground=background, relief=FLAT, bd=0,
                   command=lambda: selectAVATAR(9))
    avtb10 = Button(second_frame, image=avtr10, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(10))
    avtb11 = Button(second_frame, image=avtr11, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(11))
    avtb12 = Button(second_frame, image=avtr12, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(12))
    avtb13 = Button(second_frame, image=avtr13, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(13))
    avtb14 = Button(second_frame, image=avtr14, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(14))
    avtb15 = Button(second_frame, image=avtr15, bg=background, activebackground=background, relief=FLAT, bd=0,
                    command=lambda: selectAVATAR(15))

    avtb1.grid(row=0, column=0, ipadx=25, ipady=10)
    avtb2.grid(row=0, column=1, ipadx=25, ipady=10)
    avtb3.grid(row=0, column=2, ipadx=25, ipady=10)
    avtb4.grid(row=1, column=0, ipadx=25, ipady=10)
    avtb5.grid(row=1, column=1, ipadx=25, ipady=10)
    avtb6.grid(row=1, column=2, ipadx=25, ipady=10)
    avtb7.grid(row=2, column=0, ipadx=25, ipady=10)
    avtb8.grid(row=2, column=1, ipadx=25, ipady=10)
    avtb9.grid(row=2, column=2, ipadx=25, ipady=10)
    avtb10.grid(row=3, column=0, ipadx=25, ipady=10)
    avtb11.grid(row=3, column=1, ipadx=25, ipady=10)
    avtb12.grid(row=3, column=2, ipadx=25, ipady=10)
    avtb13.grid(row=4, column=0, ipadx=25, ipady=10)
    avtb14.grid(row=4, column=1, ipadx=25, ipady=10)
    avtb15.grid(row=4, column=2, ipadx=25, ipady=10)

    BottomFrame = Frame(avtrRoot, bg=background)
    BottomFrame.pack(pady=10)
    Button(BottomFrame, text='         Update         ', font=('Montserrat Bold', 15), bg='#01933B', fg='white', bd=0,
           relief=FLAT, command=SavePhoto).grid(row=0, column=0, padx=10)
    Button(BottomFrame, text='         Cancel         ', font=('Montserrat Bold', 15), bg='#EDEDED', fg='#3A3834', bd=0,
           relief=FLAT, command=closeWindow).grid(row=0, column=1, padx=10)

    avtrRoot.iconbitmap("extrafiles/images/changeProfile.ico")
    avtrRoot.mainloop()

#####################################################################################################
########################################################################################################


############################################## GUI #############################################

def onhover(e):
    userPhoto['image'] = chngPh


def onleave(e):
    userPhoto['image'] = userProfileImg


from ChooseAvatarPIC import *
def UpdateIMAGE():
    global ownerPhoto, userProfileImg, userIcon


    os.system('python ChooseAvatarPIC.py')
    #os.system('ChooseAvatarPIC.exe')
    u = UserData()
    u.extractData()
    ownerPhoto = u.getUserPhoto()
    userProfileImg = ImageTk.PhotoImage(
        Image.open("extrafiles/images/avatars/a" + str(ownerPhoto) + ".png").resize((120, 120)))

    userPhoto['image'] = userProfileImg
    userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a" + str(ownerPhoto) + ".png")


def SelectAvatar():
    Thread(target=UpdateIMAGE).start()


#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
    progress_bar = ttk.Progressbar(splash_root, style="white.Horizontal.TProgressbar", orient="horizontal",
                                   mode="determinate", length=303)
    progress_bar.pack()
    splash_root.update()
    progress_bar['value'] = 0
    splash_root.update()

    while progress_bar['value'] < 100:
        progress_bar['value'] += 5
        # splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
        splash_root.update()
        sleep(0.5)


def destroySplash():
    splash_root.destroy()


if __name__ == '__main__':
    splash_root = Tk()
    splash_root.configure(bg='#3895d3')
    splash_root.overrideredirect(True)
    photos = PhotoImage(file="splash.png")
    splash_label = Label(splash_root,image=photos, text="Processing...", font=('montserrat', 15), bg='#3895d3', fg='white')
    splash_label.pack()
    #splash_percentage_label = Label(splash_label, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
    #splash_percentage_label.pack(pady=(0,10))

    w_width, w_height = 400, 650
    s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    splash_root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))

    progressbar()
    splash_root.after(10, destroySplash)
    splash_root.mainloop()

    root = Tk()

    root.title('G.O.S')
    w_width, w_height = 400, 680
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width / 2) - (w_width / 2), (s_height / 2) - (w_height / 2)
    root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y - 30))  # center location of the screen
    root.configure(bg=background)
    # root.resizable(width=False, height=False)
    root.pack_propagate(0)

    root1 = Frame(root, bg='black')
    root2 = Frame(root, bg='black')
    root3 = Frame(root, bg='black')
    root4 = Frame(root, bg='black')

    for f in (root1, root2, root3, root4):
        f.grid(row=0, column=0, sticky='news')

    ################################
    ########  CHAT SCREEN  #########
    ################################

    # Chat Frame
    chat_frame = Frame(root1, width=380, height=551, bg=chatBgColor)
    chat_frame.pack(padx=10)
    chat_frame.pack_propagate(0)

    bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
    bottomFrame1.pack(fill=X, side=BOTTOM)
    VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    VoiceModeFrame.pack(fill=BOTH)
    TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    TextModeFrame.pack(fill=BOTH)

    # VoiceModeFrame.pack_forget()
    TextModeFrame.pack_forget()

    cblLightImg = PhotoImage(file='extrafiles/images/centralbtn.png')
    cblDarkImg = PhotoImage(file='extrafiles/images/centralbtn.png')
    if KCS_IMG == 1:
        cblimage = cblDarkImg
    else:
        cblimage = cblLightImg
    cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
    cbl.pack(pady=6)
    AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG,
                            font=('montserrat', 16))
    AITaskStatusLbl.place(x=140, y=32)



    color = {"nero": "#252726", "orange": "#FF8700", "darkorange": "#FE6101"}

    # setting switch state:
    btnState = False

    # loading Navbar icon image:
    navIcon = PhotoImage(file="extrafiles/images/keyboard2.png")
    closeIcon = PhotoImage(file="extrafiles/images/exit.png")


    # setting switch function:
    def switch():
        global btnState
        if btnState is True:
            # create animated Navbar closing:
            for x in range(301):
                navRoot.place(x=-x, y=0)
                topFrame.update()

            # resetting widget colors:
            #brandLabel.config(bg="gray17", fg="green")
            homeLabel.config(bg=chatBgColor)
            topFrame.config(bg=chatBgColor)
            #root.config(bg="gray17")

            # turning button OFF:
            btnState = False
        else:
            # make root dim:
            #brandLabel.config(bg=color["nero"], fg="#5F5A33")
            homeLabel.config(bg=chatBgColor)
            topFrame.config(bg=chatBgColor)
            #root.config(bg=color["nero"])

            # created animated Navbar opening
            for x in range(-300, 0):
                navRoot.place(x=x, y=0)
                topFrame.update()

            # turing button ON:
            btnState = True


    # top Navigation bar:
    topFrame = Frame(root1, bg=chatBgColor)
    #topFrame.pack(side="top", fill=tk.X)
    topFrame.place(x=0,y=0)

    # Header label text:
    homeLabel = Label(topFrame, font="Bahnschrift 15", height=2, padx=20,bg=chatBgColor,width=2)
    homeLabel.pack(side="top")

    # Main label text:
    #brandLabel = tk.Label(root4, text="Pythonista\nEmpire", font="System 30", bg="gray17", fg="green")
    #brandLabel.place(x=100, y=250)

    # Navbar button:
    navbarBtn = Button(topFrame, image=navIcon, bg=chatBgColor, activebackground=chatBgColor, bd=0, padx=20,
                          command=switch)
    navbarBtn.place(x=0, y=0)

    # setting Navbar frame:
    navRoot = Frame(root1, height=60, width=300, bg='white')
    navRoot.place(x=-300, y=0)

    # Navbar Close Button:
    closeBtn = Button(navRoot, image=closeIcon, bg='white', activebackground=chatBgColor, bd=0,
                         command=switch)
    closeBtn.place(x=250, y=8)

    # Settings Button
    sphLight = PhotoImage(file="extrafiles/images/settings.png")
    sphLight = sphLight.subsample(2, 2)
    sphDark = PhotoImage(file="extrafiles/images/settings.png")
    sphDark = sphDark.subsample(2, 2)
    if KCS_IMG == 1:
        sphimage = sphDark
    else:
        sphimage = sphLight
    settingBtn = Button(root1, image=sphimage, height=30, width=30, bg=btncolor, borderwidth=0,
                        activebackground=btncolor, command=lambda: raise_frame(root2))
    settingBtn.place(relx=1.0, y=500, x=-20, anchor="ne")

    # Keyboard Button
    """
    kbphLight = PhotoImage(file="extrafiles/images/keyboard2.png")
    kbphLight = kbphLight.subsample(2, 2)
    kbphDark = PhotoImage(file="extrafiles/images/keyboard2.png")
    kbphDark = kbphDark.subsample(2, 2)
    if KCS_IMG == 1:
        kbphimage = kbphDark
    else:
        kbphimage = kbphLight
    kbBtn = Button(root1, image=kbphimage, height=30, width=30, bg=chatBgColor, borderwidth=0,
                   activebackground=chatBgColor, command=changeChatMode)
    kbBtn.place(x=25, y=500)"""

    # Mic
    micImg = PhotoImage(file="extrafiles/images/mic.png")
    micImg = micImg.subsample(2, 2)
    micBtn = Button(TextModeFrame, image=micImg, height=30, width=30, bg='#dfdfdf', borderwidth=0,
                    activebackground="#dfdfdf", command=changeChatMode)
    micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Text Field
    #TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
    #UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
    #UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
    UserField = Entry(navRoot, fg='white', bg=chatBgColor, font=('Montserrat', 16), bd=6, width=18, relief=FLAT)
    UserField.place(x=10, y=10)
    UserField.insert(0, "Ask me anything...")
    UserField.bind('<Return>', keyboardInput)

    userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a" + str(ownerPhoto) + ".png")
    botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
    botIcon = botIcon.subsample(2, 2)

    settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg='black', fg=textColor)
    settingsLbl.pack(pady=10)
    separator = ttk.Separator(root2, orient='horizontal')
    separator.pack(fill=X)

    userProfileImg = Image.open("extrafiles/images/avatars/a" + str(ownerPhoto) + ".png")
    userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
    userPhoto = Button(root2, image=userProfileImg, bg=botChatTextBg, bd=0, relief=FLAT, activebackground=botChatTextBg,
                       command=SelectAvatar)
    userPhoto.pack(pady=(20, 5))

    chngPh = ImageTk.PhotoImage(Image.open("extrafiles/images/avatars/changephoto2.png").resize((120, 120)))

    userPhoto.bind('<Enter>', onhover)
    userPhoto.bind('<Leave>', onleave)

    userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg='black')
    userName.pack()

    settingsFrame = Frame(root2, width=300, height=300, bg='black')
    settingsFrame.pack(pady=20)

    labels = Label(settingsFrame, text='Fonts', bg='black')
    labels.place(x=0, y=220)
    #Button(settingsFrame, text="Pick a font", command=font).place(x=150, y=220)

    assLbl = Label(settingsFrame, text='Assistant Voice', font=('Arial', 13), fg=textColor, bg='black')
    assLbl.place(x=0, y=20)
    n = StringVar()
    assVoiceOption = ttk.Combobox(settingsFrame, values=('Male', 'Female'), font=('Arial', 13), width=13,
                                  textvariable=n)
    assVoiceOption.current(voice_id)
    assVoiceOption.place(x=150, y=20)
    assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

    voiceRateLbl = Label(settingsFrame, text='Voice Rate', font=('Arial', 13), fg=textColor, bg='black')
    voiceRateLbl.place(x=0, y=60)
    n2 = StringVar()
    voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
    voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
    voiceOption.current(ass_voiceRate // 50 - 2)  # 100 150 200 250 300
    voiceOption.place(x=150, y=60)
    voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)

    volumeLbl = Label(settingsFrame, text='Volume', font=('Arial', 13), fg=textColor, bg='black')
    volumeLbl.place(x=0, y=105)
    volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16,
                      highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
    volumeBar.set(int(ass_volume * 100))
    volumeBar.place(x=150, y=85)

    themeLbl = Label(settingsFrame, text='Theme', font=('Arial', 13), fg=textColor, bg='black')
    themeLbl.place(x=0, y=143)
    themeValue = IntVar()
    s = ttk.Style()
    s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor,
                focuscolor=s.configure(".")["background"])
    darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue, style='Wild.TRadiobutton',
                              command=changeTheme, takefocus=False)
    darkBtn.place(x=150, y=145)
    lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue, style='Wild.TRadiobutton',
                               command=changeTheme, takefocus=False)
    lightBtn.place(x=230, y=145)
    themeValue.set(1)
    if KCS_IMG == 0: themeValue.set(2)

    chooseChatLbl = Label(settingsFrame, text='Chat Background', font=('Arial', 13), fg=textColor, bg='black')
    chooseChatLbl.place(x=0, y=180)
    cimg = PhotoImage(file="extrafiles/images/colorchooser.png")
    cimg = cimg.subsample(3, 3)
    colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg='black')
    colorbar.place(x=150, y=180)
    if KCS_IMG == 0: colorbar['bg'] = '#E8EBEF'
    Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

    backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT,
                     command=lambda: raise_frame(root1))
    clearFaceBtn = Button(settingsFrame, text='   Clear Facial Data   ', bd=0, font=('Arial 12'), fg='white',
                          bg='#14A769', relief=FLAT, command=deleteUserData)
    backBtn.place(x=5, y=250)
    clearFaceBtn.place(x=120, y=250)

    try:
        # pass
        Thread(target=voiceMedium).start()
    except:
        pass
    try:
        # pass
        Thread(target=dataUpdate).start()
    except Exception as e:
        print('System is Offline...')

    root.iconbitmap('extrafiles/images/logo.ico')
    raise_frame(root1)
    root.mainloop()