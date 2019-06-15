import glob
import os
import shutil
import datetime
from config import currentLocation


def saveFileList(DirName=currentLocation['offlineFilesDir'], SaveTo=''):
    if SaveTo == '':
        SaveTo = currentLocation['bundlesDirs'][0] + \
            '/offlineList_' + currentLocation['name'] + '.txt'
    FileList = list(glob.glob(DirName+'/*.*'))
    FileList = list(aFile.split('/')[-1].split('\\')[-1] for aFile in FileList)
    with open(SaveTo, mode='w') as ListFileObj:
        for aFile in FileList:
            print(aFile, file=ListFileObj)


def getMissingFileList(DirName=currentLocation['offlineFilesDir'], listFile=''):
    if listFile == '':
        listFile = currentLocation['bundlesDirs'][0] + \
            '/offlineList_' + currentLocation['syncFilesTo'] + '.txt'
    FilesInDirList = glob.glob(DirName+'/*.*')
    FilesInDirList = list(FileInDirList.split(
        '/')[-1].split('\\')[-1] for FileInDirList in FilesInDirList)

    with open(listFile, mode='r') as ListFileObj:
        FilesInList = ListFileObj.read()
        FilesInList = str(FilesInList)
        FilesInList = FilesInList.splitlines()

    FilesMissingInDir = list(
        aFile for aFile in FilesInList if aFile not in FilesInDirList)
    FilesMissingInList = list(
        aFile for aFile in FilesInDirList if aFile not in FilesInList)
    return {
        'FilesMissingInDir': FilesMissingInDir,
        'FilesMissingInList': FilesMissingInList,
    }


def ZipFileList(listOfFiles, SaveToDir=currentLocation['bundlesDirs'][0] + '/bundlesOut/'):
    print('started zipping ' + str(len(listOfFiles)) + ' files.')
    if len(listOfFiles) == 0:
        print('exited file zipper.')
        return
    if not os.path.exists(SaveToDir+'/tempZip/'):
        os.mkdir(SaveToDir+'/tempZip/')
    for aFile in listOfFiles:
        shutil.copy(currentLocation['offlineFilesDir'] +
                    '/'+aFile, SaveToDir+'/tempZip/')
    nowText = datetime.datetime.now().strftime("%B %d, %Y %H-%M-%S ")
    shutil.make_archive(SaveToDir+'/compress_'+nowText,
                        'zip', SaveToDir+'/tempZip')
    UpdateFileList(listOfFiles)
    shutil.rmtree(SaveToDir+'/tempZip/')
    print('file zipping finished')


def UnZipAndUpdateFileList(ZipName, destDir):
    pass  # todo


def UpdateFileList(NewFileList, listFile=''):
    if listFile == '':
        listFile = currentLocation['bundlesDirs'][0] + \
            '/offlineList_' + currentLocation['syncFilesTo'] + '.txt'
    try:
        with open(listFile, mode='a') as ListFileObj:
            for aFile in NewFileList:
                print(aFile.split('/')[-1].split('\\')[-1], file=ListFileObj)
    except Exception as e:
        print('failed to update list file: ' + str(e))
