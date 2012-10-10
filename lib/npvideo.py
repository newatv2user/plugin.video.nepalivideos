'''
Created on May 15, 2012

@author: newatv2user
'''
import Common
from Common import MediaItem
import CommonFunctions
import sys
import re
import urllib
import xbmcplugin, xbmcgui, xbmc
from xbmcgui import ListItem
import hosts

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

BASE_URL = 'http://www.npvideo.com/%s'
BASE_URL2 = 'http://www.npvideo.com%s'
HOME = 'index.php'
site = 'npvideo'

pluginhandle = int(sys.argv[1])

def Main():
    print 'npvideo main'
    data = Common.save_web_page(BASE_URL % HOME, 'npvideo.html')
    #data = Common.load_local_page('npvideo.html')
    menu = common.parseDOM(data, "div", attrs={ "id": "nav"})[0]
    menuItems = common.parseDOM(menu, "li")
    MediaItems = []
    for menuItem in menuItems:
        Mediaitem = MediaItem()
        Title = common.parseDOM(menuItem, "a", ret="title")
        if not Title:
            altTitle = common.stripTags(menuItem)
            if altTitle == 'Live TV':
                Title = 'Live TV'
            elif altTitle == 'Home':
                Title = 'Home'
            else:
                continue
        else:
            Title = Title[0] 
        Href = common.parseDOM(menuItem, "a", ret="href")
        if not Href:
            continue
        
        if Title == 'Live TV':
            Mediaitem.Mode = 'browselive'
            Href = Href[0]
            Url = urllib.quote_plus(BASE_URL % Href)
        elif Title == 'Home':
            Mediaitem.Mode = 'browsehome'
            Url = ''
        else:
            Mediaitem.Mode = 'browse'
            Href = Href[0]
            Url = urllib.quote_plus(BASE_URL % Href)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        Mediaitem.Image = Common.search_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)

def browse(url=None):
    if not url:
        url = Common.args.url
    print 'npvideo browse'
    #data = Common.save_web_page(url, 'npvidcat.html')
    #data = Common.load_local_page('npvidcat.html')
    data = Common.getURL(url)
    videolistdiv = common.parseDOM(data, "div", attrs={ "id": "categoryvidlist"})[0]
    videolist = common.parseDOM(videolistdiv, "li")
    MediaItems = []
    for video in videolist:
        Mediaitem = MediaItem()
        Title = common.parseDOM(video, "a", ret="title")
        if not Title:
            continue
        Title = Title[0] 
        Title = common.replaceHTMLCodes(Title)
        Title = Title.encode('utf-8')
        Href = common.parseDOM(video, "a", ret="href")
        if not Href:
            continue
        Href = Href[0]
        Href = common.replaceHTMLCodes(Href)
        Href = Href.encode('utf-8')
        Url = urllib.quote_plus(BASE_URL % Href)     
        Mediaitem.Mode = 'play'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.search_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        #Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    
    right = common.parseDOM(videolistdiv, "div", attrs={ "class": "right"})
    if right:
        right = right[0]
        selected = common.parseDOM(right, "span", attrs={ "class": "selected" })
        if selected:
            selected = selected[0]
            selected = int(selected)
            nextPage = selected + 1
            pages = re.compile("<a href='(.+?)' class='bound' title=.+?>([\d]{0,})</a>").findall(right)
            for href, num in pages:
                if int(num) == nextPage:
                    # Add next page
                    Mediaitem = MediaItem()
                    Title = 'Next'
                    Url = urllib.quote_plus(BASE_URL % href)
                    Mediaitem.Image = Common.next_thumb   
                    Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
                    Mediaitem.Mode = 'browse'
                    Mediaitem.ListItem.setInfo('video', { 'Title': Title})
                    Mediaitem.ListItem.setLabel(Title)
                    Mediaitem.Isfolder = True
                    Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
                    Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
                    MediaItems.append(Mediaitem)    
                    break
    
    Common.addDir(MediaItems)    

def browselive(url=None):
    if not url:
        url = Common.args.url
    print 'npvideo browselive'
    data = Common.getURL(url)
    livetvicons = common.parseDOM(data, "div", attrs={ "id": "rvid"})[0]
    items = common.parseDOM(livetvicons, "li")
    MediaItems = []
    for item in items:
        #print 'inside for'
        Mediaitem = MediaItem()
        Title = common.parseDOM(item, "a")
        if not Title:
            print 'no title'
            continue
        Title = Title[0]
        Title = common.replaceHTMLCodes(Title)
        Title = Title.encode('utf-8')
        Href = common.parseDOM(item, "a", ret="href")
        if not Href:
            print 'no href'
            continue
        Href = Href[0]
        Url = urllib.quote_plus(BASE_URL % Href)
        Mediaitem.Mode = 'playlive'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)
    
