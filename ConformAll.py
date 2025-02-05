#!/usr/bin/env python
# See the README.md for install
import os
import json
import csv
import datetime
from pprint import pprint
import sys
import time
import platform
#import opentimelineio as otio

from multiprocessing.shared_memory import ShareableList,SharedMemory
from multiprocessing import resource_tracker
#sys.path.append('/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules')
#import DaVinciResolveScript as dvr

ICON = "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"

class MyMpClip():
    
    '''
        This class creates a virtual media clip object to use when the imported timeline refer to a clip that is linked to corrupted
        media or the media does not exist at all. This class uses the "Edit Index" of DaVinci Resolve to create the virtual clip.
        If the High Resolution media exists at conform time, that media will come online.
    '''
    
    def __init__(self,
                 file_name:str,
                 video_codec:str,
                 name:str,
                 recordFrame:int, # timeline clip position frame 
                 sourceIn:int, # clip cut in frame
                 sourceOut:int, # clip cut out frame
                 startTC:str, # clip start tc
                 endTC:str, # clip end tc
                 track:int) -> None:
        
        self._properties = {
            "File Name":file_name,
            "Video Codec":video_codec,
            "Reel Name":file_name,
            "Clip Name":name,
            "Clip Color":"Apricot",
            "Start TC":startTC,
            "End TC":endTC
            
        }
        self._recordFrame = recordFrame
        self._sourceIn = sourceIn
        self._sourceOut = sourceOut
        self._track = track
        self._mpClip = self
        self._timelineClip = None
    
    def setTimelineClip(self,clip):
        self._timelineClip = clip
    
    def GetClipProperty(self,key:str=None):
        '''
            Encapsulation of the API GetClipProperty method.
        '''
        if isinstance(self._mpClip,MyMpClip):
            if key:
                return self._properties.get(key,"")
            else:
                return self._properties
        else:
            return self._mpClip.GetClipProperty(key)
        
    def SetClipProperty(self,key:str,value:any):
        '''
            Encapsulation of the API SetClipProperty method.
        '''
        if isinstance(self._mpClip,MyMpClip):
            self._properties[key] = value
        else:
            self._mpClip.SetClipProperty(key,value)
            
    def SetClipColor(self,colorName):
        '''
            This method encapsulates the API SetClipColor method, but the color is always "Apricot",
            no matters what color is send in the argument. 
        '''
        colorName = "Apricot"
        if isinstance(self._mpClip,MyMpClip):
            self._properties["Clip Color"] = colorName
        else:
            if len(self._mpClip.GetClipColor()) == 0:
                self._mpClip.SetClipColor(colorName)
    
    def LinkProxyMedia(self,proxyMediaFilePath):
        if not isinstance(self._mpClip,MyMpClip):
            self._mpClip.LinkProxyMedia(proxyMediaFilePath)
    
    def GetName(self):
        return self._properties["Clip Name"]
    
    def ReplaceClip(self,filename:str):
        '''
            This is the encapsulation of the API ReplaceClip method, and do the same thing using this
            virtual clip object.
        '''
        version_down_19_1 = int(str(RESOLVE_VERSION[0])+str(RESOLVE_VERSION[1])) < 191
        
        ret = True
        currentFolder = getMediaFolder(currentTimeline.GetName())
        binFolder = getMediaFolder("media",parent = currentFolder)
        mediaPool.SetCurrentFolder(binFolder)
        mpClips = binFolder.GetClipList() # try if clip alread exists
        clipFound = False
        try:
            if mpClips:
                for mpClip in mpClips:
                    if mpClip and mpClip.GetClipProperty("File Path") == filename:
                        mpClips = [mpClip]
                        clipFound = True
                        print_info("Clip",mpClip.GetName(),"already exists in the media folder.")
                        break
            if not clipFound:
                mpClips = mediaPool.ImportMedia([filename])
            if len(mpClips) > 0 and mpClips[0]:
                self._mpClip = mpClips[0]
                if self._timelineClip:
                    print_info("Trying to create timeline clip",self._timelineClip.GetName())
                    self._sourceIn = self._timelineClip.GetLeftOffset()
                    self._sourceOut = self._timelineClip.GetRightOffset()
                    self._recordFrame = self._timelineClip.GetStart()
                    currentTimeline.DeleteClips([self._timelineClip])
                ## Appends list of clipInfos specified as dict of "mediaPoolItem", "startFrame" (int), "endFrame" (int), (optional) "mediaType" (int; 1 - Video only, 2 - Audio only), "trackIndex" (int) and "recordFrame" (int). Returns the list of appended timelineItems.
                    clipDict = {
                        "mediaPoolItem":self._mpClip,
                        "startFrame":self._sourceIn,
                        "endFrame":self._sourceOut-(1 if version_down_19_1 else 0),
                        "mediaType":1,
                        "trackIndex":self._track,
                        "recordFrame":self._recordFrame
                    }
                    #pprint(clipDict)
                    timelineClips = mediaPool.AppendToTimeline([clipDict])
                    if timelineClips:
                        print_info("Timeline item",timelineClips[0].GetName(),"created.")
                    else:
                        print_error("Can't create tileline item!")
                else:
                    print_error("No timeline item!")    

            else:
                print_error("Can't import",filename)
                ret = False
        except Exception as e:
            print_error("An exception accured:",e,"\nstartFrame:",self._sourceIn,"\nendFrame:",self._sourceOut,"\ntrackIndex:",self._track,"\nrecordFrame:",self._recordFrame)
            ret = False
        finally:
            mediaPool.SetCurrentFolder(currentFolder)
        
        return ret
    

def print_error(*args,sep: str = " ", end: str = "\n"):
    print('ERROR:','',end='')
    print(*args,sep=sep,end=end)
   
def print_warning(*args,sep: str = " ", end: str = "\n"):
    print('WARNING:','',end='')
    print(*args,sep=sep,end=end)
    
def print_info(*args,sep: str = " ", end: str = "\n"):
    print('INFO:','',end='')
    print(*args,sep=sep,end=end)

#resolve = dvr.scriptapp("Resolve")
print_info("Python version:",sys.version)
#print("Python Path:",sys.path)
CONFORM_ALL_VERSION="2025.3.0"
RESOLVE_VERSION=resolve.GetVersion()
RESOLVE_VERSION_STRING=resolve.GetVersionString()
RESOLVE_VERSION_SUFIX=RESOLVE_VERSION_STRING.replace('.','_')
STOCK_DRB="stock_" + RESOLVE_VERSION_SUFIX + ".drb"
BLACKLIST_FILES="blacklist_files_" + RESOLVE_VERSION_SUFIX + ".json"
print_info("ConformAll version:",CONFORM_ALL_VERSION)
print_info("DaVinci Resolve Version:",RESOLVE_VERSION_STRING)
userPath = os.path.expanduser("~")
if not os.path.exists(userPath):
    print_error("User path does not exist!!!")
    exit(1)
else:
    print_info("User HOME is:",userPath)

# application settings
settingsFile = "ConformAll.json"
settingsPath = os.path.join(userPath,"Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Settings")
settingsJson = {"projects":[{
            "project": "default",
            "mogPath" : "",
            "fieldSep" : "_",
            "fieldCount" : 5,
            "sonyPath" : "",
            "aafPath" : "",
            "avidPath" : "",
            "motionPath" : "",
            "motionFieldSep" : "_",
            "motionFieldCount" : 5,
            "exportStock" : True,
            "importStock" : True,
            "copyMediaPath" : "",
            "autoImportSourceClipsIntoMediaPool":False
            }],
            "currentProject":"default",
            "windowGeometry": { "1": 50, "2": 50, "3": 600, "4": 410 }
            }

settings = {} # project settings
currentHouseProject = ""
stockBinPath = ""

typeColor = {
    'MOG':'Orange',
    'SONY':'Violet',
    'OTHER':'Olive',
    'AUTO':'Yellow', # Media imported using the timeline import function, e.g. Edge proxy 
    'SAME':'Navy', # The High Res codec is the same of Low Res
    'NO_PROXY':'Apricot' # Used when the proxy from AAF is not imported, e.g. error importing, and we load the high resolution instead 
    
}


cancelCopyFiles = False
drScriptsPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts"
copyFilesPath = os.path.join(drScriptsPath,"copy_files.py")

def loadSettings():
    '''
        Get global settings.
    '''
    global currentHouseProject
    global settingsJson
    path = os.path.join(settingsPath,settingsFile)
    
    #print(path)
    if os.path.exists(path):
        with open(path,'r') as openFile:
            settingsJson = json.load(openFile)
    
    else:    
        with open(path, "w") as outfile:
            json.dump(settingsJson, outfile)
    
def getProjects():
    '''
        Get home projects list.
    '''
    projects = []
    for obj in settingsJson["projects"]:
        projects.append(obj['project'])
        
    return projects

def getSettings(project):
    '''
        Get some home project settings.
        Updates the global variable "settings".
        
        Arguments:
            project: the home project to get the settings
    '''
    global settings
    for obj in settingsJson["projects"]:
        if obj['project'] == project:
            settings = obj
            return True
    
    return False

    
def saveSetting(project = None,rename = False):
    '''
        Save the application settings.
        
        Arguments:
        
            project: the name of the home project to save. if present, the project settings
            are saved. If not present only the application settings are saved.
            rename: if True, the project will be renamed with the name currently in the 
            Profile UI text field (not the one selected in the pulldown).
            
            This means that the user pressed the "Rename" button.
             
    '''
    global settingsJson
    settingsJson['currentProject'] = cbProjects.CurrentText 
    settingsJson['windowGeometry'] = win.Geometry
    if project:
        values = getUIValues()
        if not getSettings(project) and not rename: # it's a new project
            settingsJson['projects'].append({'project':project})
            
        for obj in settingsJson["projects"]:
            if obj['project'] == project:
                
                if rename:
                    obj['project'] = cbProjects.CurrentText
                obj['mogPath'] = values[0]
                obj['fieldSep']=values[1]
                obj['fieldCount']=values[2]
                obj['sonyPath']=values[3]
                obj['aafPath']=values[4]
                obj['avidPath']=values[5]
                obj['motionPath']=values[6]
                obj['motionFieldSep']=values[7]
                obj['motionFieldCount']=values[8]
                obj['exportStock']=values[9]
                obj['importStock']=values[10]
                obj['copyMediaPath']=values[11]
                obj['autoImportSourceClipsIntoMediaPool']=values[12]
                break

    path = os.path.join(settingsPath,settingsFile)
    with open(path, "w") as outfile:
        json.dump(settingsJson, outfile)

def getUIValues():
    """
    Get the UI values.
    
    Return (index:value): (
        0:mogPath (string),
        1:fieldSeparator (string),
        2:fieldCount (int), 
        3:sonyPath (string), 
        4:aafPath (string),
        5:avidPath (string),
        6:motionPath (string),
        7:motionFieldSeparator (string),
        8:motionFieldCount (int),
        9:exportStock (bool),
        10:importStock (bool),
        11:copyMediaPath (string),
        12:autoImportSourceClipsIntoMediaPool (bool),
        ) Tuple
    """

    return (win.Find('txtMogPath').Text, 
            win.Find('txtFieldSep').Text, 
            win.Find('spFieldCount').Value,
            win.Find('txtSonyPath').Text,
            win.Find('txtAAFPath').Text,
            win.Find('txtAvidPath').Text,
            "","","", # retirar para usar os campos a seguir
            #win.Find('txtMotionPath').Text,
            #win.Find('txtMotionFieldSep').Text, 
            #win.Find('spMotionFieldCount').Value
            win.Find('ckExportStock').Checked,
            win.Find('ckImportStock').Checked,
            win.Find('txtCopyMediaPath').Text,
            win.Find('ckAutoImportSourceClipsIntoMediaPool').Checked                       
            )

# deprecated
def getEdgeProxyPath():
    avidPath = getUIValues()[5]
    avidPath = os.path.split(avidPath)
    if len(avidPath[1]) == 0: # path have a tail separator
        avidPath=os.path.split(avidPath[0])
    proxyPath = os.path.join(avidPath[0],'Proxy')
    if os.path.isdir(proxyPath):
        return proxyPath
    
    return None

# deprecated
def getUMEPath():
    avidPath = getUIValues()[5]
    avidPath = os.path.split(avidPath)
    if len(avidPath[1]) == 0: # path have a tail separator
        avidPath=os.path.split(avidPath[0])
    umePath = os.path.join(avidPath[0],'UME')
#    if os.path.isdir(umePath):
    return umePath

def getAvidMXFFolder():
    '''
        Gets the "Avid MediaFiles/MXF" folder from the "Avid Folders" list.
        If more than one exists, the first one is returned.
    '''
    
    for folder in settings.get('avidFolders',[]):
        if folder.endswith("Avid MediaFiles" + os.sep + "MXF"):
            return folder
        
    print_error("Avid folders list does not contains a Avid MediaFiles" + os.sep + "MXF folder.")
    
