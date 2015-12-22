import xbmc
import xbmcgui
import xbmcaddon
 
#addon       = xbmcaddon.Addon()
#addonname   = addon.getAddonInfo('name')

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
preFilledInput = ''

kb = xbmc.Keyboard(preFilledInput, 'Please type in your name to continue')
kb.doModal()
if (kb.isConfirmed()):
  person = kb.getText()

progress = xbmcgui.DialogProgress()
progress.create(__addonname__, "hi "+ person)

i = 0
while i < 11:
    percent = int( ( i / 10.0 ) * 100)
    message = "Attempting to log you in " + str(i) + " out of 10"
    progress.update( percent, "", message, "" )
    print "Message " + str(i) + " out of 10"
    xbmc.sleep( 1000 )
    if progress.iscanceled():
        break
    i = i + 1

progress.close()

#xbmc.log('charlotte '+ person, level=xbmc.LOGDEBUG)
#xbmc.executebuiltin("THE INPUTTED NAME, IS NOT VALID,()")
#xbmcgui.Dialog().ok("User name given "+ person, "x", "y", "z")

'''
import sys
import xbmcgui
import xbmcplugin

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
url = 'http://mingus.local/video/match-of-the-day-h264sm.mp4'

li = xbmcgui.ListItem('MOTD small', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
xbmcplugin.endOfDirectory(addon_handle)
'''
