'''
Created on Jul 30, 2012

@author: newatv2user
'''
import Common
from Common import MediaItem
import CommonFunctions
import sys
import re
import urllib
import xbmcplugin, xbmcgui
import hosts

# For parsedom
common = CommonFunctions
common.dbg = True
common.dbglevel = 3

BASE_URL = 'http://www.songsnepal.com'
site = 'songsnepal'

pluginhandle = int(sys.argv[1])

def Main():
    print 'songsnepal Main'
    Menu = [('New Videos', BASE_URL + '/newvideos.html', Common.video_thumb, 'browse'),
            ('Top Videos', BASE_URL + '/topvideos.html', Common.video_thumb, 'browse')]
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
        
    data = Common.getURL(BASE_URL)
    data = unicode(data, 'utf-8', 'ignore')
    #print data
    ULCat = common.parseDOM(data, "ul", {"id": "ul_categories"})[0]
    #ULCat = common.parseDOM(data, "div", {"class": "categoriesdropped"})[0]
    Items = common.parseDOM(ULCat, "li")
    for Item in Items:
        Title = common.parseDOM(Item, "a")
        if not Title:
            continue
        Title = Title[0]
        
        Href = common.parseDOM(Item, "a", ret="href")
        if not Href:
            continue
        Href = Href[0]
        Mediaitem = MediaItem()
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        Mediaitem.Image = Common.video_thumb
        Mediaitem.Mode = 'browse2'
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Href + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)

def browse(url=None):
    if not url:
        url = Common.args.url
    print 'songsnepal browse'
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    data = Common.getURL(url)
    Items = common.parseDOM(data, "tr", {"class": "row\d"})
    MediaItems = []
    for Item in Items:
        Image = common.parseDOM(Item, "img", ret="src")
        if not Image:
            Image = ''
        else:
            Image = Image[0]
        
        TDS = common.parseDOM(Item, "td")
        if not "topvideos" in url:
            TDS = TDS[0]
        
            Artist = TDS.split("<td>", 1)[0]
        
            Title = common.parseDOM(TDS, "a")
            if not Title:
                continue
            Title = Title[0]
        
            Href = common.parseDOM(TDS, "a", ret="href")
            if not Href:
                continue
            Href = Href[0]
        
            Detail = TDS.rsplit(">", 1)[1]
        else:
            Artist = TDS[1]
            Title = common.parseDOM(TDS[2], "a")
            if not Title:
                continue
            Title = Title[0]
            Href = common.parseDOM(TDS[2], "a", ret="href")
            if not Href:
                continue
            Href = Href[0]
            Detail = TDS[3]
            
        Plot = "Artist: " + Artist
        Plot += "\n" + Detail
        
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
    pagination = common.parseDOM(data, "div", {"class": "pagination"})
    if pagination:
        div = pagination[0]
        Matches = re.compile('href="(.+?)">(.+?)<').findall(div)
        for Href, Title in Matches:
            if Title != "next &raquo;":
                continue            
            
            Mediaitem = MediaItem()
            Title = 'Next'
            Url = urllib.quote_plus(BASE_URL + '/' + Href)
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

def browse2(url=None):
    if not url:
        url = Common.args.url
    print 'songsnepal browse2'
    # set content type so library shows more views and info
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    data = Common.getURL(url)
    detailpage = common.parseDOM(data, "div", {"id": "detail_page"})[0]
    Items = common.parseDOM(detailpage, "li", {"class": "item column"})
    MediaItems = []
    for Item in Items:
        Href = common.parseDOM(Item, "a", ret="href")
        if not Href:
            continue
        Href = Href[0]
        
        Image = common.parseDOM(Item, "img", ret="src")
        if not Image:
            Image = ''
        else:
            Image = Image[0]
        
        Artist = common.parseDOM(Item, "em", {"class": "artist_name"})
        if not Artist:
            Artist = ''
        else:
            Artist = Artist[0]
            
        Title = common.parseDOM(Item, "em", {"class": "song_name"})
        if not Title:
            continue
        Title = Title[0]

        Mediaitem = MediaItem()
        
        Mediaitem.Mode = 'play'
        Url = urllib.quote_plus(Href)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title, 'Plot': Artist})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Image
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Href + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)

    # Next Page
    pagination = common.parseDOM(data, "div", {"class": "pagination"})
    if pagination:
        div = pagination[0]
        Matches = re.compile('href="(.+?)">(.+?)<').findall(div)
        for Href, Title in Matches:
            if Title != "next &raquo;":
                continue            
            
            Mediaitem = MediaItem()
            Title = 'Next'
            Url = urllib.quote_plus(BASE_URL + '/' + Href)
            Mediaitem.Image = Common.next_thumb
            Mediaitem.Mode = 'browse2'
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
    playerholder = common.parseDOM(data, "div", {"id": "Playerholder"})
    # Resolve media url using videohosts
    videoUrl = None
    if playerholder:
        playerholder = playerholder[0]
        videoUrl = hosts.resolve(playerholder)
     
    if videoUrl:
        #print videoUrl
        Url = videoUrl[0]
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=Url))
