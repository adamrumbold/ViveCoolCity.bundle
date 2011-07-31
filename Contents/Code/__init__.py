# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import re
####################################################################################################

VIDEO_PREFIX = "/video/ViveCoolCity"
NAME = L('Title')
c_VERSION = 1.2

DEFAULT_CACHE_INTERVAL = 1800
OTHER_CACHE_INTERVAL = 300

ART           = 'vive-background.jpg'
ICON          = 'VCC-Logow.png'

BROWSE_URL = "http://www.vivecoolcity.com/archive/"

####################################################################################################

def Start():
    
    Log("In Start")
    
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)
    
    HTTP.SetCacheTime(DEFAULT_CACHE_INTERVAL)

####################################################################################################


#setup the Main Video Menu - ie. get Top level categories
def VideoMainMenu():
    
    dir = MediaContainer(viewGroup="InfoList")
    myNamespaces = {'ns1':'http://www.w3.org/1999/xhtml'}
    xml = XML.ElementFromURL(BROWSE_URL,True)
    xpathQuery = ""
    dir.Append(Function(DirectoryItem(TopMenuHandler, title='Every Episode We''ve Done', thumb='http://vivecoolcity.com/images/archive-EveryEp.gif'), ShowUrl='http://www.vivecoolcity.com/archive/all/', ShowTitle='all'))
    dir.Append(Function(DirectoryItem(TopMenuHandler, title='Best', thumb='http://vivecoolcity.com/images/archive-BestClips.gif'), ShowUrl='http://www.vivecoolcity.com/archive/best', ShowTitle='best'))
    dir.Append(Function(DirectoryItem(TopMenuHandler, title='How To''s', thumb='http://vivecoolcity.com/images/archive-HowTo.gif'), ShowUrl='http://www.vivecoolcity.com/archive/howto', ShowTitle='how to'))
    
    return dir

def TopMenuHandler(sender, ShowUrl, ShowTitle):
    
    dir = MediaContainer(title1="ViveCoolCity", title2=ShowTitle, viewGroup="InfoList")
    Log ("ShowTitle = " + ShowTitle)
    if ShowTitle == 'all':
        Log ("attempting to build for all")
        xml = XML.ElementFromURL(ShowUrl,True)
        myNamespaces = {'ns1':'http://www.w3.org/1999/xhtml'}
        xpathQuery = "//tr[.]/td[.]"
        Cat = xml.xpath(xpathQuery, namespaces=myNamespaces)
        Log("Number of shows = " + str(len(Cat)))
        
        for Entry in xml.xpath(xpathQuery, namespaces=myNamespaces):
            episode = {}
            episode['Title'] = Entry.xpath("span[3]")[0].text
            episode['SubTitle'] = str(Entry.xpath("span[1]")[0].text) + " -- " +  str(Entry.xpath("span[2]")[0].text)
            Log(episode['SubTitle'])
            episode['Thumb'] = Entry.xpath("a/img")[0].get('src')
            try:
                episode['Summary'] = Entry.xpath("span[4]")[0].text
            except:
                episode['Summary'] = "Error reading summary"
                #this is due to the encoding - needs to be resolved
            episode['Url'] = Entry.xpath("a")[0].get('href')
            dir.Append(Function(VideoItem(PlayVideo, title=episode['Title'],  subtitle=episode['SubTitle'], summary=episode['Summary'], thumb=episode['Thumb']), url=episode['Url']))
            
    if ShowTitle == "best":
        Log("Attempting to build for best")
        xml = XML.ElementFromURL(ShowUrl,True)
        myNamespaces = {'ns1':'http://www.w3.org/1999/xhtml'}
        xpathQuery = "//div[.]//table//tr[.]"
        Cat = xml.xpath(xpathQuery, namespaces=myNamespaces)
        Log("Number of shows = " + str(len(Cat)))
        for Entry in xml.xpath(xpathQuery, namespaces=myNamespaces):
            episode = {}
            episode['Title'] = Entry.xpath("td[3]/span[1]")[0].text
            episode['SubTitle'] = Entry.xpath("td[3]/span[2]")[0].text
            Log(episode['SubTitle'])
            episode['Thumb'] = Entry.xpath("td[2]/a/img")[0].get('src')
            episode['Summary'] = Entry.xpath("td[3]/p")[0].text
            episode['Url'] = Entry.xpath("td/a")[0].get('href')
            dir.Append(Function(VideoItem(PlayVideo, title=episode['Title'],  subtitle=episode['SubTitle'], summary=episode['Summary'], thumb=episode['Thumb']), url=episode['Url']))
        
    
    if  ShowTitle == "how to":
        Log("Attempting to build for how to")
        xml = XML.ElementFromURL(ShowUrl,True)
        myNamespaces = {'ns1':'http://www.w3.org/1999/xhtml'}
        xpathQuery = "//div[.]//table//tr[.]"
        Cat = xml.xpath(xpathQuery, namespaces=myNamespaces)
        Log("Number of shows = " + str(len(Cat)))
        for Entry in xml.xpath(xpathQuery, namespaces=myNamespaces):
            episode = {}
            episode['Title'] = Entry.xpath("td[2]/span[1]")[0].text
            episode['SubTitle'] = Entry.xpath("td[2]/span[2]")[0].text
            Log(episode['SubTitle'])
            episode['Thumb'] = Entry.xpath("td[1]/a/img")[0].get('src')
            episode['Summary'] = Entry.xpath("td[2]/p")[0].text
            episode['Url'] = Entry.xpath("td/a")[0].get('href')
            dir.Append(Function(VideoItem(PlayVideo, title=episode['Title'],  subtitle=episode['SubTitle'], summary=episode['Summary'], thumb=episode['Thumb']), url=episode['Url']))
        
    return dir
    
def PlayVideo(sender, url):
  videopage = HTTP.Request(url)
  vidurl  = re.search("QTObject\(\"(.+?)\"", videopage).group(0)
  vidurl = vidurl[10:len(vidurl)-1]
  Log("##" + vidurl)
  Log("trying to play through redirect")
  return Redirect(vidurl)