def importIngestSettings(path:str,importToKey:str,importFromKey:str):
    '''
        Import a list from the "ReelMyFiles" application.
        
        Arguments:

            path: the path to the json file
            importToKey: the dict key to here to import the list (destination key)
            importFromKey: the dict key from here to import the list (source key)
    '''
    if os.path.exists(path):
        with open(path,'r') as openFile:
            ingestSettings = json.load(openFile)
            
    currentList = [x.upper() for x in settingsJson.get(importToKey,[])]
    for ext in ingestSettings.get(importFromKey,[]):
        if ext.upper() in currentList:
            continue
        currentList.append(ext)
        
    settingsJson[importToKey] = currentList
    saveSetting()


def getAvidMedia(folderPaths : list):
    '''
        Scan the avid folders list for media file names.
        After the collect the relevant file names, call the 
        importClips method to import the media to the media pool 
        as media pool clips.
        
        Arguments:

            folderPaths: the list of folder paths. 
    '''
    
    print_info("Getting Media Files (Avid)")
    fileEndings = ["_0.MXF","V.MXF","_CC.MXF","_VFX.MXF",".pmxf"]
    avidFiles = []
    ts = time.time()
    print_info("Avid folders list:",folderPaths)
    for folderPath in folderPaths:
        if not folderPath or not os.path.exists(folderPath):
            print_error("The folder",folderPath,"does not exist. Do you forget to mount any drive?")
            continue
        isUME = os.path.basename(folderPath) == "UME"
        for root, dirs, files in os.walk(folderPath):
            for name in files:
                if not "Quarantine File" in root and not "Creating" in root and not name.startswith("."):
                    endOk = False
                    for end in fileEndings :
                        if name.upper().endswith(end.upper()):
                            endOk=True
                    if not endOk and isUME:
                        ext = os.path.splitext(name)[1]
                        if ext.upper() == ".MXF":
                            endOk = True
                    if endOk:
                        avidFiles.append(os.path.join(root,name))
            now = time.time()
            if ts + 1. < now:
                print(end=".")
                ts = now
            
    #print(amaFiles)
    print()
    print_info(len(avidFiles)," Avid MediaFiles found.")
    return importClips(avidFiles)

def getMediaFiles(foldersPaths:list, clipDict:dict, folderType:list):
    """
    Get ama files reel names as keys and paths as values.
    all OTHER folderType(s) must exist in the Camera Folders list
    
    Arguments:
    
        folderPath: path to the ama files root
        clipDict: timeline clips
        folderType: list like [ama] for MOG or the Camera Folders from the UI
    
    Return {"reelName":"filename",...}
    """
    print_info("Getting Media Files (AMA)")
    print_info("Folders to search:",foldersPaths)
    mimes=["." + x.upper() for x in settingsJson.get('fileExtensions',[])]
    amaFiles = {}
    numFiles=0
    uiValues = getUIValues()
    fieldSep = uiValues[1] if "ama" in folderType else None
    fieldCount = uiValues[2] if "ama" in folderType else None
    existingFolders = []
    for folderPath in foldersPaths:
        if not os.path.exists(folderPath):
            print_error("Folder",folderPath,"does not exist. Do you forget to mount any drive?")
        else:
            existingFolders.append(folderPath)
            
    if len(existingFolders) == 0: return amaFiles
    ts = time.time()
    for folderPath in existingFolders:
        for root, dirs, files in os.walk(folderPath):
            cameraFolderExits = False
            for c in folderType:
                rootArray = root.split(os.path.sep) # garante igualdade na palavra e não em parte
                if c in rootArray:
                    cameraFolderExits = True
                    break
            for name in files:
                replace = True
                filename = os.path.join(root,name)
                _,ext = os.path.splitext(filename)
                if cameraFolderExits and ext.upper() in mimes:
                    fileReel = extractReelName(name, fieldSep,fieldCount)
                    clip = clipDict.get(fileReel)
                    if clip:
                        
                        if amaFiles.get(fileReel):
                            mpClips = mediaPool.ImportMedia([amaFiles.get(fileReel),filename])
                            if isMpClipHighRes(mpClips[0]) and not isMpClipHighRes(mpClips[1]):
                                replace = False
                            mediaPool.DeleteClips(mpClips)
                                
                        if replace:
                            amaFiles[fileReel] = filename
                            numFiles+=1

            now = time.time()
            if ts + 1. < now:
                print("",end=".")
                ts = now


    print()                
    print_info(numFiles,"files found in",folderPath,"...")
        
    return amaFiles

def getMediaFolder(name, parent = None):
    """
    Get media folder with "name" from the media pool root, or from parent, if given.
    """
    mpRoot = mediaPool.GetRootFolder()
    if parent:
        mpRoot = parent
    for folder in mpRoot.GetSubFolderList():
        if folder.GetName() == name:
            return folder
    
    return None    

def getHostName():
    '''
        Returns the local hostname regarding the OS.
    '''
    hostName = None
    if platform.system() == "Windows":
        hostName = platform.uname().node
    else:
        hostName = os.uname()[1]
        
    return hostName

def lockBinFile(binFilePath: str):
    '''
        Create a lock file to prevent mutual access to the drb stock bin file.
        
        Returns: True if the lock is created successfully. False otherwise.
    '''
    print_info("Locking stock bin.")
    folder = os.path.dirname(binFilePath)
    if not os.path.exists(folder):
        print_error(f"Cant create lock file. Folder {folder} does not exist. Do you forget to mount some drive?")
        return False
    fileName = os.path.basename(binFilePath).removesuffix(".drb")
    lockFile = os.path.join(folder,fileName+".lock")
    lockDic = {}
    hostName = None
    if os.path.exists(lockFile):
        with open(lockFile,'r') as openFile:
            lockDic = json.load(openFile)
        hostName = lockDic['hostName']
        if hostName != getHostName():
            errorPopupDialog("The bin file is locked by the workstation named \"" + hostName + "\".\n" \
                "Try again later ...")
            return False
        else:
            # it's the same machine
            print_info("The stock bin it's locked but this machine is the owner of the lock.")
            return True
    
    #if not os.path.exists(binFilePath):
    #    print("Stock bin file noes not exist.")
    #    return True

    lockDic['hostName'] = getHostName()
    with open(lockFile,'x') as outfile:
        json.dump(lockDic, outfile)
    return True  
                
def unlockBinFile(binFilePath: str):
    '''
        Delete the lock file thats prevent mutual access to the drb stock bin file.
        
        Returns: True if the lock is deleted successfully. False otherwise.
    '''
    folder = os.path.dirname(binFilePath)
    fileName = os.path.basename(binFilePath).removesuffix(".drb")
    lockFile = os.path.join(folder,fileName + ".lock")
    hostName = getHostName()
    if os.path.exists(lockFile):
        with open(lockFile,'r') as openFile:
            lockDic = json.load(openFile)
        if hostName == lockDic['hostName']:
            try:
                os.remove(lockFile)
                print_info("Stock bin lock removed.")
            except Exception as e:
                print_error(f"Some error occurred: {e}")
                return False
        else:
            print_error("Can't unlock stock bin file! This machine is not the owner of the lock!")
            return False
    else:
        print_warning("Stock bin lock does not exist!")
    
    return True
                

def importClips(files:list):
    '''
        Import the Avid media files to the media pool as media pool clips.
        This method is called from in the return of the getAvidMedia method.
        
        Arguments:
        
            files: list of filename paths to import
    '''
    
    global stockBinPath
    
    print_info("Importing clips to stock...")
    uiValues = getUIValues()
    localTs = datetime.datetime.now()
    currentFolder = mediaPool.GetCurrentFolder()
    mpRoot = mediaPool.GetRootFolder()
    stock = getMediaFolder("stock")
    
    #if not stock:
    mediaPool.SetCurrentFolder(mpRoot)
    createEmptryStock = True
    if uiValues[10] and isImportExportDrbPossible():
        print_info("Trying to import stock folder...")
        mediaPool.DeleteFolders([stock])
        if os.path.exists(stockBinPath):

            try:
                if mediaPool.ImportFolderFromFile(stockBinPath):
                    stock = getMediaFolder("stock")
                    if stock:
                        print_info("Stock folder imported.")
                        createEmptryStock = False
                    else:
                        print_error("Can not create the stock folder object!")
                else:
                    print_error("Failed to import stock folder!")
            except:
                 print_error("This DaVinci Resolve version can't import the bin folder.")
        else:
            print_warning("Stock folder bin file does not exist!")
    else:
        if stock:
            print_info("Stock bin already exists...")
            createEmptryStock = False
                          
    if createEmptryStock:
        accepted,_,_ = genericPopupDialog("Do you want to import all Avid media files? This may take a while.","Yes","No",haveRejectButton=True)
        if accepted:
            print_info("Creating empty stock folder...")
            stock = mediaPool.AddSubFolder(mpRoot,"stock")
        else:
            print_error("Stock folder creation canceled.")
            return stock
    
    print_info("Getting filenames from stock folder clips...") 
    currentClipsFileNames = []
    ts = time.time()
    for clip in stock.GetClipList():
        if clip:
            currentClipsFileNames.append(clip.GetClipProperty("File Name"))
        now = time.time()
        if ts + 1. < now:
            print("",end=".")
            ts = now
    print()
        
    clipsInMP = len(currentClipsFileNames)
    filesNumber = len(files)
    if filesNumber == 0:
        print_warning("There is no files to import!")
        return stock
    
    #clipsToImport=filesNumber - clipsInMP
    print_info(clipsInMP,"clips already in media pool..")
    print_info("Preparing list of files to import.")
    bmd.wait(0.2)
    #print(files[0] if len(files) > 0  else "None")
        
    files2Process=[]
    blacklist = loadBlacklistFiles(os.path.join(getAvidMXFFolder(),BLACKLIST_FILES))
    print_info(len(blacklist),"files in blacklist.")
    ts = time.time()
    for file in files:
        basename = os.path.basename(file)
        if not basename in currentClipsFileNames:
            if file not in blacklist:
                files2Process.append(file)
        now = time.time()
        if ts + 1. < now:
            print("",end=".")
            ts = now
    print()
    print_info(len(files2Process), "files to import...")
    clips2ImportCounter = len(files2Process)
    
    mediaPool.SetCurrentFolder(stock)
    l_pointer=0
    r_pointer=0
    importedClips=[]
    step=1000
    print_info("Importing media (",step," files each step)...",sep="")
    for l_pointer in range(0,clips2ImportCounter,step):
        r_pointer = l_pointer + step
        if r_pointer > clips2ImportCounter:
           r_pointer = clips2ImportCounter 
        print_info("Importing from index ",l_pointer," to index ",r_pointer-1,".\t",clips2ImportCounter - l_pointer," files remaining...",sep="")
        bmd.wait(0.2)
        importedClips += mediaPool.ImportMedia(files2Process[l_pointer:r_pointer])

    mediaPool.RefreshFolders()
    print_info("Creating blacklist...")
    blacklist = createBlackListFiles(importedClips,files2Process,blacklist)
    print_info(len(blacklist),"files in blacklist.")
    
    if not isImportExportDrbPossible():
        genericPopupDialog("This DaVinci Resolve version ("+ RESOLVE_VERSION_STRING + "), can not export the stock bin folder.\nPlease, do it manualy if you want to.",
            "Ok")


    if (uiValues[9] or isDrbTodayFirstExport()) and isImportExportDrbPossible():
        print_info("Trying to export stock bin...")
        try:
            if stock.Export(stockBinPath):
                print_info("Stock bin exported...")
            else:
                print_error("Failed to export stock bin!")
        except:
            print_error("This DaVinci Resolve version can't export the bin folder.")
        
    mediaPool.SetCurrentFolder(currentFolder)
    if not importedClips:
        return stock
    print_info(len(importedClips),"clips imported of",clips2ImportCounter)   
    dt = datetime.datetime.now() - localTs
    print_info("Processed in",str(dt))
    return stock

def createBlackListFiles(importedClips:list,files2Process:list,blacklist_par:list=None):
    """
    Create a json file with a list of filenames that can not be imported to the media pool.
    
    Arguments:
        importedClips: A list of imported MediaPoolItems.
        files2Process: A list of filenames to import to the media pool.
        blacklist_par: A list of already loaded existing blacklist
        
    Returns:
        The blacklist.
    """
    localFiles2Process = files2Process.copy()
    blacklist = blacklist_par
    blackListFileName = os.path.join(getAvidMXFFolder(),BLACKLIST_FILES)
    if not blacklist:
        blacklist = loadBlacklistFiles(blackListFileName)
    
    # remove processed files from localFiles2Process
    # remaining files are the import errors
    for clip in importedClips:
        clipFilename = clip.GetClipProperty("File Path")
        if clipFilename in localFiles2Process:
            localFiles2Process.remove(clipFilename)
            
    for file in localFiles2Process:
        if file not in blacklist:
            blacklist.append(file)
            
    blacklistJson = {
        'files': blacklist
    }    
    with open(blackListFileName,'w') as f:
        json.dump(blacklistJson,f)
        
    return blacklist
        
