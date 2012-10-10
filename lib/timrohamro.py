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
import xbmcplugin, xbmcgui

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

BASE_URL = 'http://timrohamro.com'
HOME_URL = '/all/video/10/'

site = 'timrohamro'

pluginhandle = int(sys.argv[1])

def Main():
    print 'timrohamro Main'
    Url = BASE_URL + HOME_URL
    browse(Url)
    
def browse(url=None):
    if not url:
        url = Common.args.url
    data = Common.getURL(url)
    items = common.parseDOM(data, "div", attrs={ "class": "ui-corner-all"})
    MediaItems = []
    for item in items:
        Mediaitem = MediaItem()
        Title = common.parseDOM(item, "b", attrs={ "class": "Title1"})[0]
        Image = common.parseDOM(item, "img", ret="src")[0]
        Href = common.parseDOM(item, "a", ret="href")[0]
        Url = urllib.quote_plus(Href)
        Artist = re.compile('Artist Name:.+?>(.+?)<').findall(item)
        if not Artist:
            Artist = ''
        else:
            Artist = Artist[0].strip()
        Album = re.compile('Album:.+?>(.+?)<').findall(item)
        if not Album:
            Album = ''
        else:
            Album = Album[0].strip()
        Plot = 'Artist: ' + Artist + '\n'
        Plot += 'Album: ' + Album
        Mediaitem.Mode = 'play'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Plot})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Image
        #print Mediaitem.Image
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    current = common.parseDOM(data, "font", attrs={ "class": "next-pre-current"})[0]
    currenti = int(current)
    nexti = currenti + 1
    Next = re.compile("<a href='(.+?)' class='next-pre' >([\d]{0,})</a>").findall(data)
    found = None
    #print 'len of next: ' + str(len(Next))
    for href, num in Common.Unique(Next):
        #print 'next: ' + str(nexti)
        #print 'num: ' + num
        if int(num) != nexti:
            continue
        Mediaitem = MediaItem()
        Title = 'Next'
        Url = urllib.quote_plus(BASE_URL + href)
        Mediaitem.Image = Common.next_thumb
        Mediaitem.Mode = 'browse'
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        MediaItems.append(Mediaitem)
        found = True
    if not found:
        Next = common.parseDOM(data, "a", attrs={ "class": "navlink" }, ret="href")[0]
        Mediaitem = MediaItem()
        Title = 'Next'
        Url = urllib.quote_plus(BASE_URL + Next)
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
    print 'timrohamro play'
    data = Common.getURL(url)
    videoUrl = re.compile("file:'(http://.+?wmv)'").findall(data)
    if not videoUrl:
        xbmcplugin.setResolvedUrl(pluginhandle, False, xbmcgui.ListItem())
        print 'Video not found.'        
    else:
        #print videoUrl
        Url = videoUrl[0].replace(' ', '%20').replace('../', '')
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=Url))
