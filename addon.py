# https://github.com/snow6oy/plugin.video.fnarget
import sys, logging
import urllib, urlparse
import xbmcplugin, xbmcaddon, xbmcgui, xbmc

from launchkeyapiclient import LaunchkeyApiClient

def getPersonName():
  prefilledinput=''
  kb = xbmc.Keyboard(prefilledinput, 'Please type in your name to continue')
  kb.doModal()
  if (kb.isConfirmed()):
    person = kb.getText()
    return person
  else:
    return None
################################################################################
api_url='http://fnarg.local:5001/'
lac=LaunchkeyApiClient(api_url)  # pass the URL whenever new instance is created
# set logging.INFO for tranquility, DEBUG for noisiness
# DEBUG can also be turned on in Kodi > System > Settings
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

__addonname__='plugin.video.fnarget'
addon=xbmcaddon.Addon()
addonname=addon.getAddonInfo('name') # pretty version
base_url=sys.argv[0]
handle=int(sys.argv[1]) # handle the plugin was started with
args=urlparse.parse_qs(sys.argv[2][1:]) # parse ?foo=bar ignoring the ?
xbmcplugin.setContent(handle, 'video')
settings=xbmcaddon.Addon(id=__addonname__)
person=settings.getSetting('person')
mode=args.get('mode', None)

if mode is None:  
  pass # we build the default menu at the end
elif mode[0] == 'folder':
  foldername=args['foldername'][0]
  if foldername == 'login':
    if not person: # there is no local session from either settings or keyboard
      person=getPersonName()
      logging.debug('>>> about to login %s <<<' % person)
      login=lac.doLogin(person)
      logging.debug('>>> api status code %d <<<' % login['status_code'])
      if login['status_code'] == 201:# if we got a remote session then 
                                     # create local session to avoid network hit
        settings.setSetting(id='person', value=login['person']) # write local fs
        person=login['person'] # global assignment
      else:
        xbmc.executebuiltin('XBMC.Notification("Login failed", "please retry")')
        person=None # forget what was entered
    else:
      pass # why show the login option when there is already a session?
  elif foldername == 'whoami':
    if not person:
      xbmc.executebuiltin('XBMC.Notification("Nobody", "is logged in")')
    else:
      logging.debug('>>> verifying %s <<<' % api_url)
      status_code=lac.doWhoami(person)
      logging.debug('>>> api status code %d <<<' % status_code)
      if status_code != 200:
        xbmc.executebuiltin('XBMC.Notification('+ person+ ', "failed login")')        
      else:
        xbmc.executebuiltin('XBMC.Notification('+ person+ ', "is logged in")')
  elif foldername == 'logout':
    logging.debug('>>> deleting %s <<<' % api_url)    
    status_code=lac.doLogout(person)
    logging.debug('>>> api status code %d <<<' % status_code)
    xbmc.executebuiltin('XBMC.Notification('+ person+ ', "has logged out")')
    settings.setSetting(id='person', value=None)
    person=None # remove from menu
  else:
    logging.debug('>>> unknown foldername %s <<<' % foldername)
else:logging.debug('>>> unexpected mode %s <<<' % mode)

logging.debug('>>> building menu with person %s <<<' % person)
logging.debug('>>> building menu with handle %d <<<' % handle)  
for foldername in ['login', 'logout', 'whoami']:
  if foldername == 'logout' and not person or foldername == 'login' and person:
    continue
  #url=buildXbmcUrl({'mode': 'folder', 'foldername': foldername})
  url=base_url+ '?'+ urllib.urlencode(
    {'mode': 'folder', 'foldername': foldername}
  )
  li=xbmcgui.ListItem(foldername, iconImage='DefaultFolder.png')
  xbmcplugin.addDirectoryItem(
    handle=handle, url=url, listitem=li, isFolder=True
  )
xbmcplugin.endOfDirectory(handle)
################################################################################
'''
test case 0 same url with server stopped on port 5001
[WinError 10060] A connection attempt failed because the connected party did not 
properly respond after a period of time, or established connection failed 
because connected host has failed to respond

GET
test case 1 and 2 both return 404 when person is '' or graham
test case 3 returns 200 when person is camilla
> req=urllib.request.Request(url)

POST
test case 4 returns 401 when person is graham
test case 5 returns 201 when person is camilla
test case 6 returns 400 when person is ''

data=urllib.parse.urlencode({'person': person})
data=data.encode('utf-8') # data should be bytes
> req=urllib.request.Request(url, data)
status=response(req)

DELETE
test case 7 returns 204 when person is camilla
test case 8 returns 404 when person is graham
test case 9 returns 400 when person is ''
> req=urllib.request.Request(url, method='DELETE')

docs 
http://mirrors.xbmc.org/docs/python-docs/14.x-helix/

ignore these old docs 
http://mirrors.kodi.tv/docs/python-docs/14.x-helix/

# TODO
 make username and person as separate variables
 refactor to use lib/LaunchkeyApiClient.py
 report error in docs and join kodi forum
 release as module and create video plugin as demo
# DONE
 bug: local variable 'person' referenced before assignment on [x] window close
 menu should be context sensitive to logged in or not
 add notices for errors
 improve navigation to avoid empty folder

'''