def loadBlacklistFiles(blackListFileName:str):
    '''
        Load the blacklisted files from the blacklist file.
        
        Returns:

            A list with the blacklisted files.
    '''
    blacklist = []
    if os.path.exists(blackListFileName):
        with open(blackListFileName,'r') as f:
            blacklistJson = json.load(f)
            blacklist= blacklistJson.get('files',[])
            
    return blacklist


def getTimelineClips():
    '''
        Returns the timeline clips (items) in all timeline video tracks.
        
        Returns:
        
            A list with the clips. 
    '''
    
    global currentTimeline    
    clips = []
    currentTimeline = currentProject.GetCurrentTimeline()
    videoTracks = currentTimeline.GetTrackCount('video')
    print_info('Video tracks in timeline:',videoTracks)
    for i in range(1,videoTracks+1):
        print_info("Getting clips from track",i)
        for clip in currentTimeline.GetItemListInTrack('video', i):
            clips.append((clip,i))
            
    return clips

def getTimelineClipFromEditIndex():
    '''
        Returns the clips represented in the DR "Edit Index" as 
        MyMpClip (virtual media pool clip).
        Please see the MyMpClip class for details.
        
        Returns:
        
            A dict where the key is a tuple with the video track index and the clip Record In TC.
            
    '''
    
    global currentTimeline    
    currentTimeline = currentProject.GetCurrentTimeline()
    csv_path = os.path.join(os.path.expanduser("~"),"timeline.csv")
    if os.path.exists(csv_path):
        os.remove(csv_path) # remove to avoid false readings
    currentTimeline.Export(csv_path, resolve.EXPORT_TEXT_CSV, resolve.EXPORT_MISSING_CLIPS)
    if not os.path.exists(csv_path):
        print_error("Edit Index failed to export!")
        return {}
    with open(csv_path,encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
                
        data = {}
        for rows in csv_reader:
            track = rows['V']
            if track.startswith("V"):
                rec_in = tc2Frames(rows['Record In'])
                rec_out = tc2Frames(rows['Record Out'])
                source_in = tc2Frames(rows['Source In'])
                source_out = tc2Frames(rows['Source Out'])
                key = (int(track[1:]),rec_in)

                if not data.get(key,False):
                    data[key] = MyMpClip(rows["Reel"],
                                         rows["Codec"],
                                         rows["Name"],
                                         key[1],
                                         source_in, 
                                         source_out,
                                         rows['Source Start'],
                                         rows['Source End'],
                                         key[0])
        print_info(f"Edit index have {len(data)} records.")
        return data

def getMpClipsFromTimeline(resolution:str = 'all'): 
    """
        Return all media pool clips linked to the timeline don't matter the media type.
        
        Arguments:
            resolution: one of 'all','high' or 'proxy'
    """
    resolution = 'codecs' if resolution == 'high' else resolution
    resolution = 'codecsProxy' if resolution == 'proxy' else resolution
    
    timelineClips = getTimelineClips()
    clips = []
    currentList = [x.upper() for x in settingsJson.get(resolution,[])]
    for clip in timelineClips:
        mpClip = clip[0].GetMediaPoolItem()
        if mpClip:
            codec = mpClip.GetClipProperty("Video Codec")
            if len(currentList) > 0 and codec.upper() in currentList:
                clips.append(mpClip)
            
    return clips

def getTimelineClipsMog(clipsList, timeline_names_reels):
    """
    Returns the Mog media pool clips linked to the timeline.
    
    Arguments:
        clipsList: timeline clips list
        timeline_names_reels: dict with the MyMpClip objects extracted from the "Edit Index"
        
    Returns a dict as {"clipReel":(<media pool clip>,'MOG',<timelineClip>),....}
    """
    print_info("Getting MOG Clips...")
    clipDict = {}
    numClips=0
    numClipsEditIndex=0
    uiValues = getUIValues()
    fieldSep = uiValues[1]
    fieldCount = uiValues[2]
    #pprint(timeline_names_reels)
    for clip_tuple in clipsList:
        clip = clip_tuple[0]
        track = clip_tuple[1]
        mpClip = clip.GetMediaPoolItem()
        if mpClip:
            if len(mpClip.GetClipProperty("Clip Color")) == 0:
                # Try to extract the reel name from the clipname
                clipName = mpClip.GetName()
                clipReel = extractReelName(clipName,fieldSep,fieldCount)
                #clipReel = mpClip.GetClipProperty("Reel Name")
                if clipReel:
                    clipDict[clipReel] = (mpClip,'MOG',clip)
                    numClips+=1
                else:
                    # Try to get the reel name insted 
                    clipReel = extractReelName(mpClip.GetClipProperty("Reel Name"),fieldSep,fieldCount)
                    if clipReel:
                        clipDict[clipReel] = (mpClip,'MOG',clip)
                        numClips+=1
        else:
            tcIn = clip.GetStart()
            print_warning("Trying to get the reel name from the edit index with timeline clip name",clip.GetName())
            mpClip = timeline_names_reels.get((track,tcIn),False)
            if mpClip:
                mpClip.setTimelineClip(clip)
                clipReel = extractReelName(mpClip.GetClipProperty("Reel Name"),fieldSep,fieldCount)
                if clipReel:
                    print_info("Adding reel name from edit index:",clipReel)
                    clipDict[clipReel] = (mpClip,'MOG',clip)
                    numClips+=1
                    numClipsEditIndex+=1
            else:
                print_error("No edit index found for that timeline clip!")
    
    print_info(numClips,"not corformed clips found in timeline.",numClipsEditIndex,"clips detected with edit index...")        
    return clipDict if numClips > 0 else None

def getTimelineClipsOthers(clipsList,clipType,timeline_names_reels):
    """
    Returns the Sony/OTHER media pool clips linked to the timeline.
    
    Arguments:

        clipsList: timeline clips list
        clipType: clipType
        timeline_names_reels: dict with the MyMpClip objects extracted from the "Edit Index"

        
    Returns a dict as {clipReel: (<media pool clip>,clipType,timelineClip),...}
    """
    mimes=["." + x.upper() for x in settingsJson.get('fileExtensions',[])]
    print_info("Getting " + clipType + " Clips...")
    clipDict = {}
    numClips=0
    numClipsEditIndex=0
    for clip_tuple in clipsList:
        clip = clip_tuple[0]
        track = clip_tuple[1]
        mpClip = clip.GetMediaPoolItem()
        if mpClip:
            if len(mpClip.GetClipProperty("Clip Color")) == 0:

                clipReel = mpClip.GetClipProperty("Reel Name")
                if not clipReel:
                    clipReel = extractReelName(mpClip.GetClipProperty("File Name"))

                if clipReel:
                    # remove extension from the reel name, if exists
                    reelNoExt,reelExt = os.path.splitext(clipReel)
                    if reelExt.upper() in mimes:
                        clipReel = reelNoExt
                    clipDict[clipReel] = (mpClip,clipType,clip)
                    numClips+=1
        else:
            tcIn = clip.GetStart()
            print_warning("Trying to get the reel name from the edit index with timeline clip name",clip.GetName())
            mpClip = timeline_names_reels.get((track,tcIn),False)
            if mpClip:
                mpClip.setTimelineClip(clip)
                clipReel = mpClip.GetClipProperty("Reel Name")
                if not clipReel:
                    clipReel = extractReelName(mpClip.GetClipProperty("File Name"))
                if clipReel:
                    print_info("Adding reel name from edit index:",clipReel)
                    clipDict[clipReel] = (mpClip,clipType,clip)
                    numClips+=1
                    numClipsEditIndex+=1
            else:
                print_error("No edit index found for that timeline clip!")
        
    #if numClips > 0:
    #    pprint(clipDict)
    #print_info(numClips,"not corformed clips found in timeline...")    
    print_info(numClips,"not corformed clips found in timeline.",numClipsEditIndex,"clips detected with edit index...")       
    return clipDict if numClips > 0 else None

def getMpClipFromReelName(reelName:str,stockClipList:list):
    '''
        Get the media pool clip corresponding to a given reel name.
        
        Arguments:

            reelName: a str with the reel name.
            stockClipList: the list of clips from the stock bin.
            
        Returns:

            A API MediaPoolItem object.
    '''
    for mpClip in stockClipList:
        if mpClip.GetClipProperty("Reel Name") == reelName:
            return mpClip
        
 
def removeExtension(path):
    '''
        Remove a extension from a filename.
        
        Arguments:
        
            path: the filename path.
    '''
    valueParts = path.split(".")
    if len(valueParts) > 1:
        valueParts = valueParts[0:len(valueParts)-1]
        
    return ".".join(valueParts)

def extractReelName(value: str, fieldSep = None, fieldCount = None):
    '''
        Extracts a reel name from a filename.
        
        Arguments:

            value: a filename without path.
            fieldSep: the Mog field separator.
            fieldCount: the Mog number of field to have in count.
            
        Returns:

            A str with the reel name.
    '''
    
    # remove extension
    clipName = removeExtension(value)
    if fieldSep == None and fieldCount == None: # is sony
        return clipName
    fields = clipName.split(fieldSep)[0:fieldCount]
    if len(fields) != fieldCount:
        return None
    #print(fields)
    return fieldSep.join(fields)
    
def changeClipsColorOnAutoImportSourceClipsIntoMediaPool():
    '''
        Change the color of the clips when the "Auto Import Source Clips Into Media Pool" option is used.
    '''
    timelineClips = getTimelineClips()
    for clip in timelineClips:
        mpClip = clip[0].GetMediaPoolItem()
        if mpClip:
            mpClip.SetClipColor(typeColor['AUTO'])
        
def getTimelineCodecs():
    '''
        Returns all codecs used in the current timeline.
        
        Returns: 
        
            A list of str with the codecs designations.
    '''
    timelineClips = getTimelineClips()
    codecs=[]
    for clip in timelineClips:

        mpClip = clip[0].GetMediaPoolItem()
        if mpClip:
            codec = mpClip.GetClipProperty("Video Codec")
            if codec not in codecs:
                codecs.append(codec)
            
    return codecs

def replaceClips(timelineClips:dict,files:dict):
    '''
        Replace the imported timeline (AAF) linked media pool clips with the corresponding
        high resolution ones.  
        
        Arguments:
            timelineClips: a dict with the media pool clips linked to the timeline.
            files: a dict with the high resolution files to consider.
            
        Returns:

            The number of clips replaced.
    '''
    
    print_info("Conforming clips...")
    currentFolder = getMediaFolder(currentTimeline.GetName())
    binFolder = getMediaFolder("media",parent = currentFolder)
    if not binFolder:
        binFolder = mediaPool.AddSubFolder(currentFolder,"media")
        
    counter = 0
    clips2Move=[]
    clipType = None
    for key in timelineClips.keys():
        c = timelineClips.get(key)
        mpClip = c[0]
        clipType = c[1]
        timelineClip=c[2]
        timelineClipName = timelineClip.GetName()
        proxyClipFileName=mpClip.GetClipProperty("File Name") 
        proxyClipPath=mpClip.GetClipProperty("File Path")
        proxyCodec=mpClip.GetClipProperty("Video Codec")

        clipName = mpClip.GetName()
        file = files.get(key)
        #print(file)
        if file:
            oldStartTc = mpClip.GetClipProperty("Start TC")
            oldStartTCSplit = oldStartTc.split(":")
            if oldStartTCSplit[0] == "24":
                mpClip.SetClipProperty("Start TC","00:" + oldStartTCSplit[1] + ":" + oldStartTCSplit[2] + ":" + oldStartTCSplit[3])
                oldEndTC = mpClip.GetClipProperty("End TC")
                oldEndTCSplit = oldEndTC.split(":")
                oldEndHour = int(oldEndTCSplit[0])
                newEndHour = oldEndHour - 24
                mpClip.SetClipProperty("End TC",str(newEndHour) + ":" + oldEndTCSplit[1]  + ":" + oldEndTCSplit[2] + ":" + oldEndTCSplit[3])
                print_info("TC for",mpClip.GetName(),"is now",mpClip.GetClipProperty("Start TC"),"->",mpClip.GetClipProperty("End TC"))
    
            if mpClip.ReplaceClip(file):
                bmd.wait(0.1)
                if proxyCodec == mpClip.GetClipProperty("Video Codec") and not isinstance(mpClip,MyMpClip):
                    print_warning("New and old files have de same codec.")
                    mpClip.ReplaceClip(proxyClipPath)
                    bmd.wait(0.1)
                    mpClip.SetClipProperty("Scene",timelineClipName)
                    mpClip.SetClipColor(typeColor["SAME"])
                    continue    
                
                counter+=1
                mpClip.LinkProxyMedia(proxyClipPath)
                mpClip.SetClipColor(typeColor[clipType])
                mpClip.SetClipProperty("Scene",timelineClipName) 
                #mpClip.SetClipProperty("Reel",key) 

                clips2Move.append(mpClip)
                
                print_info("Clip",clipName,"replaced")
            else:
                print_error("Error replacing",clipName,"with",file)
    
    
    mediaPool.MoveClips(clips2Move,binFolder)
    mediaPool.SetCurrentFolder(currentFolder)
    print_info(str(counter)," clips conformed.")
        
    return counter

# not used
def getMpClipMyName(name:str,mediaFolder):
    for clip in mediaFolder.GetClipList():
        if name == clip.GetName():
            return clip
        
    return None
    

def insertReferences():
    '''
        Insert the optional video and audio references files into the timeline.
    '''
    global currentTimeline
    
    currentTimeline = currentProject.GetCurrentTimeline()
    filename = removeExtension(getUIValues()[4])
    audioFile = filename + ".wav"
    if not os.path.exists(audioFile):
        audioFile = filename + ".WAV"
        if not os.path.exists(audioFile):
            audioFile = None
    
    videoFile = filename + ".mxf"
    if not os.path.exists(videoFile):
        videoFile = filename + ".MXF"
        if not os.path.exists(videoFile):
            videoFile = None
    
    if audioFile:
        print_info("Inserting reference audio...")
        audioClip = mediaPool.ImportMedia([audioFile])[0]
        appendedClips = mediaPool.AppendToTimeline(audioClip)
        if len(appendedClips) == 0:
            print_error("Failed to add reference audio!")
        else:
            print_info("Reference audio added...")    
    else:
        print_warning("Reference audio file does not exist")
        
    if videoFile:
        print_info("Inserting reference video...")
        if currentTimeline.AddTrack('video'):
            trackCount = currentTimeline.GetTrackCount('video')
            videoClip = mediaPool.ImportMedia([videoFile])[0]
            if videoClip:
                clipDic = {
                    "mediaPoolItem":videoClip,
                    "startFrame":0,
                    "endFrame":videoClip.GetClipProperty("End"),
                    "mediaType":1,
                    "trackIndex":trackCount,
                    "recordFrame":currentTimeline.GetStartFrame()
                }
                appendedClips = mediaPool.AppendToTimeline([clipDic])
            if len(appendedClips) == 0:
                print_error("Failed to add reference video!")
            else:
                print_info("Reference video added...")
        else:
            print_error("Failed to create video track!")
    else:
        print_warning("Reference video file does not exist")
        
    currentTimeline.SetCurrentTimecode(currentTimeline.GetStartTimecode())
    
def buttonsEnabled(state,exceptions:list=[]):
    '''
        Activate or deactivate the UI objects before (deactivate) of after (activate) a operation.
        This prevents that the user to interact with the UI while a operation is being processed.
        
        Arguments:
        
            state: a boolean with the state to apply.
            exceptions: list of UI objects to not activate or deactivate.
    '''
    exceptions.append('mainWindow')
    exceptions.append('MyStack')
    if state:
        win.On.mainWindow.Close = OnClose
    else:
        win.On.mainWindow.Close = None
    for obj in win.GetItems().values():
        #if obj.ID in exceptions:
        #    print(obj.ID)
        if obj.ID not in exceptions:
            obj.Enabled = state

def fileExists(filePath, extraText = ""):
    '''
        Popups a message if a file does not exists.
        
        Arguments:
            
            filePath: filename path.
            extraText: some text do add to the default message.
            
        Returns:
        
            True if the file exists or False otherwise.
    '''
    if not os.path.exists(filePath):
        errorPopupDialog("The file " + filePath + " does not exists." + extraText)
        return False
    
    return True

def tc2Frames(tc:str):
    
    """
        Returns a timecode string in frames (int)
    
        Arguments:
        
            tc: a str with the time code. The "." and ";" separators will be converted to ":". 
            
        Returns:

            A int with the number of frames.
    
    """
    tc = tc.replace(".",":")
    tc = tc.replace(";",":")
    tc_list = tc.split(":")
    
    hours = int(tc_list[0])
    minutes = int(tc_list[1])
    seconds = int(tc_list[2])
    frames = int(tc_list[3])
    
    fps = int(currentProject.GetSetting("timelineFrameRate"))
    
    tc_frames = hours * 60 * 60 * fps + minutes * 60 * fps + seconds * fps + frames
    
    return tc_frames

def isAvidMediaFilesFolder(path:str):
    splitPath = os.path.normpath(path).split(os.sep)
    try:
        idx = splitPath.index("Avid MediaFiles")
    except ValueError:
        return False
    
    if len(splitPath) == idx + 1: # does not have a folder after
        return False
    
    return True

def isMpClipHighRes(clip):
    '''
        Test if a media clip codec is in the high resolution list.
        
        Arguments:

            clip: a MediaPoolItem API object
            
        Returns:
        
            True if the clip is high resolution or False if is proxy.
    '''
    
    codec = clip.GetClipProperty("Video Codec")
    return codec in settingsJson.get('codecs',[])
    
    
def isOnStockFolder():
    '''
        Test and alert the user that must get out of the stock bin folder.
        
        Returns:
        
            True if the user in inside the stock folder or False otherwise.
    '''
    if mediaPool.GetCurrentFolder().GetName() == "stock":
        errorPopupDialog("You can not do this operation inside the stock folder/bin.\nPlease choose another folder/bin")
        return True
    
    return False

def isNotTimelineSelected():
    '''
        Test and alert the user that must have a timeline selected.
        
        Returns:
        
            True if there is no timeline selects or False otherwise.
    '''
    if not currentProject.GetCurrentTimeline():
        errorPopupDialog("Please, select a timeline or import a AAF.")
        return True
    
    return False

def isEditPage():
    '''
        Test and alert the user that must be in the DR Edit page.
        
        Returns:
        
            True if the user have the edit page selected or False otherwise.
    '''
    page = resolve.GetCurrentPage()
    if page != "edit":
        errorPopupDialog("Please go to the Edit page")
        return False
    
    return True

def isCopyMediaOk():
    '''
        Test if the paths for coping the high resolution media to a new location are correct.
        
        Returns:

            A tuple with the new path and the media pool folder bin where to scan for the actual media locations.
            If the test is false a False,False tuple is returned.
    '''
    if isNotTimelineSelected():
        return False,False
    
    mediaPath = getUIValues()[11]
    if not os.path.exists(mediaPath):
        errorPopupDialog("The new media path \"" + mediaPath + "\" does not exist. Please choose a valid path.")
        return False,False
    
    currentFolder = getMediaFolder(currentTimeline.GetName())
    binFolder = getMediaFolder("media",parent = currentFolder)
    if not binFolder:
        errorPopupDialog('The "media" folder (bin) does not exists. Please conform media before copy media.')
        return False,False
    
    return mediaPath,binFolder

# TODO: some better way to test if the reel name option is selected.
def isReelNameSelected(clipDict):
    '''
        Test if the reel name option in the DR settings is selected.
        This test is done by getting the property of a media pool clip(s). If all
        clips the dict as no reel name, this will return False, even if the option is 
        selected. This need to be addressed.
        
        Arguments:
            
            A dict of media pool clips to test.
        
        Returns:

            True if the option is selected or False otherwise.
    '''
    if len(clipDict.keys()) == 0: # does not matter if does no have clips
        return True
    
    for v in clipDict.values():
        if v[0].GetClipProperty("Reel Name"):
            return True    
    
    ret,_,_ = genericPopupDialog("No Reel Names Found.\n" \
    "The reel names need to be activated in the Project Settings.\n" \
    "Please goto File->Project Settings...->General Options\n" \
    "In the Conform Options section select:\n" \
    "- Assist using reel names from the:\n" \
    "-- Embedding in source clip file","Continue","Cancel the conform process",haveRejectButton=True)
    
    return ret

def isImportExportDrbPossible():
    '''
        Test if the DR version allow importing of dbr files.
        
        Returns:

            True if is allowed or False otherwise.
    '''
    version = str(RESOLVE_VERSION[0])+str(RESOLVE_VERSION[1])
    #print(version)
    return (int(version) >= 185)

def isDrbTodayFirstExport():
    '''
        Test if the dbr file was already exported at the current day.
        If not, is asked to the user if he/she wants to export the dbr.
        This is used if the "Export Stock Bin" is not selected when importing a AAF.
        
        Returns:
        
            False if the dbr was already exported or the user rejects to export, or return True if the user accept to export.
    '''

    fileDate = None if not os.path.exists(stockBinPath) else datetime.datetime.fromtimestamp(os.path.getmtime(stockBinPath)).date()
    today = datetime.datetime.now().date()    
    if fileDate != today:
        accept,_,_ = genericPopupDialog("The stock folder has not yet been exported today. Last export date is " + str(fileDate) + ".\nDo you want to export the stock folder?","Yes","No",haveRejectButton=True)
        return accept
        
    return False
    
def areFoldersOk():
    '''
        Teste if all folders locations exit and are configured.
        
        Returns:
        
            True if everything is or False otherwise. 
    '''
    
    """
    Get the UI values.
    
    Return (index:value): (
        0:mogPath (string),
        1:fieldSeparator (string),
        2:fieldCount (int), 
        3:sonyPath (string), 
        4:aafPath (string),
        5:avidPath (string),
        6:motionPath (string),
        7:motionFieldSeparator (string),
        8:motionFieldCount (int),
        9:exportStock (bool),
        10:importStock (bool),
        11:copyMediaPath (string)
        12:autoImportSourceClipsIntoMediaPool (bool)
        ) Tuple
    """
    
    ui_values = getUIValues()
    msg = ""
    ret = True
    if not os.path.exists(ui_values[0]):
        ret = False
        msg += f"The Mog Path {ui_values[0]} does not exist.\n"
    if not os.path.exists(ui_values[0]):
        ret = False
        msg += f"The Sony Path {ui_values[3]} does not exist.\n"
    if not os.path.exists(ui_values[0]):
        ret = False
        msg += f"The Avid Path {ui_values[5]} does not exist.\n"
    if not os.path.exists(ui_values[0]):
        ret = False
        msg += f"The Edit Storage Path {ui_values[11]} does not exist.\n"
    if not ret:
        msg += "\nDo you forget to mount any drive?"
        accept,_,_ = genericPopupDialog(msg,"Continue","Exit",haveRejectButton=True)
        ret = accept
    
    return ret

#TODO: the rest of the docstrings

def timelineExists(timelineName:str):
    '''
        Test if a timeline with a given name exists.
        
        Arguments:
        
            timelineName: the name of the timeline.
            
        Returns:
        
            True if the timeline exists or else otherwise.
    '''
    for i in range(1,currentProject.GetTimelineCount()+1):
        if currentProject.GetTimelineByIndex(i).GetName() == timelineName:
            return True
    
    return False

# not used
def working(command:str="start"):
    """
        Start and stop the working script that prints progress points in the console.
        
        Arguments:
        
            command: String. command to send. May be 'start' (default), 'stop'.
    """
    if command == "start":
        sl = None;
        scriptPath=os.path.join(drScriptsPath,"working.py")
        resource_tracker.ensure_running()
        try:
            SharedMemory(name='ConformAllWorking').unlink()
            print_warning("Shared Memory removed")
        except: 
            print_warning("Shared Memory does not exist")                       
        finally:
            sl = ShareableList([False],name='ConformAllWorking')
        bmd.wait(0.1)
        fu.RunScript(scriptPath)
    elif command == "stop":
        sl = ShareableList(name='ConformAllWorking')
        sl[0] = True
        bmd.wait(0.1)
        sl.shm.close()
        

##### EVENT HANDLERS #####
def OnClose(ev):
    saveSetting(currentHouseProject)
    print_info("Exit")
    fu.ShowConsole(False)
    dispatcher.ExitLoop()

def BtConformMog(ev):
    if not isEditPage():
        return False
    if isNotTimelineSelected() or isOnStockFolder():
        return False
    print_info("Processing MOG...")
    buttonsEnabled(False)
    uiValues = getUIValues()
    #mogPath = uiValues[0]
    maxRetries = 30
    retry = 0
    result = True
    mogDic = None
    timeline_names_reels = getTimelineClipFromEditIndex()
    while retry < maxRetries and result:
        retry+=1
        print_info(f"Retry {retry} of {maxRetries}")
        timelineClipDict = getTimelineClipsMog(getTimelineClips(),timeline_names_reels)

        if timelineClipDict and isReelNameSelected(timelineClipDict):
            if not mogDic:
                mogDic = getMediaFiles(settings.get('mogFolders',[]),timelineClipDict,["ama"])
            result = replaceClips(timelineClipDict,mogDic) > 0
        else:
            result = False
        
    buttonsEnabled(True)
    print_info("Finished MOG conforming...")
    return True
    
def BtConformCameras(ev):
    who = ev['who']
    clipType = "SONY"
    folderType = ["CLIP","Clip"]
    if who == 'btConformOthers':
        clipType = "OTHER"
        folderType = settingsJson.get('cameras',[])

    if not isEditPage():
        return False
    if isNotTimelineSelected() or isOnStockFolder():
        return False
    print_info("Processing " + clipType + "...")
    buttonsEnabled(False)
    maxRetries = 30
    retry = 0
    result = True
    sonyDic = None
    #sonyPath = getUIValues()[3]
    timeline_names_reels = getTimelineClipFromEditIndex()
    while retry < maxRetries and result:
        retry+=1
        print_info(f"Retry {retry} of {maxRetries}")
        timelineClips = getTimelineClips()
        clipDict = getTimelineClipsOthers(timelineClips,clipType,timeline_names_reels)
        if clipDict and isReelNameSelected(clipDict):
            if not sonyDic:
                sonyDic = getMediaFiles(settings.get('sonyFolders',[]), clipDict,folderType)
            result = replaceClips(clipDict,sonyDic) > 0
        else:
            result = False
        
    buttonsEnabled(True)
    print_info("Finished",clipType,"conforming...")
    return True
    
def BtConformAll(ev):
    if not isEditPage():
        return
    print_info("Conforming all media types...")
    if BtConformCameras({'who':'btConformSony'}):
        if BtConformCameras({'who':'btConformOthers'}):
            BtConformMog(None)

# not used
def otioTransform(path):
    filePath,_ = os.path.splitext(path)
    otioPath = filePath + ".otio"
    currentTimeline = currentProject.GetCurrentTimeline()
    currentTimeline.Export(otioPath,resolve.EXPORT_OTIO)
    
    timeline = otio.adapters.read_from_file(otioPath)
    print_info("Reading timeline")
    if timeline:
        for clip in timeline.each_clip():
            print_info('============================================================')
            print_info(clip.name)
            for fx in clip.effects:
                if fx.metadata:
                    if fx.metadata['Resolve_OTIO']['Effect Name'] == 'Retime and Scaling':
                        fx.metadata['Resolve_OTIO']['Enabled'] = False
                        print_info(fx.metadata)
                        
    aafFile,_ = os.path.splitext(path)    
    aafFile += "_otio.otio"      
    otio.adapters.write_to_file(timeline,aafFile)               
    #Export(fileName, resolve.EXPORT_OTIO, exportSubtype)
    #thisClip = currentTimeline.GetCurrentVideoItem()
    #if thisClip.ResetNode(1):
    #    print("Clip reseted")
    #    
    #if thisClip.GetFusionCompCount() > 0:
    #    comp = thisClip.GetFusionCompByIndex(1)
    #    tools = comp.GetToolList()
    #    for tool in tools.values():
    #        pprint(tool.GetData())
    
    return aafFile

# not used
def otioExport(path:str):
    pass

def BtImportAAF(ev):
    global currentTimeline,stockBinPath
    values = getUIValues()
    if not isImportExportDrbPossible():
        accept,_,_ = genericPopupDialog("This DaVinci Resolve version (" + RESOLVE_VERSION_STRING + "), can not import the stock bin folder. \
            \nDo you want to cancel the operation and import the stock bin folder manualy?",
            "Yes, cancel the operation","No, continue with the operation",haveRejectButton=True)
        if accept:
            return
    stockBinPath = os.path.join(getAvidMXFFolder(),STOCK_DRB)
    if not isEditPage():
        return
    if isOnStockFolder():
        return
    if not lockBinFile(stockBinPath):
        return
    buttonsEnabled(False)
    
    path = values[4]
    if not os.path.exists(path):
        print_error("AAF file does not exists!")
        buttonsEnabled(True)
        unlockBinFile(stockBinPath)
        return
    timelineName = ".".join(os.path.basename(path).split(".")[0:-1])
    if timelineExists(timelineName):
        print_error("The timeline",timelineName,"already exists!")
        buttonsEnabled(True)
        unlockBinFile(stockBinPath)
        return
    autoImportSourceClipsIntoMediaPool=values[12]
    stock = None
    if not autoImportSourceClipsIntoMediaPool:
        stock = getAvidMedia(settings['avidFolders'])
        if not stock:
            return
        clips = stock.GetClipList()
        if len(clips) == 0:
            print_warning("There is no clips in stock folder!")
            if not autoImportSourceClipsIntoMediaPool:
                autoImportSourceClipsIntoMediaPool,_,_ = genericPopupDialog("There is no clips in stock folder!\nDo you want link to source camera files?","Yes","No",haveRejectButton=True)
            if not autoImportSourceClipsIntoMediaPool:
                buttonsEnabled(True)
                unlockBinFile(stockBinPath)
                return
        if not autoImportSourceClipsIntoMediaPool:
            print_info("Stock folder have",len(clips),"clips.")

    binFolder = getMediaFolder(timelineName)
    if not binFolder:
        mpRoot = mediaPool.GetRootFolder()
        binFolder = mediaPool.AddSubFolder(mpRoot,timelineName)
    
    if not mediaPool.SetCurrentFolder(binFolder):
        print_error("Can't select the bin folder")
        buttonsEnabled(True)
        unlockBinFile(stockBinPath)
        return
    
    
    print_info("Creating timeline",timelineName)
    bmd.wait(2)
    timeline = mediaPool.CreateEmptyTimeline(timelineName)
    bmd.wait(2)
    #pprint(timeline.GetSetting())
    sourceClipsFolders = [stock] if stock else []
    importDict={
    "linkToSourceCameraFiles":False,
    "autoImportSourceClipsIntoMediaPool":autoImportSourceClipsIntoMediaPool,
    "insertAdditionalTracks":False,
    "useSizingInfo":True
    }
    if not autoImportSourceClipsIntoMediaPool:
        importDict["sourceClipsFolders"] = [stock]  
    print_info("Importing AAF into timeline...")
    if not timeline.ImportIntoTimeline(path,importDict):
        print_error("Failed to import the timeline",timelineName)
        print_error("Please confirm the timeline creation frame rate in the project settings.")
    
    #timeline = mediaPool.ImportTimelineFromFile(path, {
    #    "timelineName":timelineName,
    #    "importSourceClips":False,
    #    "sourceClipsFolders":[stock]
    #    })
    #if not timeline:
    #    print("Failed to import the timeline",timelineName)
    else:
        if currentProject.SetCurrentTimeline(timeline):
            print_info("Timeline created. Inserting references...")
            insertReferences()
            if autoImportSourceClipsIntoMediaPool:
                changeClipsColorOnAutoImportSourceClipsIntoMediaPool()
                currentFolder = getMediaFolder(currentTimeline.GetName())
                binFolder = getMediaFolder("media",parent = currentFolder)
                if not binFolder:
                    binFolder = mediaPool.AddSubFolder(currentFolder,"media")
                    clips2Move = getMpClipsFromTimeline(resolution='high')
                    
                    mediaPool.MoveClips(clips2Move,binFolder)
                    mediaPool.SetCurrentFolder(currentFolder)
        
            print_info("Trying to change TCs of offline clips, if any...")
            timeline_names_reels = getTimelineClipFromEditIndex()
            #clips_count=0
            stockClipList = None

            for clip_tuple in getTimelineClips():
                #clips_count+=1
                #print("Clips count",clips_count)
                clip = clip_tuple[0]
                track = clip_tuple[1]
                mpClip = clip.GetMediaPoolItem()
                if not mpClip:
                    tcIn = clip.GetStart()
                    mpClip = timeline_names_reels.get((track,tcIn),False)
                    if mpClip:
                        startFrame = mpClip.GetClipProperty("Start TC")
                        if startFrame == "24:00:00:00":
                            #print(startFrame)
                            mpClip.setTimelineClip(clip)
                            clipReel = mpClip.GetClipProperty("Reel Name")
                            #print("mClip")
                            if not clipReel:
                                #print("extractReelName")
                                clipReel = extractReelName(mpClip.GetClipProperty("File Name"))
                            if clipReel:
                                #print("getMpClipFromReelName")
                                print_info("Edit Index clip",clipReel,"have",startFrame,"Start TC. Getting the media pool clip...")
                                if not stockClipList:
                                    stock = getMediaFolder("stock")
                                    stockClipList = stock.GetClipList()
                                mpClip = getMpClipFromReelName(clipReel,stockClipList)
                                if mpClip:
                                    #print("checking TC")
                                    mpClip.SetClipProperty("Start TC","24:00:00:00")
                                    oldEndTC = mpClip.GetClipProperty("End TC")
                                    oldEndTCSplit = oldEndTC.split(":")
                                    oldEndHour = int(oldEndTCSplit[0])
                                    newEndHour = oldEndHour + 24
                                    mpClip.SetClipProperty("End TC",str(newEndHour) + ":" + oldEndTCSplit[1]  + ":" + oldEndTCSplit[2] + ":" + oldEndTCSplit[3])
                                    print_info("TC for",mpClip.GetName(),"is now",mpClip.GetClipProperty("Start TC"),"->",mpClip.GetClipProperty("End TC"))
    
                 
        else:
            print_error("Failed to set ",timelineName," as the current timeline",timelineName)
    
    print_info("AAF import finished...")
    buttonsEnabled(True)
    unlockBinFile(stockBinPath)
    
def ProjectChanged(ev):
    '''
        Handle the Home Project pulldown event
    '''
    global currentHouseProject
    global win
    saveSetting(currentHouseProject)
    who = ev['who']
    if who == 'cbProjectsOperation':
        currentHouseProject = cbProjectsOperation.CurrentText
        cbProjects.CurrentText = currentHouseProject
    
    currentHouseProject = cbProjects.CurrentText
    if who == 'cbProjects':
        cbProjectsOperation.CurrentText = currentHouseProject
    loadSettings()
    getSettings(currentHouseProject)
    if who == 'cbProjects':
        print_info("Current project is",currentHouseProject)

    refreshMainWindow()

def DeleteProject(ev):
    global currentHouseProject
    global settingsJson
    
    if cbProjects.CurrentIndex == 0:
        print_error("Default project can not be deleted!")
        return
    print_info("Deleting project",currentHouseProject)
    oldSettings = settings
    idx = cbProjects.CurrentIndex
    currentHouseProject = None
    cbProjects.CurrentIndex = idx-1
    cbProjects.RemoveItem(idx)
    cbProjectsOperation.CurrentIndex = idx-1
    cbProjectsOperation.RemoveItem(idx)
    
    settingsJson['projects'].remove(oldSettings)

    
def AddProject(ev):
    global currentHouseProject
    newName = win.Find("txtNewProject").Text
    projects = getProjects()
    if newName in projects:
        print_error("Project",newName,"already exist!")
        return
    cbProjects.AddItem(newName)
    cbProjectsOperation.AddItem(newName)
    currentHouseProject = newName
    cbProjects.CurrentText = newName
    
def RenameProject(ev):
    newName = win.Find("txtNewProject").Text
    projects = getProjects()
    if newName in projects:
        print_error("Project",newName,"already exist!")
        return
    oldName = cbProjects.CurrentText
    cbProjects.ItemText[cbProjects.CurrentIndex] = newName
    cbProjectsOperation.ItemText[cbProjectsOperation.CurrentIndex] = newName
    saveSetting(oldName,rename=True)
    
def OnCopyMedia(ev):
    global currentProject, currentTimeline, mediaPool
    extraText = "\nThis file is needed to perform this operation."
    if not fileExists(copyFilesPath,extraText):
        return
    
    mediaPath, mediaFolder = isCopyMediaOk()

    if mediaPath and mediaFolder:
        mediaFolderName = mediaFolder.GetName()
        bt = win.Find(ev['who'])
        buttonsEnabled(False,[bt.ID])
#        bmd.wait(2)
#       buttonsEnabled(True)
#        return

        sl = None;
        resource_tracker.ensure_running()
        try:
            SharedMemory(name='ConformAllCopyMedia').unlink()
            print_warning("Shared Memory removed")
        except: 
            print_warning("Shared Memory does not exist")                       
        finally:
            sl = ShareableList([False,False,mediaPath,mediaFolderName,0],name='ConformAllCopyMedia')
        bmd.wait(0.1)

        fu.RunScript(copyFilesPath) # run child process
        bt.Text = "Cancel"
        bt.Events = {'Clicked':False}
        bmd.wait(0.5) # wait to child processs updates shm
        ts = datetime.datetime.now()
        while True:
            finished=sl[1]
            if finished:
                break
            if bt.Down:
                sl[0]=True
                bt.Text = "Canceling..."
                bt.Enabled = False
                print_info(' Canceling...\n')
                bmd.wait(0.5) # Wait to write in shm 

            bmd.wait(0.0001)
        #print(sl.shm.name)
        relinkedClips = sl[4]
        sl.shm.close()
        #sl.shm.unlink()
        if relinkedClips > 0:
            pm.SaveProject()
            currentProjectName = currentProject.GetName()
            pm.CloseProject(currentProject)
            currentProject = pm.LoadProject(currentProjectName)
            print_info("Current DaVinci Resolve project:",currentProject.GetName())
            currentTimeline = currentProject.GetCurrentTimeline()
            mediaPool = currentProject.GetMediaPool()
        dt = datetime.datetime.now() - ts
        print_info("Processed in",str(dt))
        print_info('Finished copying files.')
        bt.Text = "Copy Media"
        bt.Events = {'Clicked':True}
        buttonsEnabled(True)
    
def OnDeleteMedia(ev):
    parentFolder = getMediaFolder(currentTimeline.GetName())
    mediaFolder = getMediaFolder("media",parentFolder)
    if not mediaFolder:
        errorPopupDialog('The "media" folder (bin) does not exists. You must conform and copy files before delete files.')
        return
    
    accepted,_,_ = genericPopupDialog("Do you want to delete the media files in the edit storage folder?","Yes","No",haveRejectButton=True)
    if not accepted:
        return
    mpClips = mediaFolder.GetClipList()
    copyMediaPath = getUIValues()[11]
    clips2Move=[]
    deleteUnrelinked = False
    deleteUnrelinkedAsked = False
    for clip in mpClips:
        filePath = clip.GetClipProperty('File Path')
        if filePath.startswith(copyMediaPath):
            if os.path.exists(filePath):
                proxy = clip.GetClipProperty("Proxy Media Path")
                if clip.ReplaceClip(proxy):
                    clip.UnlinkProxyMedia()
                    clip.SetClipColor("Blue")
                    print_info('Deleting file',filePath)
                    os.remove(filePath)
                    clips2Move.append(clip)
                else:
                    if not deleteUnrelinkedAsked:
                        deleteUnrelinked,_,_ = genericPopupDialog("Some chips do not have an associated proxy and will be offline. Do you want to remove these files anyway?",
                                                                  "Yes","No",haveRejectButton=True)
                        deleteUnrelinkedAsked = True
                    if deleteUnrelinked:
                        print_info('Deleting file',filePath)
                        os.remove(filePath)
                    else:
                        print_warning("Can not delete the file ", filePath,".",sep='')
                        
            else:
                print_error(filePath,"does not exists!")
        else:
            print_error(filePath,'can not be deleted')
            
    stock = getMediaFolder("stock")
    if stock:
        mediaPool.MoveClips(clips2Move,stock)
            
            
def OnBrowse(ev):
    '''
        Handles ALL browse for files or directories buttons.
    '''
    buttonsEnabled(False)
    who = ev['who']
    if who == "btBrowseMog":
        txt = win.Find('txtMogPath')
        txt.Text = fu.RequestDir(txt.Text)
    elif who == "btBrowseSony":
        txt = win.Find('txtSonyPath')
        txt.Text = fu.RequestDir(txt.Text)
    elif who == "btBrowseAvid":
        txt = win.Find('txtAvidPath')
        newPath = fu.RequestDir(txt.Text)
        if newPath:
            #if newPath.endswith(os.sep + 'Avid MediaFiles' + os.sep + 'MXF' + os.sep) \
            #    or newPath.endswith(os.sep + 'Avid MediaFiles' + os.sep + 'UME' + os.sep):
            if isAvidMediaFilesFolder(newPath):
                txt.Text = newPath
            else:
                print_error('Wrong path')
                errorPopupDialog(newPath + " is a wrong Path.\nThe path must be in the format <Volume>" + os.sep + 'Avid MediaFiles' + os.sep + '<Some Folder>')
            
    elif who == "btBrowseAAF":
        txt = win.Find('txtAAFPath')
        txt.Text = fu.RequestFile(os.path.dirname(txt.Text),'',{"FReqB_SeqGather" : True, "FReqS_Filter" : "Open AAF Files (*.aaf)|*.aaf", "FReqS_Title" : "Choose AAF file"}) #filedialog.askopenfilename(defaultextension='aaf', initialdir=os.path.dirname(txt.Text))
    elif who == "btBrowseCopyMedia":
        txt = win.Find('txtCopyMediaPath')
        txt.Text = fu.RequestDir(txt.Text)
    elif who == "btImportExtensions":
        ingestSettingsFile = fu.RequestFile(userPath,'',{"FReqB_SeqGather" : True, "FReqS_Filter" : "Open JSON Files (*.json)|*.json", "FReqS_Title" : "Choose ReelMyFiles Ingest Settings file"})
        if ingestSettingsFile:
            importIngestSettings(ingestSettingsFile,'fileExtensions','fileExtensions')
            treeExtensionsConfig(win)
    elif who == "btImportCameraFolder":
        ingestSettingsFile = fu.RequestFile(userPath,'',{"FReqB_SeqGather" : True, "FReqS_Filter" : "Open JSON Files (*.json)|*.json", "FReqS_Title" : "Choose ReelMyFiles Ingest Settings file"})
        if ingestSettingsFile:
            importIngestSettings(ingestSettingsFile,'cameras','cameras')
            treeCameraFoldersConfig(win)
        
    buttonsEnabled(True)

def OnTabChanged(ev):
    items = win.GetItems()
    items['MyStack'].CurrentIndex  = ev['Index']

def OnMediaFoldersList(ev):
    '''
        Generic event handler for media tree folders events.
        To this work, all buttons must have the same prefixes, e.g. btAdd..., btRemove...,etc.        
    '''

    # dict to map buttons to media types
    ev_media_type = {
        'btAddMogFolder':'mog',
        'btRemoveMogFolder':'mog',
        'btAddAvidFolder':'avid',
        'btRemoveAvidFolder':'avid',
        'btAddSonyFolder':'sony',
        'btRemoveSonyFolder':'sony',
    }
    
    # dict to map media types to parameters
    param = {
        'mog':{
            'ui_value':0,
            'title':"Mog Folders",
            'treeObject':'treeMogFolders',
            'settingsKey':'mogFolders'
        },
        'avid':{
            'ui_value':5,
            'title':"Avid Folders",
            'treeObject':'treeAvidFolders',
            'settingsKey':'avidFolders'
        },
        'sony':{
            'ui_value':3,
            'title':"Sony Folders",
            'treeObject':'treeSonyFolders',
            'settingsKey':'sonyFolders'
        }
    }
    
    items = win.GetItems()
    who = ev['who']
    mediaType = ev_media_type.get(who)
    paramType = param[mediaType]
    title = paramType['title']
    settingsKey = paramType['settingsKey']
    treeObject = paramType['treeObject']
    if who.startswith('btAdd'):
        
        folder = getUIValues()[paramType['ui_value']]
        folder = os.path.normpath(folder)
        if not os.path.exists(folder):
            print_error("Folder",folder,"does not exist!")
            return
        currentList = settings.get(settingsKey,[])
        if len(currentList) == 0:
            settings[settingsKey] = []
        if folder not in currentList:
            settings[settingsKey].append(folder)
            treeMediaFoldersConfig(win,title,treeObject,settingsKey)
            saveSetting()
    elif who.startswith('btRemove'):
        tree = items[treeObject]
        haveSelecteds = False
        for it in tree.SelectedItems().values():
            haveSelecteds=True
            folder = it.Text[0]
            settings[settingsKey].remove(folder)
        
        if haveSelecteds:
            treeMediaFoldersConfig(win,title,treeObject,settingsKey)
            saveSetting()
        else:
            print_warning("Please select the folder(s) to remove!")

def OnExtensionsList(ev):
    items = win.GetItems()
    who = ev['who']
    if who == 'btAddExtension':
        _,_,items = genericPopupDialog("Enter a extension name",haveInput=True,haveRejectButton=True)
        ext = items['LineEdit'].Text
        currentList = [x.upper() for x in settingsJson.get('fileExtensions',[])]
        if len(currentList) == 0:
            settingsJson['fileExtensions'] = []
        if ext and not ext.upper() in currentList:
            settingsJson['fileExtensions'].append(ext)
            treeExtensionsConfig(win)
            saveSetting()
    elif who == 'btRemoveExtension':
        tree = items['treeExtensions']
        haveSelecteds = False
        for it in tree.SelectedItems().values():
            haveSelecteds=True
            ext = it.Text[0]
            settingsJson['fileExtensions'].remove(ext)
        
        if haveSelecteds:
            treeExtensionsConfig(win)
            saveSetting()

def OnCamerasList(ev):
    items = win.GetItems()
    who = ev['who']
    if who == 'btAddCameraFolder':
        _,_,items = genericPopupDialog("Enter a camera folder",haveInput=True,haveRejectButton=True)
        ext = items['LineEdit'].Text
        currentList = [x.upper() for x in settingsJson.get('cameras',[])]
        if len(currentList) == 0:
            settingsJson['cameras'] = []
        if ext and not ext.upper() in currentList:
            settingsJson['cameras'].append(ext)
            treeCameraFoldersConfig(win)
            saveSetting()
    elif who == 'btRemoveCameraFolder':
        tree = items['treeCameraFolders']
        haveSelecteds = False
        for it in tree.SelectedItems().values():
            haveSelecteds=True
            ext = it.Text[0]
            settingsJson['cameras'].remove(ext)
        
        if haveSelecteds:
            treeCameraFoldersConfig(win)
            saveSetting()

def OnCodecsList(ev):
    items = win.GetItems()
    who = ev['who']
    if who == 'btAddCodec':
        _,_,items = genericPopupDialog("Enter a codec",haveInput=True,haveRejectButton=True)
        codec = items['LineEdit'].Text
        addCodecsToList([codec],'codecs',treeCodecsConfig,['codecsProxy'])

    elif who in ['btRemoveCodec','btSendToProxy']:
        #print(who)
        tree = items['treeCodecs']
        haveSelecteds = False
        for it in tree.SelectedItems().values():
            haveSelecteds=True
            codec = it.Text[0]
            settingsJson['codecs'].remove(codec)
            if who == 'btSendToProxy':
                addCodecsToList([codec],'codecsProxy',treeProxyCodecsConfig)     
        
        if haveSelecteds:
            treeCodecsConfig(win)
            saveSetting()
    elif who == 'btImportFromTimeline':
        timelineCodecs = getTimelineCodecs()
        addCodecsToList(timelineCodecs,'codecs',treeCodecsConfig,['codecsProxy'])
                        
def OnProxyCodecsList(ev):
    items = win.GetItems()
    who = ev['who']
    if who == 'btAddProxyCodec':
        _,_,items = genericPopupDialog("Enter a codec",haveInput=True,haveRejectButton=True)
        codec = items['LineEdit'].Text
        addCodecsToList([codec],'codecsProxy',treeProxyCodecsConfig,['codecs'])
            
    elif who in ['btRemoveProxyCodec','btSendToHigh']:
        tree = items['treeProxyCodecs']
        haveSelecteds = False
        for it in tree.SelectedItems().values():
            haveSelecteds=True
            codec = it.Text[0]
            settingsJson['codecsProxy'].remove(codec)
            if who == 'btSendToHigh':
                pass
        
        if haveSelecteds:
            treeProxyCodecsConfig(win)
            saveSetting()

# just for tests. The button it's hidden.         
def OnTeste(ev):
    timeline_names_reels = getTimelineClipFromEditIndex()
    for clip_tuple in getTimelineClips():
        clip = clip_tuple[0]
        track = clip_tuple[1]
        mpClip = clip.GetMediaPoolItem()
        if not mpClip:
            tcIn = clip.GetStart()
            mpClip = timeline_names_reels.get((track,tcIn),False)
            if mpClip:
                mpClip.setTimelineClip(clip)
                clipReel = mpClip.GetClipProperty("Reel Name")
                if not clipReel:
                    clipReel = extractReelName(mpClip.GetClipProperty("File Name"))
                if clipReel:
                    mpClip = getMpClipFromReelName(clipReel)
                    if mpClip:
                        oldStartTC = mpClip.GetClipProperty("Start TC")
                        if oldStartTC == "00:00:00:00":
                            mpClip.SetClipProperty("Start TC","24:00:00:00")
                            oldEndTC = mpClip.GetClipProperty("End TC")
                            oldEndTCSplit = oldEndTC.split(":")
                            oldEndHour = int(oldEndTCSplit[0])
                            newEndHour = oldEndHour + 24
                            mpClip.SetClipProperty("End TC",str(newEndHour) + ":" + oldEndTCSplit[1]  + ":" + oldEndTCSplit[2] + ":" + oldEndTCSplit[3])
                            print("TC for",mpClip.GetName(),"is now",mpClip.GetClipProperty("Start TC"),"->",mpClip.GetClipProperty("End TC"))
                                          
    
    #currentFolder = mediaPool.GetCurrentFolder()
    #stock = getMediaFolder("stock")
    #for mpClip in stock.GetClipList():
    #    oldStartTC = mpClip.GetClipProperty("Start TC")
    #    if oldStartTC == "00:00:00:00":
    #        mpClip.SetClipProperty("Start TC","24:00:00:00")
    #        oldEndTC = mpClip.GetClipProperty("End TC")
    #        oldEndTCSplit = oldEndTC.split(":")
    #        oldEndHour = int(oldEndTCSplit[0])
    #        newEndHour = oldEndHour + 24
    #        mpClip.SetClipProperty("End TC",str(newEndHour) + ":" + oldEndTCSplit[1]  + ":" + oldEndTCSplit[2] + ":" + oldEndTCSplit[3])
    #        print("TC for",mpClip.GetName(),"is now",mpClip.GetClipProperty("Start TC"),"->",mpClip.GetClipProperty("End TC"))
    #    else:
    #        continue
        
    
                    
        
    
# =============== UI CONFIGURATION =============

def tabsConfig(win):
    items = win.GetItems()
    
    items['MyStack'].CurrentIndex = 0
    items['MyTabs'].AddTab("Operation")
    items['MyTabs'].AddTab("Profiles Settings")
    items['MyTabs'].AddTab("Global Settings")

def treeMediaFoldersConfig(win,treeTitle:str,treeObject:str,settingsKey:str):
    '''
        Generic method to configure media folders trees
        
        Arguments:
        
            win: the window object
            treeTitle: the title for the tree
            treeObject: the tree object name
            settingsKey: the key of the json object where the folders list is stored
    '''
    items = win.GetItems()
    tree = items[treeObject]
    tree.Clear()
    hdr = tree.NewItem()
    hdr.Text[0] = treeTitle
    tree.SetHeaderItem(hdr)
    tree.ColumnCount = 1
    folders = settings.get(settingsKey,[])
    for f in folders:
        row = tree.NewItem()
        row.Text[0] = f
        tree.AddTopLevelItem(row)

def treeExtensionsConfig(win):
    items = win.GetItems()
    tree = items['treeExtensions']
    tree.Clear()
    hdr = tree.NewItem()
    hdr.Text[0] = "Extensions"
    tree.SetHeaderItem(hdr)
    tree.ColumnCount = 1
    extensions = settingsJson.get('fileExtensions',[])
    for ext in extensions:
        row = tree.NewItem()
        row.Text[0] = ext
        tree.AddTopLevelItem(row)
        
def treeCameraFoldersConfig(win):
    items = win.GetItems()
    tree = items['treeCameraFolders']
    tree.Clear()
    hdr = tree.NewItem()
    hdr.Text[0] = "Camera Folders"
    tree.SetHeaderItem(hdr)
    tree.ColumnCount = 1
    extensions = settingsJson.get('cameras',[])
    for ext in extensions:
        row = tree.NewItem()
        row.Text[0] = ext
        tree.AddTopLevelItem(row)

def addCodecsToList(codecs:list,settingsKey:str,treeConfigFunction,settingsKeysToCheck:list = []):
    """
        Arguments:
            codecs: list of codecs to add
            settingsKey: key of the settings value for the list of codecs
            treeConfigFunction: function that configure the UI list
            settingsKeysToCheck: other settings key values to check if the codec already exists
    """
    currentList = [x.upper() for x in settingsJson.get(settingsKey,[])]
    for key in settingsKeysToCheck:
        currentList += [x.upper() for x in settingsJson.get(key,[])]
    if len(currentList) == 0:
        settingsJson[settingsKey] = []
    for codec in codecs:
        if codec and not codec.upper() in currentList:
            settingsJson[settingsKey].append(codec)
            treeConfigFunction(win)
            saveSetting()
  
def treeCodecsConfig(win):
    items = win.GetItems()
    tree = items['treeCodecs']
    tree.Clear()
    hdr = tree.NewItem()
    hdr.Text[0] = "High Resolution Codecs"
    tree.SetHeaderItem(hdr)
    tree.ColumnCount = 1
    extensions = settingsJson.get('codecs',[])
    for ext in extensions:
        row = tree.NewItem()
        row.Text[0] = ext
        tree.AddTopLevelItem(row)

def treeProxyCodecsConfig(win):
    items = win.GetItems()
    tree = items['treeProxyCodecs']
    tree.Clear()
    hdr = tree.NewItem()
    hdr.Text[0] = "Proxy Codecs"
    tree.SetHeaderItem(hdr)
    tree.ColumnCount = 1
    extensions = settingsJson.get('codecsProxy',[])
    for ext in extensions:
        row = tree.NewItem()
        row.Text[0] = ext
        tree.AddTopLevelItem(row)

def refreshMainWindow():
    items = win.GetItems()
    
    items['txtNewProject'].Text = currentHouseProject
    items['txtMogPath'].Text = settings.get('mogPath','')
    items['txtFieldSep'].Text = settings.get('fieldSep','')
    items['spFieldCount'].Value = settings.get('fieldCount',5)
    items['txtSonyPath'].Text = settings.get('sonyPath','')
    items['txtAvidPath'].Text = settings.get('avidPath','')
    items['txtAAFPath'].Text = settings.get('aafPath','')
    items['ckExportStock'].Checked = settings.get('exportStock',True)
    items['ckImportStock'].Checked = settings.get('importStock',True)
    items['ckAutoImportSourceClipsIntoMediaPool'].Checked = settings.get('autoImportSourceClipsIntoMediaPool',False)
    items['txtCopyMediaPath'].Text = settings.get('copyMediaPath','')
    treeExtensionsConfig(win)
    treeCameraFoldersConfig(win)
    treeCodecsConfig(win)
    treeProxyCodecsConfig(win)
    treeMediaFoldersConfig(win,"Avid Folders","treeAvidFolders","avidFolders")
    treeMediaFoldersConfig(win,"Sony Folders","treeSonyFolders","sonyFolders")
    treeMediaFoldersConfig(win,"Mog Folders","treeMogFolders","mogFolders")
    

# =============== UI WINDOW =============
def MainWindow():
    global cbProjects
    global cbProjectsOperation

    cbProjects = ui.ComboBox({'ID':'cbProjects','ToolTip':'Changing the profile here will change the current operation profile'})
    cbProjects.AddItems(getProjects())
    cbProjects.CurrentText = currentHouseProject
    
    cbProjectsOperation = ui.ComboBox({'ID':'cbProjectsOperation','ToolTip':'Changing the profile here also change the profile in the Profiles Settings tab'})
    cbProjectsOperation.AddItems(getProjects())
    cbProjectsOperation.CurrentText = currentHouseProject
    
    profileSettingsLayout = ui.VGroup({'ID':'houseProjectLayout','Weight': 0.0},[
        ui.Label({'Text':'Profile','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
        ui.HGroup({'Weight': 0.0},[cbProjects,
                                 ui.Button({'ID':'btDeleteProject','Text':'Delete Current','Weight': 0.0})
                                   ]),
        ui.HGroup({'Weight': 0.0},[ui.LineEdit({'ID':'txtNewProject','Text':currentHouseProject}),
                                 ui.Button({'ID':'btAddProject','Text':'Add New','Weight': 0.0}),
                                 ui.Button({'ID':'btRenameProject','Text':'Rename Current','Weight': 0.0})                            
                                   ])
        ])
    
    operationProfileLayout = ui.VGroup({'ID':'houseProjectOperationLayout','Weight': 0.0},[
        ui.Label({'Text':'Profile','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
        ui.HGroup({'Weight': 0.0},[cbProjectsOperation]),
        ])
    
    
    mogPathLayout =ui.VGroup({'Weight:2.0'},
    [    
     ui.Label({'Text':'Mog Settings','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
     ui.VGap(0.2), 
     ui.HGroup({'Weight': 0.0},
        [   ui.Label({'Text':'MOG Path','FixedSize':[70,30]}),
            ui.LineEdit({'ID':'txtMogPath','Text':settings.get('mogPath',''),'MinimumSize':[400,30]}),
            ui.Button({'ID':'btBrowseMog','Text':'Browse','Weight': 0.0})         
        ]
    ),ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeMogFolders",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 1.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddMogFolder','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveMogFolder','Text':'Remove','Weight': 0.0}),
            ])
            ])
    
    ])

    extractionLayout = ui.HGroup(
        [   ui.Label({'Text':'Field Separator','FixedSize':[100,30]}),
            ui.LineEdit({'ID':'txtFieldSep','Text':settings.get('fieldSep','_')}),
            ui.HGap(5),
            ui.Label({'Text':'Field Count','FixedSize':[100,30]}),
            ui.SpinBox({'ID':'spFieldCount','Value':settings.get('fieldCount',5),'Minimum':1,'Maximum':32,'SingleStep':1}),
        ]
    )
    
    sonyPathLayout = ui.VGroup({'Weight:2.0'},
    [ 
    ui.Label({'Text':'Sony and Other Cameras Settings','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
    ui.VGap(0.2),
     ui.HGroup({'Weight': 0.0},
        [   ui.Label({'Text':'SONY/OTHER Path','FixedSize':[75,30]}),
            ui.LineEdit({'ID':'txtSonyPath','Text':settings.get('sonyPath',''),'MinimumSize':[400,30]}),
            ui.Button({'ID':'btBrowseSony','Text':'Browse','Weight': 0.0})
        ]
    ),ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeSonyFolders",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 1.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddSonyFolder','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveSonyFolder','Text':'Remove','Weight': 0.0}),
            ])
            ])
    ])
    
    avidPathLayout = ui.VGroup({'Weight:2.0'},
    [ 
     ui.Label({'Text':'Avid','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
     ui.VGap(2),
     ui.HGroup({'Weight': 0.0},
        [   ui.Label({'Text':'AVID Path','FixedSize':[60,30]}),
            ui.LineEdit({'ID':'txtAvidPath','Text':settings.get('avidPath',''),'MinimumSize':[400,30]}),
            ui.Button({'ID':'btBrowseAvid','Text':'Browse','Weight': 0.0}),
            
        ]
    ),ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeAvidFolders",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 1.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddAvidFolder','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveAvidFolder','Text':'Remove','Weight': 0.0}),
            ])
            ])
    ])
    
    """
    motionPathLayout = ui.HGroup(
        [   ui.Label({'Text':'MOTION Path','FixedSize':[60,30]}),
            ui.LineEdit({'ID':'txtMotionPath','Text':settings['motionPath'],'MinimumSize':[400,30]}),
        ]
    )
    """
    
    importAAFLayout = ui.VGroup({'Weight': 0.0,'StyleSheet':'QGroupBox {border: 1px solid white}'},[
        ui.Label({'Text':'Import AFF','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
        ui.VGap(2),
        ui.HGroup({'Weight': 0.0},[
        ui.LineEdit({'ID':'txtAAFPath','Text':settings.get('aafPath','')}),
        ui.Button({'ID':'btBrowseAAF','Text':'Browse','Weight': 0.0}),
        ui.Button({'ID':'btImportAAF','Text':'Import AAF','Weight': 0.0}),
    ]),
        ui.HGroup({'Weight': 0.0},[
            ui.CheckBox({'ID':'ckExportStock','Text':'Export Stock Bin','Checked':settings.get('exportStock',True),'ToolTip':"Export the stock bin to " + settings.get('avidPath','') + " after importing the media"}),
            ui.CheckBox({'ID':'ckImportStock','Text':'Import Stock Bin','Checked':settings.get('importStock',True),'ToolTip':"Import the saved stock bin from disk if the stock folder does not exist"}),
            ui.CheckBox({'ID':'ckAutoImportSourceClipsIntoMediaPool','Text':'Auto Import Source Clips Into MediaPool','Checked':settings.get("autoImportSourceClipsIntoMediaPool",False),
                         'ToolTip':"Use if you want to import and link the timeline to the source clips. Use this with a Avid Edge workflow.",'StyleSheet':'color: ' + typeColor['AUTO']}),
            #autoImportSourceClipsIntoMediaPool       
                   ])
        ])  
    
    conformLayout = ui.VGroup({'Weight': 0.0},[
        ui.Label({'Text':'Conforming','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
         ui.VGap(0.2),
         ui.VGroup({'Weight': 0.0},[
         ui.Button({'ID':'btConformSony','Text':'Conform SONY','Weight': 0.0,'StyleSheet':'color: ' + typeColor['SONY']}),
         ui.Button({'ID':'btConformOthers','Text':'Conform OTHER cameras','Weight': 0.0,'StyleSheet':'color: ' + typeColor['OTHER'] }),
         ui.Button({'ID':'btConformMog','Text':'Conform MOG','Weight': 0.0,'StyleSheet':'color:' + typeColor['MOG']}),
         ui.Button({'ID':'btConformAll','Text':'Conform ALL media types','Weight': 0.0})]),
    ])
        
    copyMediaLayout = ui.VGroup({'Weight': 0.0},[
        ui.Label({'Text':'Copy files to edit storage and relink','Alignment':{'AlignTop' : True,'AlignCenter' : True},'StyleSheet':'border: 1px white;border-style: solid none none none'}),
        ui.VGap(2),
        ui.HGroup({'Weight': 0.0},[
        ui.Label({'Text':'Destination','FixedSize':[70,30]}),
        ui.LineEdit({'ID':'txtCopyMediaPath','Text':settings.get('copyMediaPath',"")}),
        ui.Button({'ID':'btBrowseCopyMedia','Text':'Browse','Weight': 0.0}),
        ui.Button({'ID':'btCopyMedia','Text':'Copy Media','Weight': 0.0}),
    ])
        ,ui.Button({'ID':'btDeleteMedia','Text':'Delete files from edit storage','ToolTip':'Delete files from "' + settings.get('copyMediaPath','None') + '" that exists in the media folder (High Res Files)'})
        ]
        
    )
    
    vLayoutOperation = ui.VGroup({'Weight': 0.0},
        [ 
         ui.Label({'Text':'<p><a href="https://github.com/c0ntact0/DAVINCI_CONFORM_MOG/blob/main/README.md#versions" target="_blank">Versions</a></p>',
                   'Alignment':{'AlignTop' : True},'OpenExternalLinks':True,'Weight': 0.0}),
         ui.VGap(0.2),
         operationProfileLayout,
         ui.VGap(0.2),
         importAAFLayout,
         ui.VGap(0.2),
         conformLayout,
         ui.VGap(0.2),
         copyMediaLayout,
         ui.VGap(0.2),
         
         ui.Label({'Text':'<img alt="" src="data:image/png;base64,' + ICON + '">', 'Alignment':{'AlignVCenter' : True,'AlignCenter': True},'OpenExternalLinks':True,'Weight': 2.0})
         #,ui.Button({'ID':'btTeste','Text':'Teste'})
         ]
        
    )
    
    vLayoutProfiles = ui.VGroup({'Weight': 0.0},[
        profileSettingsLayout,
         ui.VGap(0.2),
         mogPathLayout,
         ui.VGap(2),
         extractionLayout,
         ui.VGap(5),
         sonyPathLayout,
         ui.VGap(0.2),
         avidPathLayout,
    ])
    
    vLayoutSettings =  ui.HGroup({'Weight': 0.0},[
            ui.VGroup({'Weight': 2.0},[
            ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeExtensions",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 1.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddExtension','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveExtension','Text':'Remove','Weight': 0.0}),
                ui.Button({'ID':'btImportExtensions','Text':'Import','Weight': 0.0}),
            ])
            ]),
            ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeCodecs",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 3.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddCodec','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveCodec','Text':'Remove','Weight': 0.0}),
                ui.Button({'ID':'btSendToProxy','Text':'Send To\nProxy','Weight': 0.0}),
                ui.Button({'ID':'btImportFromTimeline','Text':'Import From\nTimeline','Weight': 0.0}),
            ])
            ]),
            ui.HGroup({'Weight': 10.0},[
            ui.Tree({
			"ID": "treeProxyCodecs",
			"SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 3.0})
            ,
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddProxyCodec','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveProxyCodec','Text':'Remove','Weight': 0.0}),
            ])
            ])
            ]),
            
            ui.HGap(20),
             
            ui.VGroup({'Weight': 2.0},[
                ui.Label({'Text':'Sony cameras with the \"Clip\" folder are already included in the \"Conform SONY\" process.','WordWrap':True,
                          'Alignment':{'AlignTop' : True},'Weight': 1.0}),
                ui.VGap(4),
                ui.HGroup({'Weight': 20.0},[
                    ui.Tree({
			            "ID": "treeCameraFolders",
			            "SortingEnabled": True,'SelectionMode':'ExtendedSelection','Weight': 2.0}),
            ui.VGroup({'Weight': 0.0},[
                ui.Button({'ID':'btAddCameraFolder','Text':'Add','Weight': 0.0}),
                ui.Button({'ID':'btRemoveCameraFolder','Text':'Remove','Weight': 0.0}),
                ui.Button({'ID':'btImportCameraFolder','Text':'Import','Weight': 0.0}),
            ])
            ])
            ])
        ])
    
    
    vLayoutMainWindow = ui.VGroup({'Weight': 0.0},[
        ui.TabBar({'Weight':0.0,'ID':'MyTabs'}),
        ui.Stack({'Weight':1.0,'ID':'MyStack'},[
            vLayoutOperation,
            vLayoutProfiles,
            vLayoutSettings            
        ])
    ])
        
    geoDic = settingsJson['windowGeometry']
    geometry = [geoDic['1'],geoDic['2'],geoDic['3'],geoDic['4']]
    win = dispatcher.AddWindow({'WindowTitle':'ConformAll (Rui Loureiro 2025)','ID':'mainWindow','Geometry':geometry},vLayoutMainWindow)
    #pprint(win.GetItems())
    
    tabsConfig(win)
    treeExtensionsConfig(win)
    treeCameraFoldersConfig(win)
    treeCodecsConfig(win)
    treeProxyCodecsConfig(win)
    treeMediaFoldersConfig(win,"Avid Folders","treeAvidFolders","avidFolders")
    treeMediaFoldersConfig(win,"Sony Folders","treeSonyFolders","sonyFolders")
    treeMediaFoldersConfig(win,"Mog Folders","treeMogFolders","mogFolders")
    
    win.On.btConformMog.Clicked = BtConformMog
    win.On.btConformSony.Clicked = BtConformCameras
    win.On.btConformOthers.Clicked = BtConformCameras
    
    win.On.btConformAll.Clicked = BtConformAll
    win.On.btImportAAF.Clicked = BtImportAAF
    win.On.cbProjects.CurrentIndexChanged = ProjectChanged
    win.On.cbProjectsOperation.CurrentIndexChanged = ProjectChanged
    win.On.btDeleteProject.Clicked = DeleteProject
    win.On.btAddProject.Clicked = AddProject
    win.On.btRenameProject.Clicked = RenameProject
    win.On.btCopyMedia.Clicked = OnCopyMedia
    win.On.btDeleteMedia.Clicked = OnDeleteMedia
    
    win.On.btBrowseMog.Clicked = OnBrowse
    win.On.btBrowseSony.Clicked = OnBrowse
    win.On.btBrowseAvid.Clicked = OnBrowse
    win.On.btBrowseAAF.Clicked = OnBrowse
    win.On.btBrowseCopyMedia.Clicked = OnBrowse
    win.On.btImportExtensions.Clicked = OnBrowse
    win.On.btImportCameraFolder.Clicked = OnBrowse
    win.On.MyTabs.CurrentChanged = OnTabChanged
    win.On.btAddExtension.Clicked = OnExtensionsList
    win.On.btRemoveExtension.Clicked = OnExtensionsList
    win.On.btAddCameraFolder.Clicked = OnCamerasList
    win.On.btRemoveCameraFolder.Clicked = OnCamerasList
    win.On.btAddCodec.Clicked = OnCodecsList
    win.On.btRemoveCodec.Clicked = OnCodecsList
    win.On.btSendToProxy.Clicked = OnCodecsList
    win.On.btImportFromTimeline.Clicked = OnCodecsList
    win.On.btAddProxyCodec.Clicked = OnProxyCodecsList
    win.On.btRemoveProxyCodec.Clicked = OnProxyCodecsList
    win.On.btSendToHigh.Clicked = OnProxyCodecsList
    
    win.On.btAddAvidFolder.Clicked = OnMediaFoldersList
    win.On.btRemoveAvidFolder.Clicked = OnMediaFoldersList
    win.On.btAddMogFolder.Clicked = OnMediaFoldersList
    win.On.btRemoveMogFolder.Clicked = OnMediaFoldersList
    win.On.btAddSonyFolder.Clicked = OnMediaFoldersList
    win.On.btRemoveSonyFolder.Clicked = OnMediaFoldersList
    
    win.On.mainWindow.Close = OnClose
   
    win.On.btTeste.Clicked = OnTeste

    return win

