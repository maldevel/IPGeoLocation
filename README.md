# IPGeoLocation

**Free, Open-Source Tool to retrieve IP Geolocation information**

Powered by [ip-api](http://ip-api.com/docs/)

IPGeoLocation is coded in Python 3.


**Features**
---
* Define your own custom User Agent string
* Proxy support
* Get Geolocation for domain/hostname
* Pick a random User Agent string from a list in file (Every User Agent string in new line)
* Call program with no arguments to get your ip geolocation
* Open IP geolocation in google maps with default browser


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
Get your IP Geolocation
* python ip2geolocation.py

Get IP Geolocation
* python ip2geolocation.py -t x.x.x.x

Custom User Agent string 
* python ip2geolocation.py -t x.x.x.x -u "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"

Using Proxy
* python ip2geolocation.py -t x.x.x.x --proxy http://127.0.0.1:8080

Pick User Agent string randomly
* python ip2geolocation.py -t x.x.x.x -ru -ulist /path/to/user/agent/strings/filename.txt

Retrieve IP geolocation and open it in Google maps with default browser
* python ip2geolocation.py -t x.x.x.x -gm
