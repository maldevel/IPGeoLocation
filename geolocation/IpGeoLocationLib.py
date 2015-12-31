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

import json, ipaddress, socket, os.path, random, webbrowser
from urllib import request
from geolocation.IpGeoLocation import IpGeoLocation
from utilities.Logger import Logger
from time import sleep
from utilities import MyExceptions 
from libraries.colorama import Fore, Style
from utilities.FileExporter import FileExporter
from subprocess import call
from sys import platform as _platform
from urllib.parse import urlparse

class IpGeoLocationLib:
    """Retrieve IP Geolocation information from http://ip-api.com"""
    
    
    def __init__(self):
        self.URL = 'http://ip-api.com'
        self.RequestURL = self.URL + '/json/{}'
        self.BOLD = '\033[1m'
        self.Proxy = None
        self.UserAgentFile = None
        self.UserAgents = None
        self.Proxies = None
        self.TargetsFile = None
        self.ProxiesFile = None
        self.Targets = None
        self.Verbose = False
        self.NoPrint = False
        self.NoLog = False 
        
        
    def GetInfo(self, target, userAgent, targetsFile=None, 
                userAgentFile=None, proxy=False, proxiesFile=None, 
                noprint=False, verbose=False, nolog=False, exportToCSVFile=None, 
                exportToXMLFile=None, exportToTXTFile=None, 
                googleMaps=False):
        """Retrieve information"""
        
        self.UserAgent = userAgent
        self.Verbose = verbose
        self.NoPrint = noprint
        self.NoLog = nolog
        
        try:
            
            #check proxies file and load it
            if proxiesFile and os.path.isfile(proxiesFile) and os.access(proxiesFile, os.R_OK):
                self.ProxiesFile = proxiesFile
                self.__print('Loading Proxies from file {}..'.format(self.ProxiesFile))
                self.__loadProxies()
            
            #check user-agent strings file and load it
            if userAgentFile and os.path.isfile(userAgentFile) and os.access(userAgentFile, os.R_OK):
                self.UserAgentFile = userAgentFile
                self.__print('Loading User-Agent strings from file {}..'.format(self.UserAgentFile))
                self.__loadUserAgents()
            
            #check targets file and load it
            if targetsFile and os.path.isfile(targetsFile) and os.access(targetsFile, os.R_OK):
                self.TargetsFile = targetsFile
                self.__print('Loading targets from file {}..'.format(self.TargetsFile))
                self.__loadTargets()

            #check if proxy valid and configure connection
            if proxy:
                self.__configureProxy(proxy)
            
            
            #retrieve information
            results = None
            if self.TargetsFile:
                results = self.__retrieveGeolocations()
            
            else:
                results = self.__retrieveGeolocation(target)
            
            #export information
            if exportToCSVFile and not os.path.exists(exportToCSVFile) and os.access(os.path.dirname(exportToCSVFile), os.W_OK):
                self.__exportResultsToCSV(results, exportToCSVFile)
                
            if exportToXMLFile and not os.path.exists(exportToXMLFile) and os.access(os.path.dirname(exportToXMLFile), os.W_OK):
                self.__exportResultsToXML(results, exportToXMLFile)
                
            if exportToTXTFile and not os.path.exists(exportToTXTFile) and os.access(os.path.dirname(exportToTXTFile), os.W_OK):
                self.__exportResultsToTXT(results, exportToTXTFile)
            
            #open location in Google Maps with default browser
            if googleMaps and type(results) is IpGeoLocation:
                self.__openLocationInGoogleMaps(results)
                
            return True
        
        except MyExceptions.UserAgentFileEmptyError:
            self.__printError("User-Agent strings file is empty!")
        except MyExceptions.InvalidTargetError:
            self.__printError('Please provide a valid Domain or IP address!')
        except MyExceptions.TargetsFileEmptyError:
            self.__printError('Targets file is empty!')
        except MyExceptions.UserAgentFileNotSpecifiedError:
            self.__printError('User-Agent strings file has not been provided!')
        except MyExceptions.TargetsFileNotSpecifiedError:
            self.__printError('Targets file has not been provided!')
        except MyExceptions.ProxyServerNotReachableError:
            self.__printError('Proxy server not reachable!')
        except MyExceptions.ProxiesFileNotSpecifiedError:
            self.__printError('Proxies file has not been provided!')
        except MyExceptions.ProxiesFileEmptyError:
            self.__printError('Proxies file is empty!')
        except MyExceptions.InvalidProxyUrlError:
            self.__printError('Proxy URL is not valid!')
        except Exception as error:
            self.__printError('An unexpected error occurred {}!'.format(error))
        
        return False
    
    
    def __checkProxyUrl(self, url):
        """Check if proxy url is valid"""
        url_checked = urlparse(url)
        if ((url_checked.scheme != 'http') & (url_checked.scheme != 'https')) | (url_checked.netloc == ''):
            raise MyExceptions.InvalidProxyUrlError()
        return url_checked
    
    
    def __configureProxy(self, proxy):
        proxy = self.__checkProxyUrl(proxy)
        self.__checkProxyConn(proxy.netloc)
        self.Proxy = proxy
        proxyHandler = request.ProxyHandler({'http':proxy.scheme + '://' + proxy.netloc})
        opener = request.build_opener(proxyHandler)
        request.install_opener(opener)
        self.__print('Proxy ({}) has been configured.'.format(proxy.scheme + '://' + proxy.netloc))
                
                
    def __openLocationInGoogleMaps(self, ipGeolObj):
        """Open IP Geolocation in Google Maps with default browser"""
        if type(ipGeolObj.Longtitude) == float and type(ipGeolObj.Latitude) == float:
            self.__print('Opening Geolocation in browser..')
            
            if _platform == 'cygwin':
                call(['cygstart', ipGeolObj.GoogleMapsLink])
                
            elif _platform == 'win32' or _platform == 'linux' or _platform == 'linux2':
                webbrowser.open(ipGeolObj.GoogleMapsLink)
            
            else:
                self.__printError('-g option is not available on your platform.')
        
        
    def __exportResultsToCSV(self, objToExport, csvFile):
        """Export results to csv file"""
        fileExporter = FileExporter()
        self.__print('Saving results to {} CSV file.'.format(csvFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToCSV(objToExport, csvFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToCSV(objToExport, csvFile)
        
        if not success:
            self.__printError('Saving results to {} CSV file failed.'.format(csvFile))
            
    
    def __exportResultsToXML(self, objToExport, xmlFile):
        """Export results to xml file"""
        fileExporter = FileExporter()
        self.__print('Saving results to {} XML file.'.format(xmlFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToXML(objToExport, xmlFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToXML(objToExport, xmlFile)
        
        if not success:
            self.__printError('Saving results to {} XML file failed.'.format(xmlFile))
            
            
    def __exportResultsToTXT(self, objToExport, txtFile):
        """Export results to text file"""
        fileExporter = FileExporter()
        self.__print('Saving results to {} text file.'.format(txtFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToTXT(objToExport, txtFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToTXT(objToExport, txtFile)
        
        if not success:
            self.__printError('Saving results to {} text file failed.'.format(txtFile))
            
        
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
        
        
        #pick random user-agent string
        if self.UserAgentFile:
            self.__pickRandomUserAgent()
            
            
        #pick random proxy connection
        if self.ProxiesFile:
            self.__pickRandomProxy()
            
        
        self.__print('Retrieving {} Geolocation..'.format(query))
        
        req = request.Request(self.RequestURL.format(target), data=None, headers={
          'User-Agent':self.UserAgent
        })
        
        response = request.urlopen(req)
        
        if response.code == 200:
            
            self.__print('User-Agent used: {}'.format(self.UserAgent))
            #self.__print('Proxy server used: {}'.format('{}://{}'.format(self.Proxy.scheme, self.Proxy.netloc)))
            
            encoding = response.headers.get_content_charset()
            ipGeoLocObj = IpGeoLocation(query, json.loads(response.read().decode(encoding)))
            
            self.__print('Geolocation information has been retrieved for {}({}).'.format(query, ipGeoLocObj.IP))
            
            if not self.NoPrint:
                self.__printIPGeoLocation(ipGeoLocObj)
                
            return ipGeoLocObj

        return False
    
    
    def __loadProxies(self):
        """Load proxies from file"""
        if not self.ProxiesFile:
            raise MyExceptions.ProxiesFileNotSpecifiedError()
        
        self.Proxies = [line.strip() for line in open(self.ProxiesFile, 'r') if line.strip()]
        self.__print('{} Proxies loaded.'.format(len(self.Proxies)))
                
        if len(self.Proxies) == 0:
            raise MyExceptions.ProxiesFileEmptyError()
        
        
    def __loadUserAgents(self):
        """Load user-agent strings from file"""
        if not self.UserAgentFile:
            raise MyExceptions.UserAgentFileNotSpecifiedError()
        
        self.UserAgents = [line.strip() for line in open(self.UserAgentFile, 'r') if line.strip()]
        self.__print('{} User-Agent strings loaded.'.format(len(self.UserAgents)))

        if len(self.UserAgents) == 0:
            raise MyExceptions.UserAgentFileEmptyError()
        
        
    def __loadTargets(self):
        """Load targets from file"""
        if not self.TargetsFile:
            raise MyExceptions.TargetsFileNotSpecifiedError()
        
        self.Targets = [line.strip() for line in open(self.TargetsFile, 'r') if line.strip()]
        self.__print('{} Targets loaded.'.format(len(self.Targets)))
            
        if len(self.Targets) == 0:
            raise MyExceptions.TargetsFileEmptyError()


    def __pickRandomProxy(self):
        """Pick randomly a proxy from the list"""
        if not self.Proxies or len(self.Proxies) == 0:
            raise MyExceptions.ProxiesFileEmptyError()
        
        self.__configureProxy(random.choice(self.Proxies))
 
 
    def __pickRandomUserAgent(self):
        """Pick randomly a user-agent string from the list"""
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
        """print/log info message"""
        if not self.NoLog:
            Logger.WriteLog('INFO', message)
            
        if self.Verbose:
            if _platform == 'win32':
                print('[*] {}'.format(message))
            else:
                print('[' + Fore.GREEN + '*' + Style.RESET_ALL + '] {}'.format(message))

    def __printResult(self, title, value):
        """print result to terminal"""
        if _platform == 'win32':
            print('{}: {}'.format(title, value))
        else:
            print(title + ': ' + self.BOLD + Fore.GREEN + value + Style.RESET_ALL)

    def __printError(self, message):
        """print/log error message"""
        if not self.NoLog:
            Logger.WriteLog('ERROR', message)
            
        if _platform == 'win32':
            print('[ERROR] {}'.format(message))
        else:
            print('[' + Fore.RED + 'ERROR' + Style.RESET_ALL + '] {}'.format(message))
        
        
    def __printIPGeoLocation(self, ipGeoLocation):
        """print IP Geolocation information to terminal"""
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


    def __checkProxyConn(self, proxy):
        """check proxy connectivity"""
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
            
    