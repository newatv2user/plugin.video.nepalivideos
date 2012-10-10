'''
Created on May 23, 2012

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

BASE_URL = 'http://canadanepal.info/'
site = 'canadanepal'

pluginhandle = int(sys.argv[1])

def Main():
    print 'canadanepal main'
    data = Common.save_web_page(BASE_URL, 'canadanepal.html')
    #data = Common.load_local_page('canadanepal.html')
    Menu = [('Video Entertainment', '', 'http://canadanepal.info/images/video.gif', 'browsevident'),
            ('Nepali News and Kura Kani', '', 'http://canadanepal.info/images/banner/samachar20.jpg', 'browsenews'),
            ('Sidebar Links', '', Common.topics_thumb, 'browsesidebars')]
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

def browsesidebars():
    print 'canadanepal browsesidebars'
    data = Common.load_local_page('canadanepal.html')
    data = data.replace('\r\n', '').replace('\r', '').replace('\n', '')
    sidecolumns = common.parseDOM(data, "td", attrs={ "width": "160", "class": "magin" })
    Hrefs = []
    print 'sidecolumns: ' + str(len(sidecolumns))
    for Column in sidecolumns:
        #print 'column: ' + Column
        Links = re.compile('<a href="(.+?)" title="" target="_blank">(.+?)</a>').findall(Column)
        if Links:
            Hrefs.extend(Links)
    if Hrefs:
        MediaItems = []
        for Url, Title in Hrefs:            
            Image = common.parseDOM(Title, "img", ret="src")
            if Image:
                Image = BASE_URL + Image[0]
            else:
                Image = Common.search_thumb
            Title = common.replaceHTMLCodes(Title)
            Title = common.stripTags(Title)
            Title = Title.encode('utf-8')
            Title = Title.replace('Watch ', '').replace('More ', '').replace('+ ', '')
            Title = Title.strip()
            
            if Title == '' or 'canadanepal' not in Url or ' Radio' in Title or 'FM' in Title:
                continue
            print 'Url: ' + Url
            print 'Title: ' + Title
            Mediaitem = MediaItem()
            Mediaitem.ListItem.setInfo('video', { 'Title': Title})
            Mediaitem.ListItem.setLabel(Title)
            Mediaitem.Isfolder = True
            Mediaitem.Image = Image
            Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
            if 'category' in Url:
                Mediaitem.Mode = 'browse'
            else:
                Mediaitem.Mode = 'play'
            Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
            Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
            MediaItems.append(Mediaitem)
        Common.addDir(MediaItems)
        
def browsevident():
    print 'canadanepal browsevident'
    data = Common.load_local_page('canadanepal.html')
    data = data.replace('\r\n', '').replace('\r', '').replace('\n', '')
    column = common.parseDOM(data, "td", attrs={ "width": "949", "class": "magin" })
    if not column:
        return
    column = column[0]
    innertable = common.parseDOM(column, "table", attrs={ "style": "border-collapse: collapse",
                                                         "bgcolor": "#c6c6c6", "border": "1",
                                                         "bordercolor": "#ffffff", "cellpadding": "3",
                                                         "cellspacing": "0",
                                                         "width": "691" })
    if not innertable:
        return
    innertable = innertable[0]
    valigntop = common.parseDOM(innertable, "tr", attrs={ "valign": "top"})
    if not valigntop:
        return
    content = valigntop[0]
    tds = common.parseDOM(content, "td")
    if not tds:
        return
    tds = tds[0]
    items = common.parseDOM(tds, "font", attrs={ "color": "#.+?" })
    if not items:
        return
    MediaItems = []
    for item in items:
        href = common.parseDOM(item, "a", ret="href")
        if not href:
            continue
        href = href[0]
        Title = common.stripTags(item)
        if Title == '':
            continue
        Title = Title.replace(' Click here', '')
        Title = common.replaceHTMLCodes(Title)
        Title = Title.encode('utf-8')
        print 'Url: ' + href
        print 'Title: ' + Title
        Url = urllib.quote_plus(href)
        Mediaitem = MediaItem()
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Mode = 'play'
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
    Common.addDir(MediaItems)

def browsenews():
    print 'canadanepal browsevident'
    data = Common.load_local_page('canadanepal.html')
    data = data.replace('\r\n', '').replace('\r', '').replace('\n', '')
    column = common.parseDOM(data, "td", attrs={ "width": "949", "class": "magin" })
    if not column:
        return
    column = column[0]
    innertable = common.parseDOM(column, "table", attrs={ "style": "border-collapse: collapse",
                                                         "bgcolor": "#c6c6c6", "border": "1",
                                                         "bordercolor": "#ffffff", "cellpadding": "3",
                                                         "cellspacing": "0",
                                                         "width": "691" })
    if not innertable:
        return
    innertable = innertable[0]
    valigntop = common.parseDOM(innertable, "tr", attrs={ "valign": "top"})
    if not valigntop:
        return
    content = valigntop[0]
    tds = common.parseDOM(content, "td")
    if not tds:
        return
    tds = tds[1]
    #print 'tds: ' + tds
    MediaItems = []
    itemsl2 = re.compile('[->]+(.+?)<a href="(.+?)"').findall(tds)
    if not itemsl2:
        return
    for Title, href in itemsl2:
        if not href:
            continue
        Title = common.stripTags(Title)
        #Title = Title.replace(' Click here', ''). replace(' Click Here', '')
        Title = Title.replace('Click Here', '').replace('ClickHere', '').replace('clickhere', '')
        Title = Title.replace('Click here', '').replace('Clickhere', '')
        Title = common.replaceHTMLCodes(Title)
        Title = Title.strip()        
        Title = Title.encode('utf-8')
        if Title == '':
            continue
        #print 'Url: ' + href
        print 'Title: ' + Title
        Url = urllib.quote_plus(href)
        Mediaitem = MediaItem()
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Common.video_thumb
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Mode = 'play'
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Url + '"&name="' + Title + '"'
        MediaItems.append(Mediaitem)
        
    Common.addDir(MediaItems)
    
def browse(url=None):
    if not url:
        url = Common.args.url
    print 'canadanepal browse'
    data = Common.getURL(url)
    listviewbox = common.parseDOM(data, "div", attrs={ "class": "listviewbox"})[0]
    videolist = common.parseDOM(listviewbox, "li")
    MediaItems = []
    for video in videolist:
        Mediaitem = MediaItem()
        Title = common.parseDOM(video, "span")
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
        Url = urllib.quote_plus(Href)
        Image = common.parseDOM(video, "img", ret="src")
        if Image:
            Image = Image[0]
        else:
            Image = Common.video_thumb
        Mediaitem.Mode = 'play'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Image = Image
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
    if 'nayakhabar' in url:
        travlink = re.compile('a href="(http://www.canadanepal.+?)".+?<strong>').findall(data)
        if travlink:
            travlink = travlink[0]
            data = Common.getURL(travlink)
    post = common.parseDOM(data, "div", attrs={ "class": "post" })[0]
    Title = common.parseDOM(post, "h2", attrs={ "class": "title"})[0]
    Title = common.replaceHTMLCodes(Title)
    Title = Title.encode('utf-8')
    entry = common.parseDOM(post, "div", attrs={ "class": "entry"})[0]
    # Resolve media url using videohosts
    videoUrl = None
    videoUrl = hosts.resolve(entry)
     
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