def errorPopupDialog(label:str=""):
    '''
        Custom popup dialog for errors.
        
        Arguments:

            label: some text to show.
            
        Returns:

            A tuple: (dialog object, dict with the dialog elements)
    '''
    
    def OnErrorDialogClose(ev):
        dispatcher.ExitLoop()
    
    fontSize = ui.Font().PixelSize
    labelLines = len(label)*fontSize/580
    arrLabel = label.split('\n')
    labelLines+=len(arrLabel)
    labelH = labelLines*fontSize if len(label)*fontSize > 580 else 30
    
    windowH = 50+labelH
   
    errorDialog = dispatcher.AddDialog({'WindowTitle':'Error','ID':'errorDialog','MinimumSize':[600,windowH],'MaximumSize':[600,windowH],'Weight': 0.0},
                                  ui.VGroup({'Weight': 0.0,'Width':0.0},[
                                      ui.Label({'ID':'Label','Text':label,'WordWrap': True,'Alignment':{'AlignTop' : True},'MinimumSize':[580,labelH],'MaximumSize':[580,labelH]}),
                                   ui.Button({'ID':'btCloseDialog','Text':'Close','Weight': 0.0})]))
    errorDialog.On.btCloseDialog.Clicked = OnErrorDialogClose
    items = errorDialog.GetItems()
    
    buttonsEnabled(False)
    errorDialog.Show()
    dispatcher.RunLoop()
    errorDialog.Hide()
    buttonsEnabled(True)
    return errorDialog,items

