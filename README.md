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
* Retrieve Geolocation of IP or Domain.
* Pick a random User-Agent string from file. Each User Agent string in new line.
* Run program with no arguments to get your IP Geolocation.
* Open IP geolocation in Google Maps using the default browser.
* Retrieve Geolocation of multiple IPs or Domains loaded from file. Each target in new line.
* Export results to csv, xml and txt format.


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
usage: ip2geolocation.py [-h] [-t host] [-T file] [-u user-agent] [-U file]
                         [-r] [-g] [-x url] [--csv file] [--xml file]
                         [-e file]

IPGeoLocation 1.5
Retrieve IP Geolocation information from http://ip-api.com


optional arguments:
  -h, --help            show this help message and exit
  -t host, --target host
                        IP Address or Domain to be analyzed.
  -T file, --tlist file
                        A list of IPs/Domains targets, each target in new line.
  -u user-agent, --useragent user-agent
                        Set the User-Agent request header (default: IP2GeoLocation 1.5).
  -U file, --ulist file
                        A list of User-Agent strings, each string in new line.
  -r                    Pick User-Agent strings randomly from a file.
  -g                    Open IP location in Google maps with default browser.
  -x url, --proxy url   Setup proxy server (example: http://127.0.0.1:8080).
  --csv file            Export results in CSV format.
  --xml file            Export results in XML format.
  -e file, --txt file   Export results.
```
  

**Examples**
---
**Retrieve your IP Geolocation**
* ./ip2geolocation.py

**Retrieve IP Geolocation**
* ./ip2geolocation.py -t x.x.x.x

**Retrieve Domain Geolocation**
* ./ip2geolocation.py -t example.com

**Custom User Agent string** 
* ./ip2geolocation.py -t x.x.x.x -u "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"

**Using Proxy**
* ./ip2geolocation.py -t x.x.x.x -x http://127.0.0.1:8080

**Pick User Agent string randomly**
* ./ip2geolocation.py -t x.x.x.x -U /path/to/user/agent/strings/filename.txt -r 

**Retrieve IP geolocation and open location in Google maps with default browser**
* ./ip2geolocation.py -t x.x.x.x -g

**Export results to CSV file**
* ./ip2geolocation.py -t x.x.x.x --csv /path/to/results.csv

**Export results to XML file**
* ./ip2geolocation.py -t x.x.x.x --xml /path/to/results.xml

**Export results to TXT file**
* ./ip2geolocation.py -t x.x.x.x -e /path/to/results.txt

**Retrieve IP Geolocation for multiple targets**
* ./ip2geolocation.py -T /path/to/targets/targets.txt

**Retrieve IP Geolocation for multiple targets and export to xml**
* ./ip2geolocation.py -T /path/to/targets/targets.txt --xml /path/to/results.xml