def browsehome():
    print 'npvideo browsehome'
    data = Common.load_local_page('npvideo.html')
    latestvideodiv = common.parseDOM(data, "div", attrs={ "id": "recentvidlist"})[0]
    items = common.parseDOM(latestvideodiv, "li")
    MediaItems = []
    for item in items:
        #print 'inside for'
        Mediaitem = MediaItem()
        Title = common.parseDOM(item, "a", ret="title")
        if not Title:
            print 'no title'
            continue
        Title = Title[0]
        Title = common.replaceHTMLCodes(Title)
        Title = Title.encode('utf-8')
        #Title = Title.encode('ascii', 'ignore')
        #print Title
        Href = common.parseDOM(item, "a", ret="href")
        if not Href:
            print 'no href'
            continue
        Href = Href[0]
        Href = common.replaceHTMLCodes(Href)
        Href = Href.encode('utf-8')        
        Url = urllib.quote_plus(BASE_URL % Href)
        Mediaitem.Mode = 'play'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        #Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)
        
def play(url=None):
    if not url:
        url = Common.args.url
    data = Common.getURL(url)
    videoborderbox = common.parseDOM(data, "div", attrs={ "id": "videoarea" })[0]
    Title = common.parseDOM(videoborderbox, "div", {"id": "videotitle"})[0]
    Title = common.replaceHTMLCodes(Title)
    Title = Title.encode('utf-8')
    videoplayer = common.parseDOM(videoborderbox, "div", attrs={ "id": "videodisplay"})[0]
    # Resolve media url using videohosts
    videoUrl = None
    videoUrl = hosts.resolve(videoplayer)
    #videoUrl = None 
    if not videoUrl:
        dialog = xbmcgui.Dialog()
        dialog.ok('Nothing to play', 'A playable url could not be found.')
        return                
    else:
        #print videoUrl
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        count = 1
        for PlayItem in videoUrl:
            Title = Title + ' Part ' + str(count)
            listitem = ListItem(Title, iconImage='', thumbnailImage='')
            listitem.setInfo('video', { 'Title': Title})
            playList.add(url=PlayItem, listitem=listitem)
            count = count + 1
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)

def playlive(url=None):
    if not url:
        url = Common.args.url
    print 'npvideo playlive'
    data = Common.save_web_page(url, 'nplive.html')
    videoplayerbox = common.parseDOM(data, "div", attrs={ "class": "liveTv"})[0]
    scriptlinks = common.parseDOM(videoplayerbox, "script", ret="src")
    videoUrl = None
    if scriptlinks:
        for link in scriptlinks:
            if "swfobject" in link or "jquery" in link:
                continue            
            videoUrl = getRtmp(BASE_URL2 % link, url)
    
    if not videoUrl:
        embeds = common.parseDOM(videoplayerbox, "embed", ret="src")
        if embeds:
            if "mms" in embeds[0]:
                videoUrl = embeds[0]
    if not videoUrl:
        EMBED = common.parseDOM(videoplayerbox, "EMBED", ret="src")
        if EMBED:
            if "rtsp" in EMBED[0]:
                videoUrl = EMBED[0]
    
    if not videoUrl:
        xbmcplugin.setResolvedUrl(pluginhandle, False, xbmcgui.ListItem())
        print 'Video not found.'        
    else:
        #print videoUrl
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=videoUrl))

def getRtmp(url, pageurl=False):
    print 'npvideo getRtmp'
    Src = Common.getURL(url)
    rtmp = re.compile("'streamer', '(rtmp://[^']+)'").findall(Src)
    if not rtmp:
        return None
    else:
        rtmp = rtmp[0]
    app = re.compile("rtmp://.+?/([^&']+)").findall(rtmp)
    if app:
        rtmp += ' app=' + app[0]
    playpath = re.compile("'file', '([^']+)'").findall(Src)
    if not playpath:
        return None
    else:
        rtmp += ' playpath=' + playpath[0]
    swfUrl = 'http://www.npvideo.com/config-js/player.swf'
    rtmp += ' swfurl=' + swfUrl
    if pageurl:
        rtmp += ' pageurl=' + pageurl
    rtmp += ' live=1'
    return rtmp
