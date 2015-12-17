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
import socket
import os.path
import random
from time import sleep

class IpGeoLocationLib:
    """Retrieve IP Geolocation information from http://ip-api.com"""
    
    def __init__(self):
        self.URL = 'http://ip-api.com/json/{}'
        self.Proxy = request.ProxyHandler({})
    
    
    def GetInfo(self, target, userAgent, targetList=None, randomUserAgent=False, uAgentList=None, proxy=False):
        """Retrieve information"""
        
        self.UserAgent = userAgent            

        if randomUserAgent and uAgentList is not None:
            userAgent = self.__pickRandomUserAgent(uAgentList)
            if(userAgent):
                self.UserAgent = userAgent
            else:
                print('Unable to pick a random User Agent string from file.')
                return False
        

        if proxy:
            self.Proxy = request.ProxyHandler({'http':proxy.scheme + '://' + proxy.netloc})
            opener = request.build_opener(self.Proxy)
            request.install_opener(opener)
                          
                          
        if targetList is not None:
            return self.__retrieveGeolocations(targetList)
        else:         
            #if target is None:
            return self.__retrieveGeolocation(target)#my ip
            #else:
            #    if self.__isValidIPAddress(target):
            #        return self.__retrieveGeolocation(target)
            #    else:
            #        ip = self.__hostnameToIP(target)#domain?
            #        if ip:
            #            return self.__retrieveGeolocation(ip)
            #        print('Please provide a valid Domain or IP address.')
                    
            
        return False
        
        
    def __retrieveGeolocations (self, targetsFile):
        """Retrieve IP Geolocation for each target in the file list"""
        try:
            IpGeoLocObjs = []

            if os.path.isfile(targetsFile) and os.access(targetsFile, os.R_OK):
                targets = [line.strip() for line in open(targetsFile, 'r') if line.strip()]
                
                for target in targets:
                    IpGeoLocObjs.append(self.__retrieveGeolocation(target))
                    if len(targets)>=150:
                        sleep(.500)#1/2 sec - ip-api will automatically ban any IP address doing over 150 requests per minute
                    
            return IpGeoLocObjs
        except:
            return False
        
        
    def __retrieveGeolocation(self, target):
        """Retrieve IP Geolocation for single target"""
        try:
            
            if target is None:
                query = 'My IP'
                target=''
            elif self.__isValidIPAddress(target):
                query = target
            else:
                ip = self.__hostnameToIP(target)#domain?
                if not ip:
                    print('Please provide a valid Domain or IP address.')
                    return False
                query = target
                target = ip
            
            req = request.Request(self.URL.format(target), data=None, headers={
              'User-Agent':self.UserAgent
            })
            
            response = request.urlopen(req)
            
            if response.code == 200:
                encoding = response.headers.get_content_charset()
                return IpGeoLocation(query, json.loads(response.read().decode(encoding)))
            else:
                #print('Unable to contact service.')
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
    
    
    def __isValidIPAddress(self, ip):
        """Check if ip is a valid IPv4/IPv6 address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False
        