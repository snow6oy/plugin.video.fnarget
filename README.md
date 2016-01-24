# plugin.video.fnarget

Fnarget exists to demonstrate the awesomeness of password-less login

## Install

Download the addon as a zipfile http://fnarg.net/plugin.video.fnarget.zip

Then from within Kodi navigate to _Install from zip file_

## Configure

By default authentication requests will be sent to the following URL
```
  api_url='http://fnarg.local:5001/'
```
If you have your own API running you may want to change this URL (see addon.py) or create a local hostsfile entry to wherever your service is running.

But if you don't have your own API service, then you can set one up by following the instructions at
https://github.com/snow6oy/fnarget-api