def genericPopupDialog(label:str="",acceptButtonText:str="OK",rejectButtonText:str="Cancel",haveInput:bool=False,haveRejectButton:bool=False):
    
    """
        A generic popup dialog to present messages to the user.
        The dialog can have a optional reject button, i.e. Cancel button, and a optional input text field.
        The input text can be accessed using the elements dict like "items['LineEdit'].Text". 
        
        Arguments:
        
            label: some text to show.
            acceptButtonText: text for the accept button (default "OK").
            rejectButtonText: text for the reject button (default "Cancel"). The haveRejectButton argument must be True to turn this button visible.
            haveInput: turn the optional 

        Return: 
        
            A tuple: (accepted (boolean),dialog object,dialog elements (dict))
    """
      
    def OnGenericPopupDialog(ev):
        
        who = ev['who']
        if who == "btCancelInputDialog":
            if haveInput:
                items['LineEdit'].Clear()
        elif who == "btOkInputDialog":
            bt = items['btOkInputDialog']
            bt.Checked = True    
        dispatcher.ExitLoop()
    
    fontSize = ui.Font().PixelSize
    labelLines = len(label)*fontSize/580
    arrLabel = label.split('\n')
    labelLines+=len(arrLabel)
    labelH = labelLines*fontSize if len(label)*fontSize > 580 else 30
    
    textEditGap = 5 if haveInput else 0
    windowH = 133+labelH
    windowH = windowH - 30 if not haveInput else windowH
    inputDialog = dispatcher.AddDialog({'WindowTitle':'Input Dialog','ID':'inputDialog','MinimumSize':[600,windowH],'MaximumSize':[600,windowH],'Weight': 5},
                                        ui.VGroup({'Weight': 0},[
                                        ui.Label({'Text':label,'ID':'Label','WordWrap': True,'Alignment':{'AlignTop' : True},'MinimumSize':[580,labelH],'MaximumSize':[580,labelH]}),#,'FrameStyle': 20 | 6}),
                                        ui.VGap(textEditGap),
                                        ui.VGap(0) if not haveInput else ui.LineEdit({'ID':'LineEdit','MinimumSize':[580,30],'MaximumSize':[580,30],'Visible':haveInput}),
                                        ui.VGap(5),
                                           ui.HGroup({'Weight': 0},[
                                               ui.Button({'Text':acceptButtonText,'ID':'btOkInputDialog','Checkable':True}),
                                               ui.VGap(0) if not haveRejectButton else ui.Button({'Text':rejectButtonText,'ID':'btCancelInputDialog'}),
                                               ])
                                       ]))
    items = inputDialog.GetItems()
    inputDialog.On.btOkInputDialog.Clicked = OnGenericPopupDialog
    inputDialog.On.btCancelInputDialog.Clicked = OnGenericPopupDialog
    
    buttonsEnabled(False)
    inputDialog.Show()
    dispatcher.RunLoop()
    inputDialog.Hide()
    buttonsEnabled(True)
    return items['btOkInputDialog'].Checked,inputDialog,items

