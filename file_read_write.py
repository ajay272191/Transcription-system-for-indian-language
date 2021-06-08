import os
import re
transcript_file = './audio'+ '.txt'
global transcriptions
transcriptions = []
def write_transcription():
    # global transcriptions
    f = open(transcript_file, "w")
    for t in transcriptions:
        t = '<s>'+ t
        t = t + '<s>'

        print(t)
        f.write(t)

if os.path.exists(transcript_file):
    # global transcriptions
    #open and read the file after the appending:
    print("file already exists")
    f = open(transcript_file, "r")
    sentences = f.read()
    sentences = re.split('<s>|</s>', sentences)
    print("sentences: ", len(sentences), sentences)
    transcriptions = []
    for s in sentences:
        if(s != ''):
            transcriptions.append(s)
        else:
            print("you fucked up")
            pass
    print(transcriptions)
    write_transcription()
  # os.remove("demofile.txt")
else:
  print("The file does not exist")
  f = open(transcript_file, "w")
  f.write("<s>1 Now the file has more content!</s>")
  f.write("<s>2 Now the file has more content!<s>")
  f.write("<s>3 Now the file has more content!<s>")
  f.write("<s>3 Now the file has more content!<s>")


print("\n\n\nand final transcriptions are \n\n\n", transcriptions)
f.close()
