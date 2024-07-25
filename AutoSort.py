import os
import shutil
import time
import datetime
import configparser
thisPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/"
config = configparser.ConfigParser()
config.read(thisPath + 'config.ini')
config.sections()
downloadPath = config['DEFAULT']['DownloadPath']
ignoreItems = ["desktop.ini", ""]
ignoreSuffix = [".download", ".crdownload", ".part", ".partial"]
sortedPath = thisPath + "Sorted/"
unsortedPath = thisPath + "Unsorted/"
logsPath = thisPath + "Logs/"

audioSuffix = [".mp3", ".wav", ".ogg"]
imagesSuffix = [".png", ".jpg", ".jpeg", ".gif", ".img"]
videosSuffix = [".mp4", ".mov", ".mpeg", ".avi"]
documentsSuffix = [".docx", ".txt", ".pdf"]

validFiles = list()

def Log(data):
    dateTimeData = datetime.datetime.today()
    date = dateTimeData.strftime('%Y-%m-%d')
    time = dateTimeData.strftime('%H:%M:%S')
    specPath = logsPath + date + ".txt"
    if(os.path.exists(specPath)):
        f = open(specPath, "a")
        f.write("\n" + time + ": " + data)
        f.close()
    else:
        f = open(specPath, "a")
        f.write(time + ": " +data)
        f.close()


# Get folders inside of downloads
def StageOne():
    dir_list = os.listdir(downloadPath)
    for x in dir_list:
        if(IsValidFile(x)):
            validFiles.append(downloadPath + "/" + x)
    StageTwo(validFiles)

# Check if ignore file. This is to avoid moving important files
def IsValidFile(filePath):
    for x in ignoreItems:
        if(filePath == x):
            return False
        if(str(filePath).startswith("~")):
            return False
    for x in ignoreSuffix:
        if(str(filePath).lower().endswith(x)):
            return False
    return True

def MoveFile(file, destination):
    Log("Trying to move " + os.path.basename(file) + " to " + destination + "...")
    try:
        shutil.move(file, destination + os.path.basename(file))
        Log("Moved " + os.path.basename(file) + " successfully.")
    except OSError:
        Log("ERROR: Failed to move " + os.path.basename(file) + " to " + destination)
        quit()

def CheckSuffix(fileName):
    fileName = str(fileName).lower()
    for x in imagesSuffix:
        if(fileName.endswith(x)):
            return "image"
    for x in audioSuffix:
        if(fileName.endswith(x)):
            return "audio"
    for x in documentsSuffix:
        if(fileName.endswith(x)):
            return "doc"
    for x in videosSuffix:
        if(fileName.endswith(x)):
            return "video"
    if(fileName.endswith(".zip")):
        return "zip"
    return "unsorted"

# With list of valid files to move, move them to correct folder
def StageTwo(validFiles):
    for fileName in validFiles:
        matchVar = CheckSuffix(fileName)
        match matchVar:
            case "image":
                MoveFile(fileName, sortedPath + "Images/")
                continue
            case "audio":
                MoveFile(fileName, sortedPath + "Audio/")
                continue
            case "doc":
                MoveFile(fileName, sortedPath + "Documents/")
                continue
            case "video":
                MoveFile(fileName, sortedPath + "Videos/")
                continue
            case "zip":
                MoveFile(fileName, sortedPath + "Zipped/")
                continue
            case "unsorted":
                MoveFile(fileName, unsortedPath)
                continue

startTime = time.time()

def CheckDownloadsLoop():
    time.sleep(15)
    while(True):
        StageOne()
        timeElapsed = time.time() - startTime
        Log("Time elapsed: " + str(round(timeElapsed)) + "s")
        time.sleep(3600)

CheckDownloadsLoop()
