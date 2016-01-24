import urllib, urllib2

class LaunchkeyApiClient:

  api_url=""
  # load the API that will pass credentials to the launchkey service
  def __init__(self, api_url):
    self.api_url=api_url

  def authApi(self, req):
    try: rsp=urllib2.urlopen(req)
    except urllib2.HTTPError as e: # connx was ok, have status code
      return e.getcode()
    except urllib2.URLError as e: # connx failed, timeout .. whatever
      return 0  # e.reason would be more informative
                # but its a string and we need to return an integer
    return rsp.getcode()  # rsp.reason, see above

  # prepare a POST request for the api client
  def doLogin(self, person=None):
    data=urllib.urlencode({'person': person})
    data=data.encode('utf-8') # data should be bytes
    req=urllib2.Request(self.api_url, data)
    status_code=self.authApi(req)
    return {'status_code': status_code, 'person': person}

  # prepare a GET request for the api client
  def doWhoami(self, person=""):
    req=urllib2.Request(self.api_url+ person)
    status_code=self.authApi(req)
    return status_code

  # and a DELETE request too
  def doLogout(self, person=None):
    opener=urllib2.build_opener(urllib2.HTTPHandler)
    req=urllib2.Request(self.api_url+ person)
    req.get_method=lambda: 'DELETE'
    status_code=self.authApi(req)
    return status_code