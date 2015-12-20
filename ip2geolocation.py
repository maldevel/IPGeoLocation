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
from libraries.colorama import Fore, Style

VERSION = '1.7'


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
    
    
def printInfo( message, newLine=False):
    if args.verbose:
        if newLine:
            print('{}\n'.format(message))
        else:
            print('{}'.format(message))
        
        
def printError( message):
    print('Error: {}\n'.format(message))
    
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="""IPGeoLocation {} 
Retrieve IP Geolocation information from http://ip-api.com
    """.format(VERSION), formatter_class=RawTextHelpFormatter)
    
    
    #pick target/s
    parser.add_argument('-m', '--my-ip',  
                        dest='myip',
                        action='store_true', 
                        help='Get Geolocation info for my IP address.')
    
    parser.add_argument('-t', '--target',  
                        help='IP Address or Domain to be analyzed.')
    
    parser.add_argument('-T', '--tlist', 
                        metavar='file',
                        type=checkFileRead, 
                        help='A list of IPs/Domains targets, each target in new line.')
    
    
    #user-agent configuration
    parser.add_argument('-u', '--user-agent', 
                        metavar='User-Agent', 
                        dest='uagent',
                        default='IP2GeoLocation {}'.format(VERSION), 
                        help='Set the User-Agent request header (default: IP2GeoLocation {}).'.format(VERSION))
    
    parser.add_argument('-r', 
                        action='store_true',
                        help='Pick User-Agent strings randomly from a file.')
    
    parser.add_argument('-U', '--ulist', 
                        metavar='file', 
                        type=checkFileRead, 
                        help='A list of User-Agent strings, each string in new line.')
    
    
    #misc options
    parser.add_argument('-g', 
                        action='store_true', 
                        help='Open IP location in Google maps with default browser.')
    
    parser.add_argument('--no-print', 
                        action='store_true', 
                        help='Do not print results to terminal.')
    
    parser.add_argument('-v', '--verbose', 
                        action='store_true', 
                        help='Enable verbose printing.')
    
    
    #anonymity options
    parser.add_argument('-x', '--proxy', 
                        type=checkProxy, 
                        help='Setup proxy server (example: http://127.0.0.1:8080)')
    
    
    #export options
    parser.add_argument('-e', '--txt', 
                        metavar='file', 
                        type=checkFileWrite, 
                        help='Export results.')
    
    parser.add_argument('-ec', '--csv', 
                        metavar='file', 
                        type=checkFileWrite, 
                        help='Export results in CSV format.')
    
    parser.add_argument('-ex', '--xml', 
                        metavar='file', 
                        type=checkFileWrite, 
                        help='Export results in XML format.')
    
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
      
    if(args.target and args.tlist):
        printError("You can request Geolocation information either for a single target(-t) or a list of targets(-T). Not both!")
        sys.exit(1)
        
    if(args.target and args.myip):
        printError("You can request Geolocation information either for a single target(-t) or your own IP address. Not both!")
        sys.exit(1)
        
    if(args.tlist and args.myip):
        printError("You can request Geolocation information either for a list of targets(-T) or your own IP address. Not both!")
        sys.exit(1)
    
    if(args.tlist and args.g):
        printError("Google maps location is working only with single targets.")
        sys.exit(2)
        
        
    if(args.r and not args.ulist):
        printError("You haven't provided a User-Agent strings file, each string in a new line.")
        sys.exit(3)
    
    ipGeoLocRequest = IpGeoLocationLib()
    result = ipGeoLocRequest.GetInfo(args.target, args.uagent, args.tlist, args.r, args.ulist, args.proxy, args.no_print, args.verbose)

    IpGeoLocObj = None
    IpGeoLocObjs = None
    
    if type(result) is IpGeoLocation:
        IpGeoLocObj = result
    elif type(result) is list:
        IpGeoLocObjs = result
    else:
        printError("Retrieving IP Geolocation information failed.")
        sys.exit(5)
        
    
    if IpGeoLocObjs is not None:
        if args.csv:
            fileExporter = FileExporter()
            if args.verbose:
                printInfo('Saving results to {} csv file.'.format(args.csv))
            if not fileExporter.ExportListToCSV(IpGeoLocObjs, args.csv):
                printError('Saving results to {} csv file failed.'.format(args.csv))
            
        if args.xml:
            fileExporter = FileExporter()
            printInfo('Saving results to {} xml file.'.format(args.xml))
            if not fileExporter.ExportListToXML(IpGeoLocObjs, args.xml):
                printError('Saving results to {} xml file failed.'.format(args.xml))
            
        if args.txt:
            fileExporter = FileExporter()
            printInfo('Saving results to {} txt file.'.format(args.txt))
            if not fileExporter.ExportListToTXT(IpGeoLocObjs, args.txt):
                printError('Saving results to {} txt file failed.'.format(args.txt))
        
                
    elif IpGeoLocObj is not None:
        if args.g:
            if type(IpGeoLocObj.Longtitude) == float and type(IpGeoLocObj.Latitude) == float:
                printInfo('Opening Geolocation in browser..'.format(args.csv))
                webbrowser.open(IpGeoLocObj.GoogleMapsLink)

        if args.csv:
            fileExporter = FileExporter()
            printInfo('Saving results to {} csv file.'.format(args.csv))
            if not fileExporter.ExportToCSV(IpGeoLocObj, args.csv):
                printError('Saving results to {} csv file failed.'.format(args.csv))
            
        if args.xml:
            fileExporter = FileExporter()
            printInfo('Saving results to {} xml file.'.format(args.xml))
            if not fileExporter.ExportToXML(IpGeoLocObj, args.xml):
                printError('Saving results to {} xml file failed.'.format(args.xml))
            
        if args.txt:
            fileExporter = FileExporter()
            printInfo('Saving results to {} txt file.'.format(args.txt))
            if not fileExporter.ExportToTXT(IpGeoLocObj, args.txt):
                printError('Saving results to {} txt file failed.'.format(args.txt))
            
