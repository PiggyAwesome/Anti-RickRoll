import os
import cv2
import sys
from FindSimilar import find_similar
from pytube import YouTube
import shutil
from threading import Thread

download = input("Is your video a youtube video [y] or local file? [l]: ")
text = "Enter video path: "

if download.lower() == "y":
    text = "Enter raw YouTube url: "
    download = True

vid = input(text)


if not os.path.exists(vid) and download != True:
    print("Video does not exist!")
    exit()

rolls = os.path.abspath("rolls")
temp = os.path.abspath("temp")

print("Removing old frames...")
shutil.rmtree(temp)
os.mkdir(temp)

if download == True:
    print("Downloading... ")
    yt = YouTube(vid)
    title = yt.title
    yt = yt.streams.get_lowest_resolution()
    yt.download(output_path=temp)
    place = temp + "\\" + title + ".mp4"

else:
    place = vid

brek = False
sus = 0
print("Scanning... ")


vidcap = cv2.VideoCapture(place)
def frame(second):
    global brek
    global sus
    if brek == True:
        exit()
    vidcap.set(cv2.CAP_PROP_POS_MSEC, second*1000)
    hasFrames, image = vidcap.read()
    if hasFrames == True:
        currentFrame = temp + "\image" + str(count) + ".jpg"
        try:
            cv2.imwrite(currentFrame, image)
            found = find_similar(rolls, temp + "\image" + str(count) + ".jpg", 80)
        except FileNotFoundError:
            return 0
        if found[0] == True:
           sus += 1
        if sus >= 5:
            print("Rickroll detected!")
            quit()
    if hasFrames == False:
        print("No Rickroll!")
        exec("brek = True")
        sys.exit()

        

second = 0
count = 1
frameRate = 1
success = frame(second)

while brek == False:
    count += 1
    second = second + frameRate
    second = round(second, 2) 
    Thread(target=frame, args=[second], daemon=True).start()
 
