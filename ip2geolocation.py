#!/usr/bin/env python3
# encoding: UTF-8

"""
    IPGeoLocation - Retrieve IP Geolocation information 
    Powered by http://ip-api.com
    Copyright (C) 2015 @maldevel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'maldevel'

import argparse, sys
from argparse import RawTextHelpFormatter
from geolocation.IpGeoLocationLib import IpGeoLocationLib
import webbrowser
from urllib.parse import urlparse

VERSION = '1.3'


def checkURL(url):
        """Check if url is valid"""
        url_checked = urlparse(url)
        if ((url_checked.scheme != 'http') & (url_checked.scheme != 'https')) | (url_checked.netloc == ''):
            raise argparse.ArgumentTypeError('Invalid %s Proxy URL (example: https://127.0.0.1:8080).' % url)
        return url_checked
    
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=""" 
IPGeoLocation {} 
A tool to retrieve IP Geolocation information.
Powered by http://ip-api.com
    """.format(VERSION), formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('-t', '--target', metavar='Host', help='The IP Address or Domain to be analyzed.')
    parser.add_argument('-u', '--useragent', metavar='User-Agent', default='IP2GeoLocation', help='Set the User-Agent request header (default: IP2GeoLocation).')
    parser.add_argument('-r', help='Pick User Agent strings randomly.', action='store_true')
    parser.add_argument('-l', metavar='User-Agent list', dest='user_agent_list', help='Set tge User-Agent file list. Each User-Agent string should be in a new line.')
    parser.add_argument('-x', '--proxy', metavar='Proxy', type=checkURL, help='Set the proxy server (example: http://127.0.0.1:8080).')
    parser.add_argument('-g', help='Open IP location in Google maps with default browser.', action='store_true')
    
    args = parser.parse_args()
    
    if(args.r and args.user_agent_list is None):
        print('You have to provide a file with User Agent strings. Each User agent string should be in a new line.')
        sys.exit(2)
    
    ipGeoLocRequest = IpGeoLocationLib()
    IpGeoLocObj = ipGeoLocRequest.GetInfo(args.target, args.useragent, args.r, args.user_agent_list, args.proxy)
        
    if IpGeoLocObj:
        if args.g:
            if type(IpGeoLocObj.Longtitude) == float and type(IpGeoLocObj.Latitude) == float:
                webbrowser.open('http://www.google.com/maps/place/{},{}/@{},{},16z'.
                            format(IpGeoLocObj.Latitude, IpGeoLocObj.Longtitude, IpGeoLocObj.Latitude, IpGeoLocObj.Longtitude))

        print("""
IPGeoLocation {} - Retrieve IP Geolocation information
Powered by http://ip-api.com

Results
        
    IP: {}
    ASN: {}
    City: {}
    Country: {}
    Country Code: {}
    ISP: {}
    Latitude: {}
    Longtitude: {}
    Organization: {}
    Region Code: {}
    Region Name: {}
    Timezone: {}
    Zip Code: {}
            """.format(VERSION,
                   IpGeoLocObj.IP,
                   IpGeoLocObj.ASN,
                   IpGeoLocObj.City, 
                   IpGeoLocObj.Country,
                   IpGeoLocObj.CountryCode,
                   IpGeoLocObj.ISP,
                   IpGeoLocObj.Latitude,
                   IpGeoLocObj.Longtitude,
                   IpGeoLocObj.Organization,
                   IpGeoLocObj.Region,
                   IpGeoLocObj.RegionName,
                   IpGeoLocObj.Timezone,
                   IpGeoLocObj.Zip)#.encode('cp737', errors='replace').decode('cp737')
               )
