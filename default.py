import sys, os
import xbmc, xbmcaddon, xbmcplugin
import CommonFunctions
import lib.Common as Common

# plugin constants
#plugin = "nepalivideos - " + version

__settings__ = xbmcaddon.Addon()
settingsDir = __settings__.getAddonInfo('profile')
settingsDir = xbmc.translatePath(settingsDir)
cacheDir = os.path.join(settingsDir, 'cache')
pluginhandle = int(sys.argv[1])

# For parsedom
common = CommonFunctions
common.dbg = False
common.dbglevel = 3

def Run():
    if sys.argv[2] == '':
        # Build Main Directory
        Common.BuildMainDirectory()
    elif Common.args.site in Common.DictValues():
        print 'found in dict values'
        exec 'import lib.%s as sitemodule' % Common.args.site
        exec 'sitemodule.%s()' % Common.args.mode
        if not Common.args.mode.startswith('play'):
            xbmcplugin.endOfDirectory(pluginhandle)
        
Run()
sys.modules.clear()
