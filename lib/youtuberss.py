'''
Created on Dec 19, 2012

@author: newatv2user
'''
import Common
from Common import MediaItem
import StorageServer
import CommonFunctions
import urllib
import sys
import hosts
import xbmcplugin, xbmcgui

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

cache = StorageServer.StorageServer(Common.Addonid, 1)

Query = 'nepali%20videos%20AND%20(hd%20OR%20720p%20OR%201080p)'
URL = 'http://gdata.youtube.com/feeds/base/videos?q=%s&start-index=%d&client=ytapi-youtube-search&alt=rss&v=1&orderby=published'
site = 'youtuberss'
pluginhandle = int(sys.argv[1])

def Main():
    print 'youtuberss Main'
    browse()
    
def browse():
    try:
        StartIndex = int(Common.args.startindex)
    except:
        StartIndex = 1
    Url = URL % (Query, StartIndex)
    Data = cache.cacheFunction(Common.getURL, Url)
    channel = common.parseDOM(Data, "channel")
    if not channel:
        return
    channel = channel[0]
    MediaItems = []
    totalResults = common.parseDOM(channel, "openSearch:totalResults")
    if totalResults:
        totalResults = int(totalResults[0])
        NextStart = StartIndex + 25
        if NextStart < totalResults:
            Mediaitem = MediaItem()    # Add a link to next page
            Title = 'Next Page'
            Mediaitem.Mode = 'browse'
            Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
            Mediaitem.Url += '"&startindex="' + str(NextStart) + '"&name="' + Title + '"'
            Mediaitem.ListItem.setLabel(Title)
            Mediaitem.Image = Common.next_thumb
            Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
            Mediaitem.Isfolder = True
            MediaItems.append(Mediaitem)
        
    items = common.parseDOM(channel, "item")
    if not items:
        return
    for item in items:
        Mediaitem = MediaItem()    # Add the items
        Title = common.parseDOM(item, "title")
        if not Title:
            continue
        Title = Title[0]
        
        Href = common.parseDOM(item, "link")
        if not Href:
            continue
        Href = Href[0]
        Mediaitem.Mode = 'play'
        Hrefz = urllib.quote_plus(Href)
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode 
        Mediaitem.Url += '"&url="' + Hrefz + '"&name="' + Title + '"'
        Mediaitem.ListItem.setProperty('IsPlayable', 'true')
        MediaItems.append(Mediaitem)

    Common.addDir(MediaItems)    
    Common.SetViewMode()
    
def play():
    Linky = Common.args.url
    videoUrl = hosts.resolve(Linky)
    if videoUrl:
        Url = videoUrl[0]
        xbmcplugin.setResolvedUrl(pluginhandle, True, xbmcgui.ListItem(path=Url))
