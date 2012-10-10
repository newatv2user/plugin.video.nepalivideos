'''
Created on Jul 9, 2012

@author: newatv2user
'''

import Common
from Common import MediaItem
import CommonFunctions
import sys
import urllib
import xbmcplugin, xbmcgui, xbmc
from xbmcgui import ListItem
import hosts

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

BASE_URL = 'http://www.enternepal.net'
site = 'enternepal'
pluginhandle = int(sys.argv[1])

def Main():
    print 'enternepal Main'
    Menu = [('Music Videos', BASE_URL + '/category/music-videos', Common.video_thumb, 'browse'),
            ('Video Gallery', BASE_URL + '/video-gallery', Common.video_thumb, 'browse')]
    MediaItems = []
    for Title, Url, Thumb, Mode in Menu:
        Mediaitem = MediaItem()
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        Mediaitem.Image = Thumb
        Mediaitem.Mode = Mode
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)
    
def browse(url=None):
    if not url:
        url = Common.args.url
    print 'enternepal browse'
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    data = Common.getURL(url)
    #data = Common.save_web_page(url, 'nepalisongs.html')
    #data = Common.load_local_page('npvideo.html')
    videolist = common.parseDOM(data, "div", attrs={ "class": "category_video.*?"})    
    MediaItems = []
    for menuItem in videolist:
        Href = common.parseDOM(menuItem, "a", ret="href")
        if not Href:
            continue
        Href = Href[0]
        
        Image = common.parseDOM(menuItem, "img", ret="src")
        if not Image:
            Image = ''
        else:
            Image = Image[0]
            
        Title = common.parseDOM(menuItem, "img", ret="title")
        if not Title:
            continue
        Title = Title[0]
        Title = common.replaceHTMLCodes(Title)
        
        Plot = common.parseDOM(menuItem, "div", {"class": "title"})
        if not Plot:
            Plot = ''
        else:
            Plot = Plot[0]
            
        Mediaitem = MediaItem()
        
        Mediaitem.Mode = 'play'
        Url = urllib.quote_plus(Href)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Image
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    # Next Page
    pagination = common.parseDOM(data, "a", { "class": "nextpostslink" }, ret="href")
    if pagination:
        Href = pagination[0]
        Href = common.replaceHTMLCodes(Href)
        Mediaitem = MediaItem()
        Title = 'Next'
        Url = urllib.quote_plus(Href)
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
    playerholder = common.parseDOM(data, "object")
    # Resolve media url using videohosts
    videoUrl = None
    if playerholder:
        playerholder = playerholder[0]
        videoUrl = hosts.resolve(playerholder)
    if not videoUrl:
        flvdiv = common.parseDOM(data, "div", {"class": "downloadTxt"})
        if flvdiv:
            flvdiv = flvdiv[0]
            flvlink = common.parseDOM(flvdiv, "a", ret="href")
            if flvlink:
                videoUrl = []
                videoUrl.append(flvlink[0].replace(' ', '%20'))
    #videoUrl = None 
    if videoUrl:
        #print videoUrl
        Url = videoUrl[0]
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=Url))
