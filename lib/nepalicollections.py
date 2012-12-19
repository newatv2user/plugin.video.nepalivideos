'''
Created on Sep 28, 2012

@author: newatv2user
'''
import Common
from Common import MediaItem
import CommonFunctions
import sys
import urllib, re
import xbmcplugin, xbmcgui, xbmc
from xbmcgui import ListItem
from datetime import date, timedelta
import json
import hosts

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

BASE_URL = 'http://www.nepalicollections.com'
POST_URL = '/login.php'
DETAIL_URL = '/dailydetail.php?id='
site = 'nepalicollections'
pluginhandle = int(sys.argv[1])

def Main():
    print 'nepalicollections Main'
    Today = date.today()
    Yesterday = Today - timedelta(1)
    Menu = [('Today', BASE_URL + POST_URL + '&Post=' + Today.strftime("%m/%d/%Y"), Common.video_thumb, 'browse'),
            ('Yesterday', BASE_URL + POST_URL + '&Post=' + Yesterday.strftime("%m/%d/%Y"), Common.video_thumb, 'browse'),
            ('Search By Date', '', Common.search_thumb, 'searchd'),
            ('Search By Name', '', Common.search_thumb, 'searchn')]
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
        Mediaitem.Url += '"&url="' + urllib.quote_plus(Url) + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)

def browse(url=None):
    if not url:
        url = Common.args.url
    print 'nepalicollections browse'
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    splits = url.split("&Post=")
    url = splits[0]
    post = splits[1]
    postdict = {}
    if (re.match("\d\d/\d\d/\d\d\d\d", post)):
        postdict["stype"] = "date"
        postdict["searchtext"] = urllib.quote_plus(post)
    else:
        postdict["stype"] = "name"
        postdict["searchtext"] = post
    postdict["func"] = "searchdaily"
    
    data = Common.fetch(url, postdict)
    #print data
    responseJson = json.loads(data)
    items = responseJson["records"] 
    MediaItems = []
    for menuItem in items:
        Mediaitem = MediaItem()
        Title = menuItem["title"]
        ID = menuItem["dailylinkid"] 
        Href = BASE_URL + DETAIL_URL + ID
        Mediaitem.Mode = 'play'
        Url = urllib.quote_plus(Href)
        #print Url
        Date = menuItem["date"]
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Date})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)
    
    Common.addDir(MediaItems)
    Common.SetViewMode()

def searchd():
    print 'Search by date.'
    keyb = xbmc.Keyboard('', 'Search By Date. Enter in format mm/dd/yyyy')
    keyb.doModal()
    if (keyb.isConfirmed() == False):
        return
    search = keyb.getText()
    if not search or search == '':
        return
    if (not re.match("\d\d/\d\d/\d\d\d\d", search)):
        return
    
    #search = urllib.quote_plus(search)
    Url = BASE_URL + POST_URL + '&Post=' + search
    browse(Url)
    
def searchn():
    print 'Search by name.'
    keyb = xbmc.Keyboard('', 'Search By Name.')
    keyb.doModal()
    if (keyb.isConfirmed() == False):
        return
    search = keyb.getText()
    if not search or search == '':
        return
    
    search = search.replace(' ', '%20')
    Url = BASE_URL + POST_URL + '&Post=' + search
    #print Url
    browse(Url)

def play(url=None):
    if not url:
        url = Common.args.url
    data = Common.fetch(url)
    panel = common.parseDOM(data, "div", attrs={ "class": "panel" })[0]
    Title = re.compile('<h3>Daily Link : (.+?) on').findall(data)
    if Title:
        Title = Title[0]
        Title = common.replaceHTMLCodes(Title)
        Title = Title.encode('utf-8')
    else:
        Title = 'Video'
    # Resolve media url using videohosts
    videoUrl = None
    videoUrl = hosts.resolve(panel)
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
