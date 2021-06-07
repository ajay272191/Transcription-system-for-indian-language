#for voice Recognition
import os
import time
import socket
import pyttsx3
import threading
import webbrowser

# importing libraries for speech recognition
from pocketsphinx import LiveSpeech, DefaultConfig, Decoder, get_model_path, get_data_path
import speech_recognition as sr

#for ui
from tkinter import *
# from tkinter.ttk import *
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename

# from tkinter.filedialog import asksaveasfilename
#----------choose image----------------

# importing library for user intaraction


#importing libraries for audio processing
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play



# import tkinter as tk
# from PIL import Image, ImageTk
# from tkinter.filedialog import askopenfile


# object creation
engine = pyttsx3.init()
# """ RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
engine.setProperty('rate', 100)     # setting up new voice rate
# """VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
# """VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[22].id)   #changing index, changes voices. 1 for female



# configuring decoder to decode text from audio

#getting model path
model_path_ = get_model_path()

# setting up custom configuration
config = DefaultConfig()
config.set_string('-hmm', os.path.join(model_path_, 'en-us'))
config.set_string('-lm', os.path.join(model_path_, 'en-us.lm.bin'))
config.set_string('-dict', os.path.join(model_path_, 'cmudict-en-us.dict'))
decoder = Decoder(config)


# Decoding streaming data
buf = bytearray(4096)


root = Tk()
root.title("Sarthi AMA's Virtual Assistant")
root.geometry('900x500')

# set variable for open filename
global open_status_name
open_status_name = False

# initial audio curser position after breaking up sound, on occurance of silance
global slice_position
slice_position = 0

# create new file function
def new_file():
    #delete previus text
    transcipted_text.delete("1.0", END)
    #upadte status bar
    root.title('New file text pad')
    status_bar.config(text="New File...")
    global open_status_name
    open_status_name = False

