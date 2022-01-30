#!/usr/bin/env python3
import signal
import sys
from iterfzf import iterfzf
import argparse
from time import sleep
import mutagen
import os

#def AskUser():
#    Parser = argparse.ArgumentParser(description="A simple tool to modify ID3 tags on files")
#    Parser.add_argument("-f", "--filename", action="store_true", help="use filepath in menu")
#    Parser.add_argument("UsageDir", help="dir to scan for tagged files")
#    return Parser.parse_args()

#print(AskUser())

#def FZFYield(ListOfOptions):
#    for i in ListOfOptions:
#        yield i
#        sleep(0.005)

#def ReadFile(FileName):
#    return mutagen.File(FileName)

Labels = ["title", "album", "filepath"]
Seperator = " - "

# Util function to cut text
def CutText(Text, Amount=20):
    if len(Text) > Amount:
        return "..."
    else:
        return Text 

def CheckResult(Return):

    if Return == None:
        print("FZF exited")
        exit(1)


# The screen displaying tags
def DisplayDir(FileDir):
    DirRead = []

    def ReadDir(FileDir):
        for Root, SubFolder, Files in os.walk(FileDir):
            for Filename in Files:
                # Path to use in tagging
                Path = Root + "/" + Filename
                try:
                    # If file exitsts
                    FileContent = mutagen.File(Path)
                    if (FileContent != None):
                        #print(FileContent)
                        FileContent["filepath"] = os.path.relpath(Path,FileDir)
                        
                        Return = ""

                        for i in Labels:
                            if i in FileContent:
                                Return = Return + Seperator + str(FileContent[i][0])

                        #print(Return)
                        yield Return
                        #yield Path
                        #sleep(0.1)
                        #print(Return)
                    
                except mutagen.MutagenError as e:
                    pass
                except TypeError:
                    pass

    Return = iterfzf(ReadDir(FileDir), prompt=FileDir+ " > ")   
    CheckResult(Return)
    return FileDir + Return.split(Seperator)[-1]
    
    
    #ReadDir(FileDir, Labels)


    #print(DirRead)
    #return Return 

# The screen which display file tags
def DisplayFile(FileName):
    FileContent = mutagen.File(FileName)

    def ReadFile(Content):
        for i in Content.keys():
            yield i + " - " + CutText(str(Content[i]))
            sleep(0.001)

    Return = iterfzf(ReadFile(FileContent), prompt=FileName + " > ")
    CheckResult(Return)
    return [FileContent, Return.split(Seperator)[0]]


# The screen to edit tags
def DisplayEdit(FileContents, Tag):
    FileContents[Tag] = input("Enter new value > ")
    FileContents.save()


#FileName = "/media/nfs-music/musiclibrary/MONORAL/Turbulence/08 Kiri.opus"
##Dict = ReadFile(FileName)
##DisplayFile(Dict, FileName + " > ")
#
#FileMetadata, UserChoice = DisplayFile(FileName)
#print(UserChoice)
#print()



if len(sys.argv) > 1:
    RootDir = sys.argv[1]

    # Main loop
    while True:
        Song = DisplayDir(RootDir)
        Content, Tag = DisplayFile(Song)
        DisplayEdit(Content, Tag)
else:
    print("Usage: MusicDir [filepath]")



