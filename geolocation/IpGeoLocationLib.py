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

import json, ipaddress 
from urllib import request
from geolocation.IpGeoLocation import IpGeoLocation
from urllib.parse import urlparse
import socket
import os.path
import random

class IpGeoLocationLib:
    """Retrieve IP Geolocation information using http://ip-api.com website"""
    
    def __init__(self):
        self.UserAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'
        self.URL = 'http://ip-api.com/json/{}'
        self.Proxy = request.ProxyHandler({})
    
    
    def GetInfo(self, host, userAgent=None, randomUserAgent=False, userAgentFileList=None, proxy=None):
        """Retrieve information"""
        
        if userAgent is not None:
            self.UserAgent = userAgent
            
            
        if randomUserAgent and userAgentFileList is not None:
            userAgent = self.__pickRandomUserAgent(userAgentFileList)
            if(userAgent):
                self.UserAgent = userAgent
            else:
                print('Unable to pick a random User Agent string from file.')
                return False
        
        
        if proxy is not None:
            proxyUrl = self.__isValidURL(proxy)
            if(proxyUrl):
                ip = self.__hostnameToIP(proxyUrl.hostname)
                if ip:
                    proxy = '{}://{}:{}'.format(proxyUrl.scheme, ip, proxyUrl.port)
                    self.Proxy = request.ProxyHandler({proxyUrl.scheme:proxy})
                    opener = request.build_opener(self.Proxy)
                    request.install_opener(opener)
                else:
                    print('Unable to resolve Proxy hostname to IP.')
                    return False
            else:
                print('Proxy URL is not valid.')
                return False
                          
                                 
        if host is None:
            return self.__retrieveGeolocation('')#my ip
        else:
            if self.__isValidIPAddress(host):
                return self.__retrieveGeolocation(host)
            else:
                ip = self.__hostnameToIP(host)#domain?
                if ip:
                    return self.__retrieveGeolocation(host)
                print('Please provide a valid Domain or IP address.')
            
        return False
        
        
    def __retrieveGeolocation(self, ip):
        try:
            req = request.Request(self.URL.format(ip), data=None, headers={
              'User-Agent':self.UserAgent
            })
            response = request.urlopen(req)
            if response.code == 200:
                encoding = response.headers.get_content_charset()
                return IpGeoLocation(json.loads(response.read().decode(encoding)))
            else:
                print('Unable to contact service.')
                return False
        except:
            return False
                
                
    def __pickRandomUserAgent(self, userAgentFileList):
        """Pick randomly a user agent string from a provided file"""
        try:
            if os.path.isfile(userAgentFileList) and os.access(userAgentFileList, os.R_OK):
                lines = [line.strip() for line in open(userAgentFileList, 'r') if line.strip()]
                return random.choice(lines)            
            return False
        except:
            return False
        
        
    def __hostnameToIP(self, hostname):
        """Resolve hostname to IP address"""
        try:
            return socket.gethostbyname(hostname)
        except:
            return False
        
        
    def __isValidURL(self, url):
        """Check if url is valid"""
        try:
            return urlparse(url)
        except:
            return False
    
    
    def __isValidIPAddress(self, ip):
        """Check if ip is a valid IPv4/IPv6 address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
        