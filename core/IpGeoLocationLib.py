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

from core.Utils import Utils
import json, random, os
from core.MyExceptions import *
from core.IpGeoLocation import IpGeoLocation
from time import sleep
from core.FileExporter import FileExporter
from urllib.parse import urlparse
from urllib import request 

class IpGeoLocationLib:
    """Retrieve IP Geolocation information from http://ip-api.com"""
    
    def __init__(self, target, logger, noprint=False, nolog=False, verbose=False):    
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
        self.NoPrint = noprint
        self.Target = target
        self.Logger = logger
        self.Utils = Utils(nolog, verbose)
        
    def GetInfo(self, userAgent, targetsFile=None, 
                userAgentFile=None, proxy=False, proxiesFile=None, 
                exportToCSVFile=None, exportToXMLFile=None, 
                exportToTXTFile=None, googleMaps=False):
        """Retrieve information"""
        
        self.UserAgent = userAgent
        
        try:
            
            #check proxies file and load it
            if proxiesFile and os.path.isfile(proxiesFile) and os.access(proxiesFile, os.R_OK):
                self.ProxiesFile = proxiesFile
                self.Logger.Print('Loading Proxies from file {}..'.format(self.ProxiesFile))
                self.__loadProxies()
            
            #check user-agent strings file and load it
            if userAgentFile and os.path.isfile(userAgentFile) and os.access(userAgentFile, os.R_OK):
                self.UserAgentFile = userAgentFile
                self.Logger.Print('Loading User-Agent strings from file {}..'.format(self.UserAgentFile))
                self.__loadUserAgents()
            
            #check targets file and load it
            if targetsFile and os.path.isfile(targetsFile) and os.access(targetsFile, os.R_OK):
                self.TargetsFile = targetsFile
                self.Logger.Print('Loading targets from file {}..'.format(self.TargetsFile))
                self.__loadTargets()

            #check if proxy valid and configure connection
            if proxy:
                self.__configureProxy(proxy)
            
            
            #retrieve information
            results = None
            if self.TargetsFile:
                results = self.__retrieveGeolocations()
            
            else:
                results = self.__retrieveGeolocation(self.Target)
            
            #export information
            if exportToCSVFile and not os.path.exists(exportToCSVFile) and os.access(os.path.dirname(exportToCSVFile), os.W_OK):
                self.__exportResultsToCSV(results, exportToCSVFile)
                
            if exportToXMLFile and not os.path.exists(exportToXMLFile) and os.access(os.path.dirname(exportToXMLFile), os.W_OK):
                self.__exportResultsToXML(results, exportToXMLFile)
                
            if exportToTXTFile and not os.path.exists(exportToTXTFile) and os.access(os.path.dirname(exportToTXTFile), os.W_OK):
                self.__exportResultsToTXT(results, exportToTXTFile)
            
            #open location in Google Maps with default browser
            if googleMaps and type(results) is IpGeoLocation:
                self.Utils.openLocationInGoogleMaps(results)
                
            return True
        
        except UserAgentFileEmptyError:
            self.Logger.PrintError("User-Agent strings file is empty!")
        except InvalidTargetError:
            self.Logger.PrintError('Please provide a valid Domain or IP address!')
        except TargetsFileEmptyError:
            self.Logger.PrintError('Targets file is empty!')
        except UserAgentFileNotSpecifiedError:
            self.Logger.PrintError('User-Agent strings file has not been provided!')
        except TargetsFileNotSpecifiedError:
            self.Logger.PrintError('Targets file has not been provided!')
        except ProxyServerNotReachableError:
            self.Logger.PrintError('Proxy server not reachable!')
        except ProxiesFileNotSpecifiedError:
            self.Logger.PrintError('Proxies file has not been provided!')
        except ProxiesFileEmptyError:
            self.Logger.PrintError('Proxies file is empty!')
        except InvalidProxyUrlError:
            self.Logger.PrintError('Proxy URL is not valid!')
        except Exception as error:
            self.Logger.PrintError('An unexpected error occurred {}!'.format(error))
        
        return False
    
    def __checkProxyUrl(self, url):
        """Check if proxy url is valid"""
        url_checked = urlparse(url)
        if (url_checked.scheme not in ('http', 'https')) | (url_checked.netloc == ''):
            return False
        return url_checked
    
    
    def __configureProxy(self, proxy):
        #proxy = self.__checkProxyUrl(proxy)
        #if not proxy:
        #    raise MyExceptions.InvalidProxyUrlError()
        
        self.Utils.checkProxyConn(self.URL, proxy.netloc)
        self.Proxy = proxy
        proxyHandler = request.ProxyHandler({'http':proxy.scheme + '://' + proxy.netloc})
        opener = request.build_opener(proxyHandler)
        request.install_opener(opener)
        self.Logger.Print('Proxy ({}) has been configured.'.format(proxy.scheme + '://' + proxy.netloc))
                
                
    def __exportResultsToCSV(self, objToExport, csvFile):
        """Export results to csv file"""
        fileExporter = FileExporter()
        self.Logger.Print('Saving results to {} CSV file.'.format(csvFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToCSV(objToExport, csvFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToCSV(objToExport, csvFile)
        
        if not success:
            self.Logger.PrintError('Saving results to {} CSV file failed.'.format(csvFile))
            
    
    def __exportResultsToXML(self, objToExport, xmlFile):
        """Export results to xml file"""
        fileExporter = FileExporter()
        self.Logger.Print('Saving results to {} XML file.'.format(xmlFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToXML(objToExport, xmlFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToXML(objToExport, xmlFile)
        
        if not success:
            self.Logger.PrintError('Saving results to {} XML file failed.'.format(xmlFile))
            
            
    def __exportResultsToTXT(self, objToExport, txtFile):
        """Export results to text file"""
        fileExporter = FileExporter()
        self.Logger.Print('Saving results to {} text file.'.format(txtFile))
        success = False
        
        if type(objToExport) is IpGeoLocation:
            success = fileExporter.ExportToTXT(objToExport, txtFile)
        elif type(objToExport) is list:
            success = fileExporter.ExportListToTXT(objToExport, txtFile)
        
        if not success:
            self.Logger.PrintError('Saving results to {} text file failed.'.format(txtFile))
            
        
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
            
        elif self.Utils.isValidIPAddress(target):
            query = target
            
        else:
            ip = self.Utils.hostnameToIP(target)#domain?
            if not ip:
                raise InvalidTargetError()
            
            query = target
            target = ip
        
        
        #pick random user-agent string
        if self.UserAgentFile:
            self.__pickRandomUserAgent()
            
            
        #pick random proxy connection
        if self.ProxiesFile:
            self.__pickRandomProxy()
            
        
        self.Logger.Print('Retrieving {} Geolocation..'.format(query))
        
        req = request.Request(self.RequestURL.format(target), data=None, headers={
          'User-Agent':self.UserAgent
        })
        
        response = request.urlopen(req)
        
        if response.code == 200:
            
            self.Logger.Print('User-Agent used: {}'.format(self.UserAgent))
            
            encoding = response.headers.get_content_charset()
            ipGeoLocObj = IpGeoLocation(query, json.loads(response.read().decode(encoding)))
            
            self.Logger.Print('Geolocation information has been retrieved for {}({}).'.format(query, ipGeoLocObj.IP))
            
            if not self.NoPrint:
                self.Logger.PrintIPGeoLocation(ipGeoLocObj)
                
            return ipGeoLocObj

        return False
    
    
    def __loadProxies(self):
        """Load proxies from file"""
        if not self.ProxiesFile:
            raise ProxiesFileNotSpecifiedError()
        
        self.Proxies = [line.strip() for line in open(self.ProxiesFile, 'r') if line.strip()]
        self.Logger.Print('{} Proxies loaded.'.format(len(self.Proxies)))
                
        if len(self.Proxies) == 0:
            raise ProxiesFileEmptyError()
        
        
    def __loadUserAgents(self):
        """Load user-agent strings from file"""
        if not self.UserAgentFile:
            raise UserAgentFileNotSpecifiedError()
        
        self.UserAgents = [line.strip() for line in open(self.UserAgentFile, 'r') if line.strip()]
        self.Logger.Print('{} User-Agent strings loaded.'.format(len(self.UserAgents)))

        if len(self.UserAgents) == 0:
            raise UserAgentFileEmptyError()
        
        
    def __loadTargets(self):
        """Load targets from file"""
        if not self.TargetsFile:
            raise TargetsFileNotSpecifiedError()
        
        self.Targets = [line.strip() for line in open(self.TargetsFile, 'r') if line.strip()]
        self.Logger.Print('{} Targets loaded.'.format(len(self.Targets)))
            
        if len(self.Targets) == 0:
            raise TargetsFileEmptyError()


    def __pickRandomProxy(self):
        """Pick randomly a proxy from the list"""
        if not self.Proxies or len(self.Proxies) == 0:
            raise ProxiesFileEmptyError()
        
        self.__configureProxy(random.choice(self.Proxies))
 
 
    def __pickRandomUserAgent(self):
        """Pick randomly a user-agent string from the list"""
        if not self.UserAgents or len(self.UserAgents) == 0:
            raise UserAgentFileEmptyError()
        
        self.UserAgent = random.choice(self.UserAgents)
        
