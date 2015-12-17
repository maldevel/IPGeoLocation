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
from geolocation.IpGeoLocation import IpGeoLocation
from utilities.FileExporter import FileExporter
import webbrowser
from urllib.parse import urlparse
import os.path


VERSION = '1.5'


def checkProxy(url):
        """Check if proxy url is valid"""
        url_checked = urlparse(url)
        if ((url_checked.scheme != 'http') & (url_checked.scheme != 'https')) | (url_checked.netloc == ''):
            raise argparse.ArgumentTypeError('Invalid {} Proxy URL (example: https://127.0.0.1:8080).'.format(url))
        return url_checked
    
    
def checkFileRead(filename):
    """Check if file exists and we have access to read it"""
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        return filename
    else:
        raise argparse.ArgumentTypeError("Invalid {} file (File does not exist, insufficient permissions or it's not a file).".format(filename))
    
    
def checkFileWrite(filename):
    """Check if we can write to file"""
    if os.path.isfile(filename):
        raise argparse.ArgumentTypeError("File {} already exists.".format(filename))
    elif os.path.isdir(filename):
        raise argparse.ArgumentTypeError("Folder provided. Please provide a file.")
    elif os.access(os.path.dirname(filename), os.W_OK):
        return filename
    else:
        raise argparse.ArgumentTypeError("Unable to write to {} file (Insufficient permissions).".format(filename))


def printIPGeoLocation(ipGeoLocation):
    print("""
    Target: {}
    
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
    Google Maps: {}
            """.format(ipGeoLocation.Query,
                   ipGeoLocation.IP,
                   ipGeoLocation.ASN,
                   ipGeoLocation.City, 
                   ipGeoLocation.Country,
                   ipGeoLocation.CountryCode,
                   ipGeoLocation.ISP,
                   ipGeoLocation.Latitude,
                   ipGeoLocation.Longtitude,
                   ipGeoLocation.Organization,
                   ipGeoLocation.Region,
                   ipGeoLocation.RegionName,
                   ipGeoLocation.Timezone,
                   ipGeoLocation.Zip,
                   ipGeoLocation.GoogleMapsLink
               )#.encode('cp737', errors='replace').decode('cp737')
       )
    
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="""IPGeoLocation {} 
Retrieve IP Geolocation information from http://ip-api.com
    """.format(VERSION), formatter_class=RawTextHelpFormatter)
    
    #target
    parser.add_argument('-t', '--target', metavar='host', help='IP Address or Domain to be analyzed.')
    parser.add_argument('-T', '--tlist', metavar='file', type=checkFileRead, help='A list of IPs/Domains targets, each target in new line.')
    
    #user-agent
    parser.add_argument('-u', '--useragent', metavar='user-agent', default='IP2GeoLocation {}'.format(VERSION), help='Set the User-Agent request header (default: IP2GeoLocation {}).'.format(VERSION))
    parser.add_argument('-U', '--ulist', metavar='file', type=checkFileRead, help='A list of User-Agent strings, each string in new line.')
    
    #misc
    parser.add_argument('-r', help='Pick User-Agent strings randomly from a file.', action='store_true')
    parser.add_argument('-g', help='Open IP location in Google maps with default browser.', action='store_true')
    
    #anon
    parser.add_argument('-x', '--proxy', metavar='url', type=checkProxy, help='Setup proxy server (example: http://127.0.0.1:8080).')
    
    #export
    parser.add_argument('--csv', metavar='file', type=checkFileWrite, help='Export results in CSV format.')
    parser.add_argument('--xml', metavar='file', type=checkFileWrite, help='Export results in XML format.')
    parser.add_argument('-e', '--txt', metavar='file', type=checkFileWrite, help='Export results.')
    
    args = parser.parse_args()
    
    
    if(args.target is not None and args.tlist is not None):
        print("You can provide either a single target(-t) or a list of targets(-T). Not both!")
        sys.exit(2)
        
    
    if(args.tlist is not None and args.g):
        print("Google maps location is working only with single targets.")
        sys.exit(3)
        
        
    if(args.r and args.ulist is None):
        print("You didn't provide a file with User-Agent strings, each string in a new line.")
        sys.exit(4)
    
    
    ipGeoLocRequest = IpGeoLocationLib()
    result = ipGeoLocRequest.GetInfo(args.target, args.useragent, args.tlist, args.r, args.ulist, args.proxy)


    IpGeoLocObj = None
    IpGeoLocObjs = None
    
    if type(result) is IpGeoLocation:
        IpGeoLocObj = result
    elif type(result) is list:
        IpGeoLocObjs = result
    
    
    if IpGeoLocObjs is not None:
        if args.csv:
            fileExporter = FileExporter()
            if not fileExporter.ExportListToCSV(IpGeoLocObjs, args.csv):
                print('Saving results to {} csv file failed.'.format(args.csv))
            
        if args.xml:
            fileExporter = FileExporter()
            if not fileExporter.ExportListToXML(IpGeoLocObjs, args.xml):
                print('Saving results to {} xml file failed.'.format(args.xml))
            
        if args.txt:
            fileExporter = FileExporter()
            if not fileExporter.ExportListToTXT(IpGeoLocObjs, args.txt):
                print('Saving results to {} txt file failed.'.format(args.txt))
        
        print('IPGeoLocation {} - Results'.format(VERSION))
        for obj in IpGeoLocObjs:
            if obj:
                printIPGeoLocation(obj)
        
        
    elif IpGeoLocObj is not None:
        if args.g:
            if type(IpGeoLocObj.Longtitude) == float and type(IpGeoLocObj.Latitude) == float:
                webbrowser.open(IpGeoLocObj.GoogleMapsLink)

        if args.csv:
            fileExporter = FileExporter()
            if not fileExporter.ExportToCSV(IpGeoLocObj, args.csv):
                print('Saving results to {} csv file failed.'.format(args.csv))
            
        if args.xml:
            fileExporter = FileExporter()
            if not fileExporter.ExportToXML(IpGeoLocObj, args.xml):
                print('Saving results to {} xml file failed.'.format(args.xml))
            
        if args.txt:
            fileExporter = FileExporter()
            if not fileExporter.ExportToTXT(IpGeoLocObj, args.txt):
                print('Saving results to {} txt file failed.'.format(args.txt))
            
        print('IPGeoLocation {} - Results'.format(VERSION))
        printIPGeoLocation(IpGeoLocObj)
    
