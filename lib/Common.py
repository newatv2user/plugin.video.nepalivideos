'''
Created on May 15, 2012

@author: newatv2user
'''
import sys, os
import urllib, urllib2, cookielib
import xbmc, xbmcplugin, xbmcaddon
from xbmcgui import ListItem
import CommonFunctions

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

__settings__ = xbmcaddon.Addon(id='plugin.video.nepalivideos')
settingsDir = __settings__.getAddonInfo('profile')
settingsDir = xbmc.translatePath(settingsDir)
cacheDir = os.path.join(settingsDir, 'cache')
pluginhandle = int(sys.argv[1])

"""
    PARSE ARGV
"""
class _Info:
    def __init__(self, *args, **kwargs):
        print "common.args"
        print kwargs
        self.__dict__.update(kwargs)

exec "args = _Info(%s)" % (urllib.unquote_plus(sys.argv[2][1:].replace("&", ", ").replace('"', '\'')),)

if not os.path.exists(settingsDir):
    os.mkdir(settingsDir)
if not os.path.exists(cacheDir):
    os.mkdir(cacheDir)

programs_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'programs.png')
topics_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'topics.png')
search_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'search.png')
next_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'next.png')
movies_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'movies.jpg')
tv_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'television.jpg')
shows_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'shows.png')
video_thumb = os.path.join(__settings__.getAddonInfo('path'), 'resources', 'media', 'movies.png')

class MediaItem:
    ##################
    ## Class for items
    ##################
    def __init__(self):
        self.ListItem = ListItem()
        self.Image = ''
        self.Url = ''
        self.Isfolder = False
        self.Mode = ''

def addDir(Listitems):
    if Listitems is None:
        return
    Items = []
    for Listitem in Listitems:
        #print Listitem.Image
        Item = Listitem.Url, Listitem.ListItem, Listitem.Isfolder
        Items.append(Item)
    handle = pluginhandle
    xbmcplugin.addDirectoryItems(handle, Items)

def getURL(url):
    ## Get URL
    print 'getURL :: url = ' + url
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    usock = opener.open(url)
    response = usock.read()
    usock.close()
    return response

def fetch(url, postdata=None):
    print 'fetch: ' + url
    # postdata is a dict for the data to POST
    result = None
    if postdata:
        result = common.fetchPage({"link": url, "post_data": postdata})
    else:
        result = common.fetchPage({"link": url})
    if result["status"] == 200:
        return result["content"]
    else:
        return None

def save_web_page(url, filename):
    # Save page locally
    f = open(os.path.join(cacheDir, filename), 'w')
    data = getURL(url)
    f.write(data)
    f.close()
    return data

def load_local_page(filename):
    # Read from locally save page
    f = open(os.path.join(cacheDir, filename), 'r')
    data = f.read()
    f.close()
    return data

def Unique(seq, idfun=None):
    ''' Return a unique list
        Source: http://www.peterbe.com/plog/uniqifiers-benchmark
    '''
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def SetViewMode():
    # Set View Mode selected in the setting
    try:
        # if (xbmc.getSkinDir() == "skin.confluence"):
        if __settings__.getSetting('view_mode') == "1": # List
            xbmc.executebuiltin('Container.SetViewMode(502)')
        if __settings__.getSetting('view_mode') == "2": # Big List
            xbmc.executebuiltin('Container.SetViewMode(51)')
        if __settings__.getSetting('view_mode') == "3": # Thumbnails
            xbmc.executebuiltin('Container.SetViewMode(500)')
        if __settings__.getSetting('view_mode') == "4": # Poster Wrap
            xbmc.executebuiltin('Container.SetViewMode(501)')
        if __settings__.getSetting('view_mode') == "5": # Fanart
            xbmc.executebuiltin('Container.SetViewMode(508)')
        if __settings__.getSetting('view_mode') == "6":  # Media info
            xbmc.executebuiltin('Container.SetViewMode(504)')
        if __settings__.getSetting('view_mode') == "7": # Media info 2
            xbmc.executebuiltin('Container.SetViewMode(503)')
            
        if __settings__.getSetting('view_mode') == "0": # Media info for Quartz?
            xbmc.executebuiltin('Container.SetViewMode(52)')
    except:
        print "SetViewMode Failed: " + __settings__.getSetting('view_mode')
        print "Skin: " + xbmc.getSkinDir()
    
"""
    DEFINE
"""
'''site_dict = { 'NPVideo.com': 'npvideo',
              'TimroHamro.com': 'timrohamro' }'''

site_dict = { 'npvideo': ('NPVideo.com', shows_thumb),
              'timrohamro': ('TimroHamro.com', 'http://timrohamro.com/images/timrohamro.png'),
              'nepalisongs': ('NepaliSongs.tv', 'http://nepalisongs.tv/templates/zenics/images/nepalisongs.png'),
              'canadanepal': ('CanadaNepal.info', 'http://canadanepal.info/LOGO.PNG?4d90a879c4c17170cc959d2fff61062b'),
              'enternepal': ('EnterNepal.net', 'http://www.enternepal.net/wp-content/themes/enternepal/images/en_logo.png'),
              'songsnepal': ('SongsNepal.com', 'http://www.songsnepal.com/templates/ozenyx/images/logo.png'),
              'nepalicollections': ('NepaliCollections.com', 'http://nepalicollections.com/function/images/newmain1_01.png')
            }
    
'''def BuildMainDirectory():
    MediaItems = []
    for name, site in site_dict.iteritems():
        Mediaitem = MediaItem()
        Title = name        
        Mediaitem.Mode = 'Main'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        Mediaitem.Image = search_thumb
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode + '"&name="' + urllib.quote_plus(Title) + '"'
        MediaItems.append(Mediaitem)
    addDir(MediaItems)
    xbmcplugin.endOfDirectory(pluginhandle)'''
    
def BuildMainDirectory():
    MediaItems = []
    for site, sitedetail in site_dict.iteritems():
        Mediaitem = MediaItem()
        Title = sitedetail[0]        
        Mediaitem.Mode = 'Main'
        Mediaitem.ListItem.setInfo('video', { 'Title': Title})
        Mediaitem.ListItem.setLabel(Title)
        Mediaitem.Isfolder = True
        Mediaitem.Image = sitedetail[1]
        Mediaitem.ListItem.setThumbnailImage(Mediaitem.Image)
        Mediaitem.Url = sys.argv[0] + '?site="' + site + '"&mode="' + Mediaitem.Mode + '"&name="' + urllib.quote_plus(Title) + '"'
        MediaItems.append(Mediaitem)
    addDir(MediaItems)
    xbmcplugin.endOfDirectory(pluginhandle)
    
def DictValues():
    Values = []
    for site, _ in site_dict.iteritems():
        Values.append(site)
    return Values
