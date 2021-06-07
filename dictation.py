# importing library for user intaraction
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename

#importing libraries for audio processing
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play
import os

# importing libraries for speech recognition
from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path


# setting up GUI
root = Tk()
root.geometry('200x100')




#getting model path
model_path = get_model_path()

# setting up custom configuration
config = DefaultConfig()
config.set_string('-hmm', os.path.join(model_path, 'en-us'))
config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
decoder = Decoder(config)


# Decoding streaming data
buf = bytearray(4096)


# filename = ""

def transcribe(filename):
    #
    print("\n\n-----------------------------",filename,"\n\n")
    # file_dir =   "26.wav"
    sound = AudioSegment.from_file(filename, "wav")
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


    i = 0
    while True:
        user_input = input(" N for play next clip B  for play previous clip and c for current clip")
        print(user_input)
        flag = 1


        if(user_input == 'N' or user_input == 'n'):
            print("\nnext playing ", i, "clip")
            i = i + 1
        elif(user_input == 'B' or user_input == 'b'):
            print("\nprevious playing ", i, "clip")
            i = i - 1
        elif(user_input == 'C' or user_input == 'c'):
            print("\ncurrent playing ", i, "clip")
        else:
            print(i, " wrong input")
            i = i - 1
            flag = 0

        if(i == total_chunk):
            print("\nend of clip ", i)
            print("\ndo you want to  close playing then enter Y pr y else any Button")
            choice = input()
            flag = 0
            if(choice == 'Y' or choice == 'y'):
                print("\n exiting................")
                break
            else:
                i = i-1
        if(i<0):
            flag = 0
            print("\nsorry can't play because curser it at starting point itself: ", i)
            i= i+1


        if(flag == 1):
            # data_path = get_data_path()
            prediction = ""

            with open(chunk_list[i], 'rb') as f:
                decoder.start_utt()
                while f.readinto(buf):
                    decoder.process_raw(buf, False, False)
                decoder.end_utt()


            # print('Best hypothesis segments:', [segment.word for segment in decoder.seg()])

            for segment in decoder.seg():
                prediction = prediction + " " + segment.word

            print("\n\nfinal prediction is: ", prediction, "\n")
            play(chunks[i])


def open_file():

    filename = askopenfilename(filetypes =[('Mp3 file', '.mp3'), ('Wav file', '.wav')])
    print("\n\nfile: ", filename,"\n\n\n")
    transcribe(filename)


btn = Button(root, text ='Open', command = lambda:open_file())
btn.pack(side = TOP, pady = 10)




mainloop()

# import os
# if os.path.exists("demofile.txt"):
#   os.remove("demofile.txt")
# else:
#   print("The file does not exist")
