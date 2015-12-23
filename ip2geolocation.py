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
__version__ = '1.8'

import argparse, sys, webbrowser, os.path
from argparse import RawTextHelpFormatter
from geolocation.IpGeoLocationLib import IpGeoLocationLib
from geolocation.IpGeoLocation import IpGeoLocation
from utilities.FileExporter import FileExporter
from utilities.Logger import Logger
from urllib.parse import urlparse
from libraries.colorama import Fore, Style
from subprocess import call
from sys import platform as _platform


def checkProxyUrl(url):
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
    
    
def printInfo( message):
    if not args.nolog:
        Logger.WriteLog('INFO', message)
            
    if args.verbose:
        if _platform == 'win32':
            print('[*] {}'.format(message))
        else:
            print('[' + Fore.GREEN + '*' + Style.RESET_ALL + '] {}'.format(message))


def printError(message):
    if not args.nolog:
        Logger.WriteLog('ERROR', message)
            
    if _platform == 'win32':
        print('[ERROR] {}'.format(message))
    else:
        print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] {}'.format(message))
    

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""IPGeoLocation {} 
Retrieve IP Geolocation information from http://ip-api.com
http://ip-api.com service will automatically ban any IP addresses doing over 150 requests per minute.
    """.format(__version__), formatter_class=RawTextHelpFormatter)
    
    
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
                        default='IP2GeoLocation {}'.format(__version__), 
                        help='Set the User-Agent request header (default: IP2GeoLocation {}).'.format(__version__))
    
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
    
    parser.add_argument('--noprint', 
                        action='store_true', 
                        help='IPGeolocation will print IP Geolocation info to terminal. It is possible to tell IPGeolocation not to print results to terminal with this option.')
    
    parser.add_argument('-v', '--verbose', 
                        action='store_true', 
                        help='Enable verbose output.')
    
    parser.add_argument('--nolog', 
                        action='store_true', 
                        help='IPGeolocation will save a .log file. It is possible to tell IPGeolocation not to save those log files with this option.')
    
    
    #anonymity options
    parser.add_argument('-x', '--proxy', 
                        type=checkProxyUrl, 
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
    result = ipGeoLocRequest.GetInfo(args.target, args.uagent, args.tlist, 
                                     args.r, args.ulist, args.proxy, 
                                     args.noprint, args.verbose, args.nolog)

    IpGeoLocObj = None
    IpGeoLocObjs = None
    
    if type(result) is IpGeoLocation:
        IpGeoLocObj = result
    elif type(result) is list:
        IpGeoLocObjs = result
    else:
        printError("Retrieving IP Geolocation information failed.")
        sys.exit(5)
        
    
    if args.csv:
        fileExporter = FileExporter()
        printInfo('Saving results to {} CSV file.'.format(args.csv))
        success = False
        
        if IpGeoLocObjs:
            success = fileExporter.ExportListToCSV(IpGeoLocObjs, args.csv)
        elif IpGeoLocObj:
            success = fileExporter.ExportToCSV(IpGeoLocObj, args.csv)
        
        if not success:
            printError('Saving results to {} CSV file failed.'.format(args.csv))
    
    
    if args.xml:
        fileExporter = FileExporter()
        printInfo('Saving results to {} XML file.'.format(args.xml))
        success = False
        
        if IpGeoLocObjs:
            success = fileExporter.ExportListToXML(IpGeoLocObjs, args.xml)
        elif IpGeoLocObj:
            success = fileExporter.ExportToXML(IpGeoLocObj, args.xml)
        
        if not success:
            printError('Saving results to {} XML file failed.'.format(args.xml))
            
            
    if args.txt:
        fileExporter = FileExporter()
        printInfo('Saving results to {} text file.'.format(args.txt))
        success = False
        
        if IpGeoLocObjs:
            success = fileExporter.ExportListToTXT(IpGeoLocObjs, args.txt)
        elif IpGeoLocObj:
            success = fileExporter.ExportToTXT(IpGeoLocObj, args.txt)
            
        if not success:
            printError('Saving results to {} text file failed.'.format(args.txt))
                
    
    if args.g:
        if type(IpGeoLocObj.Longtitude) == float and type(IpGeoLocObj.Latitude) == float:
            
            printInfo('Opening Geolocation in browser..'.format(args.csv))
            
            if _platform == 'cygwin':
                call(['cygstart', IpGeoLocObj.GoogleMapsLink])
                
            elif _platform == 'win32' or _platform == 'linux' or _platform == 'linux2':
                webbrowser.open(IpGeoLocObj.GoogleMapsLink)
            
            else:
                printError('-g option is not available on your platform.')
