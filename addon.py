import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import urllib.request
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
	addon=xbmcaddon.Addon()
	addonname=addon.getAddonInfo('name')
	prefilledinput=''
	kb = xbmc.Keyboard(prefilledinput, 'Please type in your name to continue')
	kb.doModal()
	if (kb.isConfirmed()):
	  person = kb.getText()
	return person

def response(req):
	try: rsp=urllib.request.urlopen(req)
	except urllib.error.HTTPError as e: # connx was ok, have status code
		return e.getcode()
	except urllib.error.URLError as e: # connx failed, timeout .. whatever
		return e.reason
	return rsp.status  # rsp.reason

person=None
url='http://fnarg.local:5001/'+ person

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
#url = 'http://mingus.local/video/match-of-the-day-h264sm.mp4'
li = xbmcgui.ListItem('MOTD small', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
xbmcplugin.endOfDirectory(addon_handle)

if person:
  showProgress(person)
else:
	pass
	req=urllib.request.Request(url)
	print(response(req))

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