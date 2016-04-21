#!/usr/bin/env python3
# encoding: UTF-8

"""
    This file is part of IPGeoLocation tool.
    Copyright (C) 2015-2016 @maldevel
    https://github.com/maldevel/IPGeoLocation
    
    IPGeoLocation - Retrieve IP Geolocation information 
    Powered by http://ip-api.com
    
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
    
    For more see the file 'LICENSE' for copying permission.
"""

__author__   = 'maldevel'
__twitter__  = '@maldevel'
__version__  = '2.0.4'
__year__     = '2015-2016'


from argparse import RawTextHelpFormatter
import argparse, os
from urllib.parse import urlparse
from core.Logger import Red


banner = """
{0} 

{1} Retrieve IP Geolocation information from ip-api.com
{1} Copyright (c) {2} {3} ({4})
{1} ip-api.com service will automatically ban any IP addresses doing over 150 requests per minute.

""".format(Red('IPGeolocation ' + __version__), Red('--['), __year__, __author__, __twitter__)


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
    
    
def checkProxyUrl(url):
    """Check if proxy url is valid"""
    url_checked = urlparse(url)
    if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
        raise argparse.ArgumentTypeError('Invalid {} Proxy URL (example: http://127.0.0.1:8080).'.format(url))
    return url_checked


parser = argparse.ArgumentParser(description=banner, formatter_class=RawTextHelpFormatter)
    
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

parser.add_argument('-X', '--xlist', 
                    metavar='file', 
                    type=checkFileRead, 
                    help='A list of proxies, each proxy url in new line.')


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