def open_file():
    #delete previus text
    transcipted_text.delete("1.0", END)

    #grab filename
    text_file = filedialog.askopenfilename(initialdir='', title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.y"), ("All Files", "*.*")))
    #check if th3re is a file name
    if text_file:
        #make filename global so we can access it later
        global open_status_name
        open_status_name = text_file


    #update satus bar
    name = text_file
    status_bar.config(text=f'{name}        ')
    # name = name.replace("","")
    root.title(f'{name}')

    #open fileids
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    #add file to text file
    transcipted_text.insert(END, stuff)
    #close the text file
    text_file.close()

def save_as_file():

    global text_file
    text_file = asksaveasfilename()
    open_status_name = text_file
    # text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir='', title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", ".html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        #save the file
        f = open(text_file, 'a')
        f.write(transcipted_text.get(1.0, END))
        status_bar.config(text=f'{text_file} :saved       ')
        #close the file
        f.close()

#save file
def save_file():
    global open_status_name
    # open_status_name = text_file
    if open_status_name:
        #save the file
        f = open(open_status_name, 'w')
        f.write(transcipted_text.get(1.0, END))
        #status update and popup code
        status_bar.config(text=f'{open_status_name} :saved       ')
        #close the file
        f.close()
    else:
        save_as_file()

#sarthi's functions
class Sarthi(object):
    # def __init__(self):
        # self.sarthi
    def sarthi_tts(self, transcipted_text):
        engine.say(transcipted_text)
        engine.runAndWait()
        engine.stop()

    def test_connection(self):
       try:
           socket.create_connection(('google.com',80))
           return True
       except OSError:
           return False


    def sarthi_stt(self):
        r = sr.Recognizer()
        # browse_text.set("processing...")

        if self.test_connection()==True:
            print("get set speak")
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                self.sarthi_tts("please speak")                                           # use the default microphone as the audio source
                audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

            try:
                #sarthi_tts("processing your command..")
                self.x=r.recognize_google(audio)
                print("by google command: ", self.x)
                return self.x    # recognize speech using Google Speech Recognition
            except Exception:                           # speech is unintelligible
                print("Could not understand audio")
                return 0
        else:
            print("no  internet connection ")
            print("Offline so result maybe inaccurate")
            print("now speek")
            self.sarthi_tts("please speak")
            self.model_path = get_model_path()
            # print(self.model_path)
            speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(self.model_path, 'en-us'),
            lm=os.path.join(self.model_path, 'en-us.lm.bin'),
            dic=os.path.join(self.model_path, 'cmudict-en-us.dict')
	        #hmm=os.path.join(self.model_path, 'hindi'),
            #lm=os.path.join(self.model_path, 'hindi.lm.bin'),
            #dic=os.path.join(self.model_path, 'hindi_s.dic')
            )
            self.x=''
            count = 0
            for phrase in speech:
                self.x=self.x+str(phrase)
                count = count + 1
                if(count == 2):
                    break
            print("you speak by phonix: ", self.x)
            # print(x)
            return (self.x)

    def sarthi_openatom(self):
        # self.command = "atom"
        self.sarthi_tts("opening atom")
        os.system(f"atom")
    def sarthi_chrome(self):
        # self.command = "google-chrome"
        self.sarthi_tts("opening google chrome")
        os.system(f"google-chrome")

    def sarthi_youtube(self):
        self.sarthi_tts("opening youtube")
        self.url = 'https://www.youtube.com/'
        webbrowser.open(self.url, new=2)
    def sarthi_facebook(self):
        self.sarthi_tts("opening facebook")
        self.url = 'https://www.facebook.com/'
        webbrowser.open(self.url, new=2)
    def sarthi_gmail(self):
        self.sarthi_tts("opening gmail")
        self.url = 'https://gmail.com/'
        webbrowser.open(self.url, new=2)
    # def sarthi_openatom(self):
    #     self.command = "atom"
    #     self.sarthi_tts("opening atom")
    #     os.system(f"atom")

    def sarthi_pwd(self):
        self.cwd=os.getcwd()
        print(str(self.cwd))
        self.sarthi_tts("PRESENT WORKING DIRECTORY is "+str(self.cwd))


    # def sarthi_websearch(keyword):
    def sarthi_websearch(self):
        # If new is 0, the url is opened in the same browser window if possible.
        # If new is 1, a new browser window is opened if possible.
        # If new is 2, a new browser page (“tab”) is opened if possible
        self.url = 'https://www.google.com'
        webbrowser.open('https://www.google.com', new=2)

    #main_function
    def sarthi(self):
        self.application_key = 0
        self.command_key = 0
        # self.sarthi_tts("please speek")

        self.x= self.sarthi_stt()
        if(self.x==0):
            self.x = ""
            self.sarthi_tts('can not hear you click and please speak again')
            return self.x
        self.x = self.x.lower()
        if(self.x == "open google chrome"):
            self.x = "open google_chrome"
        print(self.x, "you says")
            # self.sarthi()
        self.sarthi_dic={
            'folder':{
                'current':self.sarthi_pwd
            },
            'web':{
                'search':self.sarthi_websearch
            },
            'open':{
                'item':self.sarthi_openatom,
                'google_chrome': self.sarthi_chrome,
                'youtube': self.sarthi_youtube,
                'facebook': self.sarthi_facebook,
                'gmail': self.sarthi_gmail,
                # https://pypi.org/project/update-check/
                # https://www.w3resource.com/python-exercises/python-basic-exercise-2.php

            }
        }
        self.words_list=self.x.split(" ")
        for i in self.words_list:
            if i in self.sarthi_dic.keys():
                self.application_key=i
                self.application_flag=1
                break
            else:
                self.application_flag=0

        if(self.application_flag != 0):
            self.command_flag = 0
            self.command_key = 0
            print("here")
            for i in self.words_list:
                if i in self.sarthi_dic[self.application_key].keys():
                    self.command_flag=1
                    self.command_key=i
                    break
                else:
                    self.command_flag=0
            if(self.command_flag != 0):
                if(self.command_flag ==1 and self.application_flag==1):
                    print("executing command: ____", self.sarthi_dic[self.application_key][self.command_key])
                    self.sarthi_dic[self.application_key][self.command_key]()
            else:
                self.user_info="sorry as of now, we are not providing this service"
                self.sarthi_tts(self.user_info)
                print(self.user_info)
                self.x = self.user_info + ": " + self.x
                # return self.x
        else:
            self.sarthi_tts("cant recognize what you said please click and start again")
            print('cant recognize please click and start again')
            # self.sarthi()
        print("returning comband from sarthi: ", self.x)
        return self.x


