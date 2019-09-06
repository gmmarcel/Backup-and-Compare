#!/usr/bin/python3
'''
@author : Marcel Gruber
@email  : info@marcel-gruber.de
@date   : 2019.09.06
@version: 0.1
'''

import os
import sys
import shutil

import config


##Check Folder if exist and create it
def checkFolder(sourcePath,destinationPath,fList):
    for f in fList:
        #print("FIRST: ",f)
        for folderSub in f:
            folderSub   = folderSub.replace(sourcePath,destinationPath)
            folderName  = folderSub.replace(".","")
            folderExist = os.path.isdir(folderSub)
            #print("Folder:"+folderSub+" == ",folderExist)

            if not folderExist:
                try:
                    os.mkdir(folderSub)

                except OSError:
                    print("Creation of the directory %s failed" %folderName)
                else:
                    print("Successfully created the directory %s" % folderName)
            else:
                pass


## Check File if exist and if not newer and copy/replace
def checkFile(sourcePath,destinationPath,allFiles):
    for f in allFiles:
        fileSource  = f
        fileDest    = f.replace(sourcePath,destinationPath)
        fileExist   = os.path.isfile(fileDest)
        fileName    = fileDest.replace(".","")
        #print("File: "+fileName+" == ",fileExist)

        if not fileExist:
            try:
                shutil.copy2(fileSource,fileDest)
            except IOError as e:
                print("Unable to copy file. %s" % e)
            except:
                print("Unexpected error:", sys.exc_info())
                exit(1)
            else:
                print("File successfully copied %s" % fileName)
        else:
            fileSourceT = os.path.getmtime(fileSource)
            fileDestT   = os.path.getmtime(fileDest)
            if fileSourceT > fileDestT:
                os.remove(fileDest)
                shutil.copy2(fileSource,fileDest)
                print("File successfully replaced %s" % fileName)
            elif fileSourceT == fileDestT:
                pass
                #print("File has same modified time!!!")
            else:
                pass
                #print("File in destination Path is newer")


#List all Files and Folders 
def data_to_backup(sourcePath,destinationPath):
    folderList = [f.name for f in os.scandir(sourcePath) if f.is_dir()]
    print("Folder List: ",folderList)
    fList = []
    for i in folderList:
        #fList.append(i)
        fList.append([x[0] for x in os.walk("{}".format(sourcePath))])
    #print("Directories and sub: ",fList)

    allFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(sourcePath):
        allFiles += [os.path.join(dirpath, file) for file in filenames]
    #print("All Files in Source Path: ",allFiles)

    checkFolder(sourcePath,destinationPath,fList)
    checkFile(sourcePath,destinationPath,allFiles)


#Backup old Files before overwrite
def data_zip():
    pass


#Start the script
def start(sourcePath,destinationPath):
    path = os.getcwd()
    print("The current working directory is %s" % path)
    print("The source Path is %s" % sourcePath)
    print("The destination Path is %s" % destinationPath)
    data_to_backup(sourcePath,destinationPath)


##Start script
start(config.sourcePath,config.destinationPath)