How should I call the getters and setters of that xbmcplugin functions that controls settings? 

I am running the Helix version of Kodi 

Kodi (14.2 Git:20150326-7cc53a9). Platform: Windows NT x86 32-bit
Using Release Kodi x32 build

My code provides three parameters as described in the python-docs for Helix.
http://mirrors.kodi.tv/docs/python-docs/14.x-helix/xbmcplugin.html#-setSetting

but I consistently get an error and see the following in the kodi.log

-->Python callback/script returned the following error<--
Error Type: <type 'exceptions.TypeError'>
Error Contents: function takes at most 2 arguments (3 given)
Traceback (most recent call last):
  File "C:\Users\gavinj\AppData\Roaming\Kodi\addons\script.fnarget\addon.py", line 74, in <module>
    settings.setSetting(sys.argv[1], id='person', value='Dorothy')
TypeError: function takes at most 2 arguments (3 given)
-->End of Python script error report<--

Removing the first argument makes the error go away. Is this just a lucky guess?