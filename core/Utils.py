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

__author__ = 'maldevel'

import webbrowser, ipaddress, socket
from sys import platform as _platform
from subprocess import call
from urllib import request
from core import MyExceptions 
from core.Logger import Logger

class Utils:
    
    def __init__(self, nolog=False, verbose=False):    
        self.Logger = Logger(nolog, verbose)
        
        
    def openLocationInGoogleMaps(self, ipGeolObj):
        """Open IP Geolocation in Google Maps with default browser"""
        if type(ipGeolObj.Longitude) == float and type(ipGeolObj.Latitude) == float:
            self.Logger.Print('Opening Geolocation in browser..')
            
            if _platform == 'cygwin':
                call(['cygstart', ipGeolObj.GoogleMapsLink])
                
            elif _platform == 'win32' or _platform == 'linux' or _platform == 'linux2':
                webbrowser.open(ipGeolObj.GoogleMapsLink)
            
            else:
                self.Logger.PrintError('-g option is not available on your platform.')
                
                
    def hostnameToIP(self, hostname):
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(hostname)
        except:
            return False
    
    
    def isValidIPAddress(self, ip):
        """Check if ip is a valid IPv4/IPv6 address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
    
            
    def checkProxyConn(self, url, proxy):
        """check proxy connectivity"""
        check = True
        self.Logger.Print('Testing proxy {} connectivity..'.format(proxy))
    
        try:
            req = request.Request(url)
            req.set_proxy(proxy, 'http')
            request.urlopen(req)
        except:
            check = False
        
        if check == True:
            self.Logger.Print('Proxy server is reachable.')
        else:
            raise MyExceptions.ProxyServerNotReachableError()
            
            