def give_intro():
    time.sleep(1)
    # engine.say('Hi I am your Shree please click button to start live transcription')
    # engine.runAndWait()
    engine.stop()

def call_sarthi():
    browse_text.set("listening...")
    command = Sarthi()
    # p1 = MyClass()
    give_command = command.sarthi()
    print("given command: ", give_command)
    # instructions.set(give_command)
    global transcipted_text
    transcipted_text.insert(INSERT, give_command)
    transcipted_text.insert(INSERT, "________________ comand: ")
    # browse_text.set("start")



global flag
flag = 1
global chunk_list
global total_chunk
chunk_list = []
global file_path_name
global chunks
file_path_name = " "
def choose_file():
    global slice_position
    global file_path_name
    global total_chunk
    global chunk_list
    global chunks
    slice_position = 0
    file_path_name = askopenfilename(filetypes =[('Wav file', '.wav'), ('Mp3 file', '.mp3')])
    print("\n\nfilename______: ", file_path_name,"\n\n\n")
    file_path['text'] =  "File: " + file_path_name

    print("\n\n-----------------------------",file_path_name,"\n\n")
    # file_dir =   "26.wav"
    sound = AudioSegment.from_file(file_path_name, "wav")
    # play(sound)
    # root.withdraw()
    chunks = split_on_silence(sound,
        # must be silent for at least half a second
        min_silence_len=100,
        # consider it silent if quieter than -16 dBFS
        silence_thresh=-50
     )
    total_chunk = len(chunks)
    print("\n\ntotal no of chunks ", len(chunks))

    chunk_list = []
    for i, chunk in enumerate(chunks):
        chunk.export("files/chunk{0}.wav".format(i), format="wav")
        # play(chunk)
        print("chunk ", i, ": ", len(chunk), "ms", " typw: ",type(chunk))
        chunk_list.append("files/chunk"+str(i)+".wav")
    print("chunk_list: ", chunk_list)
    print("\n\n")

    engine.say("After choosing the files, it been breaked on each silance, now you can play and see transcription of each slices")
    engine.runAndWait()
    engine.stop()
    # transcribe(filename)
    return 0

def play_and_do_transcribe():
    global slice_position
    global total_chunk
    global flag
    global chunks
    print("---------------------------slice_position: ", slice_position,"----------------------------------------")
    global file_path_name
    global chunk_list
    print("\n\n\n-------------------------chunk_list: ", chunk_list, " total_chunk: " ,total_chunk,"\n\n")
    if(slice_position >= total_chunk):
        slice_position = slice_position -1
        print("\nend of clip ", slice_position)
        print("\ndo you want to  close playing then enter Y pr y else any Button")

        engine.say("End of the file cross")
        engine.runAndWait()
        engine.stop()
        # choice = input()
        # flag = 0
        # if(choice == 'Y' or choice == 'y'):
        #     print("\n exiting................")
        #     break
        # else:
        #     slice_position = slice_position - 1
        flag = 0

    elif(slice_position < 0):
        flag = 0
        engine.say("it is already at beginning position")
        engine.runAndWait()
        engine.stop()
        print("\nsorry can't play because curser it at starting point itself: ", slice_position)
        slice_position = slice_position + 1

    if(flag == 1):
        # data_path = get_data_path()
        prediction = ""

        with open(chunk_list[slice_position], 'rb') as f:
            decoder.start_utt()
            while f.readinto(buf):
                decoder.process_raw(buf, False, False)
            decoder.end_utt()

        for segment in decoder.seg():
            prediction = prediction + " " + segment.word

        print("\n\nfinal prediction is: ", prediction, "\n")
        transcipted_text.insert(INSERT, prediction)
        play(chunks[slice_position])

    return 0


def forward_slice():
    global flag
    flag = 1
    global slice_position
    slice_position = slice_position + 1
    play_and_do_transcribe()
    return 0

def backward_slice():
    global flag
    flag = 1
    global slice_position
    slice_position = slice_position - 1
    play_and_do_transcribe()
    return 0

def current_slice():
    global flag
    flag = 1
    play_and_do_transcribe()
    return 0

#----------------- for live audio ----------------------
logo = ImageTk.PhotoImage(Image.open('logo.png').resize((200, 200)))
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.pack()

