

##Download SocksiPy - A Python SOCKS client module. ( http://code.google.com/p/socksipy-branch/downloads/list )
##Simply copy the file "socks.py" to your Python's lib/site-packages directory, and initiate a socks socket like this.
## NOTE: you must use socks before urllib2.
import socks
import socket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
import  urllib2
import simplejson


url = 'http://openapi.ro/api/companies/13548146.json'
request = urllib2.Request(url)
request.add_header('Cache-Control','max-age=0')
response = urllib2.urlopen(request)

result = simplejson.load(response)


print result