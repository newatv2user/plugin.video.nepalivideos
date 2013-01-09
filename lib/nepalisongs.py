'''
Created on May 22, 2012

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
common.dbg = True
common.dbglevel = 3

BASE_URL = 'http://nepalisongs.tv/newvideos.html'
HOME_URL = 'http://nepalisongs.tv/'
site = 'nepalisongs'
pluginhandle = int(sys.argv[1])

def Main():
    print 'nepalisongs Main'
    browse(BASE_URL)
    
def browse(url=None):
    if not url:
        url = Common.args.url
    print 'nepalisongs browse'
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    data = Common.getURL(url)
    #data = Common.save_web_page(url, 'nepalisongs.html')
    #data = Common.load_local_page('npvideo.html')
    data = unicode(data, 'utf-8', 'ignore')
    videolist = common.parseDOM(data, "ul", attrs={ "class": "top-videos-list"})[0]
    menuItems = common.parseDOM(videolist, "li")
    MediaItems = []
    for menuItem in menuItems:
        Mediaitem = MediaItem()
        spans = common.parseDOM(menuItem, "span")
        if len(spans) == 3:
            Artist = spans[0]
            #print Artist
            Title = spans[1]
            Title = common.stripTags(Title)
            Detail = Artist + '\n' + spans[2]
        else:
            continue
         
        Href = common.parseDOM(menuItem, "a", ret="href")
        if not Href:
            continue
        Mediaitem.Mode = 'play'
        Href = Href[0]
        Url = urllib.quote_plus(Href)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Artist': Artist, 'Plot': Detail})
        Mediaitem.ListItem.setLabel(Title)
        Img = common.parseDOM(menuItem, "img", ret="src")
        if Img:
            Mediaitem.Image = Img[0]
        else:
            Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    # Next Page
    pagination = common.parseDOM(data, "div", attrs={ "class": "pagination" })[0]
    nextHref = re.compile('href="([^"]+)">next').findall(pagination)
    if nextHref:
        Href = nextHref[0]
        Href = common.replaceHTMLCodes(Href)
        Mediaitem = MediaItem()
        Title = 'Next'
        Url = urllib.quote_plus(HOME_URL + Href)
        Mediaitem.Image = Common.next_thumb
        Mediaitem.Mode = 'browse'
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)
    Common.SetViewMode()

def play(url=None):
    if not url:
        url = Common.args.url
    data = Common.getURL(url)
    playerholder = common.parseDOM(data, "div", attrs={ "id": "Playerholder" })[0]
    # Resolve media url using videohosts
    videoUrl = None
    videoUrl = hosts.resolve(playerholder)
    #videoUrl = None 
    if videoUrl:
        #print videoUrl
        Url = videoUrl[0]
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=Url))