#-------------------command wrapper-----------------------------------------
comand_frame = Frame(root)
comand_frame.pack()

#instructions
instructions = Label(comand_frame, text="click on the button to give a command")
# instructions.pack()
instructions.grid(row=0, column=0, padx=10)

#browse button
browse_text = StringVar()
# browse_btn = tk.Button(root, textvariable=browse_text, command = , font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
mic_image = Image.open("mic.png")
mic_image = mic_image.resize((35, 35), Image.ANTIALIAS)
reset_img = ImageTk.PhotoImage(mic_image)
browse_btn = Button(comand_frame,borderwidth=0, textvariable=browse_text, image=reset_img,  command=lambda:call_sarthi(),bg="#d9d9d9", fg="white", height=45, width=50)
# browse_text.set("Start")
# browse_btn.pack()
browse_btn.grid(row=1, column=0, padx=10)


#------------------------For audio file ----------------------------------------------

# def open_transcription():
#     show_control.pack_forget() if show_control.winfo_manager() else show_control.pack(after=sent_control, anchor=W, padx=5, pady=10)

choose_img = Image.open("choose_file_.png")
choose_img = choose_img.resize((100, 40), Image.ANTIALIAS)
choose_img = ImageTk.PhotoImage(choose_img)
# , height=45, width=50
show_control = Button(comand_frame,borderwidth=0, textvariable=browse_text, image=choose_img,  command=lambda:choose_file(), font="Raleway", bg="#d9d9d9", fg="white")
show_control.grid(row=0, column=1, padx=10)

# transcipted_text = Text(my_frame, width = 97, height = 25, font=("Helvetica", 16), selectbackground="Yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, pady=5)
# file_path = Text(comand_frame,width=50,height = 2,  selectbackground="Yellow", selectforeground="black", undo=False, pady=5)
file_path = Label(comand_frame, text="file")
file_path.grid(row=1, column=1, padx=10, )
# file_path.insert(INSERT, "file path: ")
file_path['text'] = 'file path: '

sent_control = Frame(comand_frame)
sent_control.grid(row=2, column=1, padx=30)


backward = ImageTk.PhotoImage(Image.open('skip-back.png').resize((35, 35)))
current = ImageTk.PhotoImage(Image.open('play.png').resize((35, 35)))
forward = ImageTk.PhotoImage(Image.open('skip-forward.png').resize((35, 35)))


# Create Volume Meter
backward_button = Button(sent_control, image=forward, borderwidth=0, textvariable=browse_text,  command=lambda:backward_slice(), font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50)
backward_button.grid(row=0, column=0, padx=0)
backward_button = Label(sent_control, text="previus")
backward_button.grid(row=1, column=0, padx=0)

current_button = Button(sent_control, image=current, borderwidth=0, textvariable=browse_text,  command=lambda:current_slice(), font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50)
current_button.grid(row=0, column=1, padx=0)
current_button = Label(sent_control, text="current")
current_button.grid(row=1, column=1, padx=0)


forward_button = Button(sent_control, image=backward, borderwidth=0, textvariable=browse_text,  command=lambda:forward_slice(), font="Raleway", bg="#d9d9d9", fg="white", height=45, width=50)
forward_button.grid(row=0, column=2, padx=0)
forward_button = Label(sent_control, text="next")
forward_button.grid(row=1, column=2, padx=0)



#create main frame
my_frame = Frame(root)
my_frame.pack(pady = 5)

#create scrollbar for text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

#create Text Box
global transcipted_text
transcipted_text = Text(my_frame, width = 97, height = 25, font=("Helvetica", 16), selectbackground="Yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, pady=5)
transcipted_text.pack()
transcipted_text.insert(INSERT, "Your comand: ")


#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#add file Menu
file_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#add edit menu
edit_menu=Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

#add status bar to bottom of app
status_bar = Label(root, text="Ready        ", anchor=E)#east = E
status_bar.pack(fill=X, side=BOTTOM, ipady=5 )
#configure scrollbar
text_scroll.config(command=transcipted_text.yview)


threading.Thread(target = give_intro).start()




#setting up voice command
print("----------------------\n\n",file_path_name,"\n\n")




root.mainloop()
