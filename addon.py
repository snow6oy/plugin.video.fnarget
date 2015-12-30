import sys, logging
import urllib, urllib2, urlparse
import xbmcplugin, xbmcaddon, xbmcgui, xbmc
# XBMC Python comes with all the standard modules from Python 2.6 or later
# http://mirrors.kodi.tv/docs/python-docs/14.x-helix/
def showProgress(person):
  progress = xbmcgui.DialogProgress()
  progress.create(__addonname__, "hi "+ person)
  i=0
  while i < 11:
    percent = int( ( i / 10.0 ) * 100)
    message = "Attempting to log you in " + str(i) + " out of 10"
    progress.update(percent, "", message, "")
    print("Message "+ str(i)+ " out of 10")
    xbmc.sleep(1000)
    if progress.iscanceled():
      break
    i=i+ 1
  progress.close()

def getPersonName():
  prefilledinput=''
  kb = xbmc.Keyboard(prefilledinput, 'Please type in your name to continue')
  kb.doModal()
  if (kb.isConfirmed()):
    person = kb.getText()
  return person

def authApi(req):
  try: rsp=urllib2.urlopen(req)
  except urllib2.HTTPError as e: # connx was ok, have status code
    return e.getcode()
  except urllib2.URLError as e: # connx failed, timeout .. whatever
    return 0   # e.reason would be better but its a string and easier to always return numeric
  return rsp.getcode()  # rsp.reason

def buildXbmcUrl(query):
    return base_url + '?' + urllib.urlencode(query)

################################################################################
__addonname__='script.fnarget'
addon=xbmcaddon.Addon()
addonname=addon.getAddonInfo('name') # pretty version
base_url = sys.argv[0]
addon_handle=int(sys.argv[1]) # handle the plugin was started with
args = urlparse.parse_qs(sys.argv[2][1:]) # parse ?foo=bar ignoring the ?
xbmcplugin.setContent(addon_handle, 'files')
settings=xbmcaddon.Addon(id=__addonname__)
person=settings.getSetting('person') # TODO set and unset on login and logout
api_url='http://fnarg.local:5001/'
mode=args.get('mode', None)
# set to logging.INFO for tranquility, DEBUG for noisiness
# DEBUG can also be turned on in Kodi > System > Settings
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if mode is None:
  for foldername in ['login', 'logout', 'whoami']:
    url=buildXbmcUrl({'mode': 'folder', 'foldername': foldername})
    li=xbmcgui.ListItem(foldername, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
  xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'folder':
  foldername=args['foldername'][0]
  if foldername == 'login':
    if not person: # there is no local session
      person=getPersonName()
      logging.info('>>> about to login %s <<<' % person)
      data=urllib.urlencode({'person': person})
      data=data.encode('utf-8') # data should be bytes
      req=urllib2.Request(api_url, data)
      status_code=authApi(req)
      logging.info('>>> api status code %d <<<' % status_code)
      if status_code == 201: # got a remote session ok, now we create local session to avoid network overhead
        settings.setSetting(id='person', value=person)
    else:
      logging.warning(">>> why show the '%s' folder when there is already a session? <<<" % foldername)      
  elif foldername == 'whoami':
    api_url=api_url+ person
    logging.info('>>> verifying %s <<<' % api_url)    
    req=urllib2.Request(api_url)
    status_code=authApi(req)
    logging.info('>>> api status code %d <<<' % status_code)
  elif foldername == 'logout':
    api_url=api_url+ person
    logging.info('>>> deleting %s <<<' % api_url)
    opener=urllib2.build_opener(urllib2.HTTPHandler)
    req=urllib2.Request(api_url)
    req.get_method = lambda: 'DELETE'
    status_code=authApi(req)
    logging.info('>>> api status code %d <<<' % status_code)
    if status_code == 204: # clear down local session unless there was a remote error
      settings.setSetting(id='person', value=None)
  xbmcplugin.endOfDirectory(addon_handle)
else:
  logging.warning('>>> unexpected mode %s <<<' % mode)
################################################################################
'''
test case 0 same url with server stopped on port 5001
[WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond

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