def copyFilesDialog():
    canceled = False
    
    def run(ev):
        for i in range(10):
            if canceled:
                break
            bmd.wait(1)
            print(i)
        
        dispatcher.ExitLoop()
        
    def OnCancel(ev):
        global canceled
        
        print("Canceled")
        canceled = True
    
    copyDialog = dispatcher.AddDialog({'WindowTitle':'Input Dialog','ID':'inputDialog','FixedSize':[420,133]},
                                      ui.VGroup([
                                          
                                        ui.Button({'Text':'Cancel','ID':'btCancel'})  
                                      ]))
    
    timer = ui.Timer({'ID':'Timer','SingleShot':True,'Interval':1000})
    ui.QueueEvent('Timer', 'Timeout', {})
    copyDialog.On.btCancel.Clicked = OnCancel
    dispatcher.On.Timer.Timeout = run
    
    items = copyDialog.GetItems()
    pprint(items)
    copyDialog.Show()
    timer.Start()
    
    print(timer.SingleShot,timer.Interval,timer.GetTimerID(),timer.IsActive,timer.RemainingTime)
    dispatcher.RunLoop()

    copyDialog.Hide()
    
################# MAIN ###################
if __name__ == "__main__":


    loadSettings()
    currentHouseProject = settingsJson['currentProject']
    getSettings(currentHouseProject)
    
    mediaStorage = resolve.GetMediaStorage()
    #fusion = resolve.Fusion()
    fu.ShowConsole(True)
    
    pm = resolve.GetProjectManager()
    ui = fu.UIManager
    dispatcher = bmd.UIDispatcher(ui)

    currentProject = pm.GetCurrentProject()
    #pprint(currentProject.GetSetting())
    print_info("Current DaVinci Resolve project:",currentProject.GetName())
    #pprint(currentProject.GetSetting())
    currentTimeline = currentProject.GetCurrentTimeline()
    mediaPool = currentProject.GetMediaPool()
    win = MainWindow()
    if areFoldersOk():
        win.Show()
        dispatcher.RunLoop()
    win.Hide()