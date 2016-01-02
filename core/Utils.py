#!/usr/bin/env python3
# encoding: UTF-8

"""
    IPGeoLocation - Retrieve IP Geolocation information 
    Powered by http://ip-api.com
    Copyright (C) 2015-2016 @maldevel

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

import webbrowser, ipaddress, socket
from core.Logger import *
from sys import platform as _platform
from subprocess import call
from urllib import request
from core import MyExceptions 
    

def openLocationInGoogleMaps(ipGeolObj, nolog=False, verbose=False):
    """Open IP Geolocation in Google Maps with default browser"""
    if type(ipGeolObj.Longtitude) == float and type(ipGeolObj.Latitude) == float:
        Print('Opening Geolocation in browser..', nolog, verbose)
        
        if _platform == 'cygwin':
            call(['cygstart', ipGeolObj.GoogleMapsLink])
            
        elif _platform == 'win32' or _platform == 'linux' or _platform == 'linux2':
            webbrowser.open(ipGeolObj.GoogleMapsLink)
        
        else:
            PrintError('-g option is not available on your platform.', nolog)
            
            
def hostnameToIP(hostname):
    """Resolve hostname to IP address"""
    try:
        return socket.gethostbyname(hostname)
    except:
        return False


def isValidIPAddress(ip):
    """Check if ip is a valid IPv4/IPv6 address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

        
def checkProxyConn(url, proxy, nolog=False, verbose=False):
    """check proxy connectivity"""
    check = True
    Print('Testing proxy {} connectivity..'.format(proxy), nolog, verbose)

    try:
        req = request.Request(url)
        req.set_proxy(proxy, 'http')
        request.urlopen(req)
    except:
        check = False
    
    if check == True:
        Print('Proxy server is reachable.', nolog, verbose)
    else:
        raise MyExceptions.ProxyServerNotReachableError()
            
            