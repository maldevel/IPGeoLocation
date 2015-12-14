# IPGeoLocation

**A tool to retrieve IP Geolocation information**

Powered by [ip-api](http://ip-api.com/docs/)


**Requirements**
---
Python 3.x


**Features**
---
* Define your own custom User Agent string.
* Proxy support.
* Get Geolocation for domain/hostname.
* Pick a random User Agent string from a list in file (Every User Agent string in new line).
* Call program with no arguments to get your ip geolocation.
* Open IP geolocation in google maps using the default browser.


**Geolocation Information**
---
* ASN
* City
* Country
* Country Code
* ISP
* Latitude
* Longtitude
* Organization
* Region Code
* Region Name
* Timezone
* Zip Code


**Usage**
---
```
$ ./ip2geolocation.py -h 
usage: ip2geolocation.py [-h] [-t Host] [-u User-Agent] [-r]
                         [-l User-Agent list] [-x Proxy] [-g]


IPGeoLocation 1.3
A tool to retrieve IP Geolocation information.
Powered by http://ip-api.com


optional arguments:
  -h, --help            show this help message and exit
  -t Host, --target Host
                        The IP Address or Domain to be analyzed.
  -u User-Agent, --useragent User-Agent
                        Set the User-Agent request header (default: IP2GeoLocation).
  -r                    Pick User Agent strings randomly.
  -l User-Agent list    Set tge User-Agent file list. Each User-Agent string should be in a new line.
  -x Proxy, --proxy Proxy
                        Set the proxy server (example: http://127.0.0.1:8080).
  -g                    Open IP location in Google maps with default browser.
```
  

**Examples**
---
**Get your IP Geolocation**
* ./ip2geolocation.py

**Get IP Geolocation**
* ./ip2geolocation.py -t x.x.x.x

**Custom User Agent string** 
* ./ip2geolocation.py -t x.x.x.x -u "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"

**Using Proxy**
* ./ip2geolocation.py -t x.x.x.x -x http://127.0.0.1:8080

**Pick User Agent string randomly**
* ./ip2geolocation.py -t x.x.x.x -l /path/to/user/agent/strings/filename.txt -r 

**Retrieve IP geolocation and open location in Google maps with default browser**
* ./ip2geolocation.py -t x.x.x.x -g
