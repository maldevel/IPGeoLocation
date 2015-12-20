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

import json, ipaddress, socket, os.path, random, platform
from urllib import request
from geolocation.IpGeoLocation import IpGeoLocation
from time import sleep
from utilities import MyExceptions 
from libraries.colorama import Fore, Style

class IpGeoLocationLib:
    """Retrieve IP Geolocation information from http://ip-api.com"""
    
    def __init__(self):
        self.URL = 'http://ip-api.com'
        self.RequestURL = self.URL + '/json/{}'
        self.BOLD = '\033[1m'
        self.Proxy = request.ProxyHandler({})
        self.RandomUA = False
        self.UserAgentFile = None
        self.UserAgents = None
        self.TargetsFile = None
        self.Targets = None
        self.Verbose = False
        self.NoPrint = False
        
    def GetInfo(self, target, userAgent, targetsFile=None, rUserAgent=False, userAgentFile=None, proxy=False, noprint=False, verbose=False):
        """Retrieve information"""
        
        self.UserAgent = userAgent
        self.RandomUA = rUserAgent
        self.Verbose = verbose
        self.NoPrint = noprint
        
        try:
            
            if userAgentFile and os.path.isfile(userAgentFile) and os.access(userAgentFile, os.R_OK):
                self.UserAgentFile = userAgentFile
                self.__print('Loading User-Agent strings from file..')
                self.__loadUserAgents()
            
            if targetsFile and os.path.isfile(targetsFile) and os.access(targetsFile, os.R_OK):
                self.TargetsFile = targetsFile
                self.__print('Loading targets from file..')
                self.__loadTargets()

            if proxy:
                self.__checkProxy(proxy.netloc)
                self.Proxy = request.ProxyHandler({'http':proxy.scheme + '://' + proxy.netloc})
                opener = request.build_opener(self.Proxy)
                request.install_opener(opener)
                self.__print('Proxy ({}) has been configured.'.format(proxy.scheme + '://' + proxy.netloc))
            
            
            if self.TargetsFile:
                return self.__retrieveGeolocations()
            
            else:
                return self.__retrieveGeolocation(target)
                
            
        except MyExceptions.UserAgentFileEmptyError:
            self.__printError("User-Agent strings file is empty!")
        except MyExceptions.InvalidTargetError:
            self.__printError('Please provide a valid Domain or IP address.')
        except MyExceptions.TargetsFileEmptyError:
            self.__printError('Targets file is empty!.')
        except MyExceptions.UserAgentFileNotSpecifiedError:
            self.__printError('User-Agent strings file has not been provided!.')
        except MyExceptions.TargetsFileNotSpecifiedError:
            self.__printError('Targets file has not been provided!.')
        except MyExceptions.ProxyServerNotReachableError:
            self.__printError('Proxy server not reachable')
        except:
            self.__printError("An unexpected error occurred")
        
        return False
        
        
    def __retrieveGeolocations (self):
        """Retrieve IP Geolocation for each target in the list"""
        IpGeoLocObjs = []
                    
        for target in self.Targets:
            IpGeoLocObjs.append(self.__retrieveGeolocation(target))
            if len(self.Targets)>=150:
                sleep(.500) #1/2 sec - ip-api will automatically ban any IP address doing over 150 requests per minute
                
        return IpGeoLocObjs
        
        
    def __retrieveGeolocation(self, target):
        """Retrieve IP Geolocation for single target"""
        
        if not target:
            query = 'My IP'
            target=''
            
        elif self.__isValidIPAddress(target):
            query = target
            
        else:
            ip = self.__hostnameToIP(target)#domain?
            if not ip:
                raise MyExceptions.InvalidTargetError()
            
            query = target
            target = ip
        
        
        if self.RandomUA and self.UserAgentFile:
            self.__pickRandomUserAgent()
        
        
        self.__print('Retrieving {} Geolocation..'.format(target))
        
        req = request.Request(self.RequestURL.format(target), data=None, headers={
          'User-Agent':self.UserAgent
        })
        
        response = request.urlopen(req)
        
        if response.code == 200:
            self.__print('User-Agent used: {}'.format(self.UserAgent))
            encoding = response.headers.get_content_charset()
            self.__print('Geolocation information has been retrieved')
                
            ipGeoLocObj = IpGeoLocation(query, json.loads(response.read().decode(encoding)))
        
            if not self.NoPrint:
                self.__printIPGeoLocation(ipGeoLocObj)
                
            return ipGeoLocObj

        return False
    
    
    def __loadUserAgents(self):
        """Load user-agent strings from file"""
        if not self.UserAgentFile:
            raise MyExceptions.UserAgentFileNotSpecifiedError()
        
        self.UserAgents = [line.strip() for line in open(self.UserAgentFile, 'r') if line.strip()]
        self.__print('User-Agent strings loaded.')
                
        if len(self.UserAgents) == 0:
            raise MyExceptions.UserAgentFileEmptyError()
        
        
    def __loadTargets(self):
        """Load targets from file"""
        if not self.TargetsFile:
            raise MyExceptions.TargetsFileNotSpecifiedError()
        
        self.Targets = [line.strip() for line in open(self.TargetsFile, 'r') if line.strip()]
        self.__print('Targets loaded.')
            
        if len(self.Targets) == 0:
            raise MyExceptions.TargetsFileEmptyError()

 
    def __pickRandomUserAgent(self):
        """Pick randomly a user-agent string from list"""
        if not self.UserAgents or len(self.UserAgents) == 0:
            raise MyExceptions.UserAgentFileEmptyError()
        
        self.UserAgent = random.choice(self.UserAgents)
        
        
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
        
    
    def __print(self, message):
        if self.Verbose:
            if platform.system() == 'Windows':
                print('[*] {}'.format(message))
            else:
                print('[' + Fore.GREEN + '*' + Style.RESET_ALL + '] {}'.format(message))

    def __printResult(self, title, value):
            if platform.system() == 'Windows':
                print('{}: {}'.format(title, value))
            else:
                print(title + ': ' + self.BOLD + Fore.GREEN + value + Style.RESET_ALL)

    def __printError(self, message):
        if platform.system() == 'Windows':
            print('[ERROR] {}'.format(message))
        else:
            print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] {}'.format(message))
        
        
    def __printIPGeoLocation(self, ipGeoLocation):
        self.__printResult('\nTarget', ipGeoLocation.Query)
        self.__printResult('IP', ipGeoLocation.IP)
        self.__printResult('ASN', ipGeoLocation.ASN)
        self.__printResult('City', ipGeoLocation.City)
        self.__printResult('Country', ipGeoLocation.Country)
        self.__printResult('Country Code', ipGeoLocation.CountryCode)
        self.__printResult('ISP', ipGeoLocation.ISP)
        self.__printResult('Latitude', str(ipGeoLocation.Latitude))
        self.__printResult('Longtitude', str(ipGeoLocation.Longtitude))
        self.__printResult('Organization', ipGeoLocation.Organization)
        self.__printResult('Region Code', ipGeoLocation.Region)
        self.__printResult('Region Name', ipGeoLocation.RegionName)
        self.__printResult('Timezone', ipGeoLocation.Timezone)
        self.__printResult('Zip Code', ipGeoLocation.Zip)
        self.__printResult('Google Maps', ipGeoLocation.GoogleMapsLink)
        print()
        #.encode('cp737', errors='replace').decode('cp737')


    def __checkProxy(self, proxy):
        check = True
        self.__print('Testing proxy {} connectivity..'.format(proxy))

        try:
            req = request.Request(self.URL)
            req.set_proxy(proxy, 'http')
            request.urlopen(req)
        except:
            check = False
        
        if check == True:
            self.__print('Proxy server is reachable.')
        else:
            raise MyExceptions.ProxyServerNotReachableError()
            
    