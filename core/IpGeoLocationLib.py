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

from core.Utils import *
from core.Logger import PrintIPGeoLocation
import json, random, os
from core.IpGeoLocation import IpGeoLocation
from time import sleep
from core.FileExporter import FileExporter
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
                Print('Loading Proxies from file {}..'.format(self.ProxiesFile), self.NoLog, self.Verbose)
                self.__loadProxies()
            
            #check user-agent strings file and load it
            if userAgentFile and os.path.isfile(userAgentFile) and os.access(userAgentFile, os.R_OK):
                self.UserAgentFile = userAgentFile
                Print('Loading User-Agent strings from file {}..'.format(self.UserAgentFile), self.NoLog, self.Verbose)
                self.__loadUserAgents()
            
            #check targets file and load it
            if targetsFile and os.path.isfile(targetsFile) and os.access(targetsFile, os.R_OK):
                self.TargetsFile = targetsFile
                Print('Loading targets from file {}..'.format(self.TargetsFile), self.NoLog, self.Verbose)
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
                openLocationInGoogleMaps(results, self.NoLog, self.Verbose)
                
            return True
        
        except MyExceptions.UserAgentFileEmptyError:
            PrintError("User-Agent strings file is empty!", self.NoLog)
        except MyExceptions.InvalidTargetError:
            PrintError('Please provide a valid Domain or IP address!', self.NoLog)
        except MyExceptions.TargetsFileEmptyError:
            PrintError('Targets file is empty!', self.NoLog)
        except MyExceptions.UserAgentFileNotSpecifiedError:
            PrintError('User-Agent strings file has not been provided!', self.NoLog)
        except MyExceptions.TargetsFileNotSpecifiedError:
            PrintError('Targets file has not been provided!', self.NoLog)
        except MyExceptions.ProxyServerNotReachableError:
            PrintError('Proxy server not reachable!', self.NoLog)
        except MyExceptions.ProxiesFileNotSpecifiedError:
            PrintError('Proxies file has not been provided!', self.NoLog)
        except MyExceptions.ProxiesFileEmptyError:
            PrintError('Proxies file is empty!', self.NoLog)
        except MyExceptions.InvalidProxyUrlError:
            PrintError('Proxy URL is not valid!', self.NoLog)
        except Exception as error:
            PrintError('An unexpected error occurred {}!'.format(error), self.NoLog)
        
        return False
    
    def __checkProxyUrl(self, url):
        """Check if proxy url is valid"""
        url_checked = urlparse(url)
        if ((url_checked.scheme != 'http') & (url_checked.scheme != 'https')) | (url_checked.netloc == ''):
            return False
        return url_checked
    
    
    def __configureProxy(self, proxy):
        #proxy = self.__checkProxyUrl(proxy)
        #if not proxy:
        #    raise MyExceptions.InvalidProxyUrlError()
        
        checkProxyConn(self.URL, proxy.netloc, self.NoLog, self.Verbose)
        self.Proxy = proxy
        proxyHandler = request.ProxyHandler({'http':proxy.scheme + '://' + proxy.netloc})
        opener = request.build_opener(proxyHandler)
        request.install_opener(opener)
        Print('Proxy ({}) has been configured.'.format(proxy.scheme + '://' + proxy.netloc), self.NoLog, self.Verbose)
                
                
    def __exportResultsToCSV(self, objToExport, csvFile):
        """Export results to csv file"""
        fileExporter = FileExporter()
        Print('Saving results to {} CSV file.'.format(csvFile), self.NoLog, self.Verbose)
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToCSV(objToExport, csvFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToCSV(objToExport, csvFile)
        
        if not success:
            PrintError('Saving results to {} CSV file failed.'.format(csvFile), self.NoLog)
            
    
    def __exportResultsToXML(self, objToExport, xmlFile):
        """Export results to xml file"""
        fileExporter = FileExporter()
        Print('Saving results to {} XML file.'.format(xmlFile), self.NoLog, self.Verbose)
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToXML(objToExport, xmlFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToXML(objToExport, xmlFile)
        
        if not success:
            PrintError('Saving results to {} XML file failed.'.format(xmlFile), self.NoLog)
            
            
    def __exportResultsToTXT(self, objToExport, txtFile):
        """Export results to text file"""
        fileExporter = FileExporter()
        Print('Saving results to {} text file.'.format(txtFile), self.NoLog, self.Verbose)
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToTXT(objToExport, txtFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToTXT(objToExport, txtFile)
        
        if not success:
            PrintError('Saving results to {} text file failed.'.format(txtFile), self.NoLog)
            
        
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
            
        elif isValidIPAddress(target):
            query = target
            
        else:
            ip = hostnameToIP(target)#domain?
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
            
        
        Print('Retrieving {} Geolocation..'.format(query), self.NoLog, self.Verbose)
        
        req = request.Request(self.RequestURL.format(target), data=None, headers={
          'User-Agent':self.UserAgent
        })
        
        response = request.urlopen(req)
        
        if response.code == 200:
            
            Print('User-Agent used: {}'.format(self.UserAgent), self.NoLog, self.Verbose)
            #Print('Proxy server used: {}'.format('{}://{}'.format(self.Proxy.scheme, self.Proxy.netloc)))
            
            encoding = response.headers.get_content_charset()
            ipGeoLocObj = IpGeoLocation(query, json.loads(response.read().decode(encoding)))
            
            Print('Geolocation information has been retrieved for {}({}).'.format(query, ipGeoLocObj.IP), self.NoLog, self.Verbose)
            
            if not self.NoPrint:
                PrintIPGeoLocation(ipGeoLocObj)
                
            return ipGeoLocObj

        return False
    
    
    def __loadProxies(self):
        """Load proxies from file"""
        if not self.ProxiesFile:
            raise MyExceptions.ProxiesFileNotSpecifiedError()
        
        self.Proxies = [line.strip() for line in open(self.ProxiesFile, 'r') if line.strip()]
        Print('{} Proxies loaded.'.format(len(self.Proxies)), self.NoLog, self.Verbose)
                
        if len(self.Proxies) == 0:
            raise MyExceptions.ProxiesFileEmptyError()
        
        
    def __loadUserAgents(self):
        """Load user-agent strings from file"""
        if not self.UserAgentFile:
            raise MyExceptions.UserAgentFileNotSpecifiedError()
        
        self.UserAgents = [line.strip() for line in open(self.UserAgentFile, 'r') if line.strip()]
        Print('{} User-Agent strings loaded.'.format(len(self.UserAgents)), self.NoLog, self.Verbose)

        if len(self.UserAgents) == 0:
            raise MyExceptions.UserAgentFileEmptyError()
        
        
    def __loadTargets(self):
        """Load targets from file"""
        if not self.TargetsFile:
            raise MyExceptions.TargetsFileNotSpecifiedError()
        
        self.Targets = [line.strip() for line in open(self.TargetsFile, 'r') if line.strip()]
        Print('{} Targets loaded.'.format(len(self.Targets)), self.NoLog, self.Verbose)
            
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
        
