import sys, logging
import urllib, urllib2, urlparse
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
# right http://mirrors.xbmc.org/docs/python-docs/14.x-helix/
# wrong http://mirrors.kodi.tv/docs/python-docs/14.x-helix/
# TODO
# make username and person as separate variables
# bug: local variable 'person' referenced before assignment on [x] window close
# refactor to use lib/LaunchkeyApiClient.py
# report error in docs and join kodi forum
# release as module and create video plugin as demo
# DONE
# menu should be context sensitive to logged in or not
# add notices for errors
# improve navigation to avoid empty folder
def getPersonName():
  if not person:
    prefilledinput=''
    kb = xbmc.Keyboard(prefilledinput, 'Please type in your name to continue')
    kb.doModal()
    if (kb.isConfirmed()):
      person = kb.getText()
  return person # from either settings or keyboard

def buildXbmcUrl(query):
  return base_url+ '?'+ urllib.urlencode(query)
################################################################################
class LaunchkeyApiClient:
  # TODO pass this when new instance is created
  api_url='http://fnarg.local:5001/'

  def authApi(self, req):
    try: rsp=urllib2.urlopen(req)
    except urllib2.HTTPError as e: # connx was ok, have status code
      return e.getcode()
    except urllib2.URLError as e: # connx failed, timeout .. whatever
      return 0  # e.reason would be more informative
                # but its a string and we need to return an integer
    return rsp.getcode()  # rsp.reason, see above

  # prepare a POST request for the api client
  def doLogin(self, person):
    logging.debug('>>> about to login %s <<<' % person)
    data=urllib.urlencode({'person': person})
    data=data.encode('utf-8') # data should be bytes
    req=urllib2.Request(self.api_url, data)
    status_code=self.authApi(req)
    return {'status_code': status_code, 'person': person}

  # prepare a GET request for the api client
  def doWhoami(self, person=None):
    api_url=self.api_url+ person
    logging.debug('>>> verifying %s <<<' % api_url)
    req=urllib2.Request(api_url)
    status_code=self.authApi(req)
    return status_code

  # and a DELETE request too
  def doLogout(self, person=None):
    api_url=self.api_url+ person
    logging.debug('>>> deleting %s <<<' % api_url)
    opener=urllib2.build_opener(urllib2.HTTPHandler)
    req=urllib2.Request(api_url)
    req.get_method=lambda: 'DELETE'
    status_code=self.authApi(req)
    return status_code
################################################################################
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
lac=LaunchkeyApiClient()
# set logging.INFO for tranquility, DEBUG for noisiness
# DEBUG can also be turned on in Kodi > System > Settings
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if mode is None:  
  pass # we build the default menu at the end
elif mode[0] == 'folder':
  foldername=args['foldername'][0]
  if foldername == 'login':
    if not person: # there is no local session
      person=getPersonName()
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
      status_code=lac.doWhoami(person)
      logging.debug('>>> api status code %d <<<' % status_code)
      if status_code != 200:
        xbmc.executebuiltin('XBMC.Notification('+ person+ ', "failed login")')        
      else:
        xbmc.executebuiltin('XBMC.Notification('+ person+ ', "is logged in")')
  elif foldername == 'logout':
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
  url=buildXbmcUrl({'mode': 'folder', 'foldername': foldername})
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
'''