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

from datetime import datetime
import os
from termcolor import colored
from sys import platform as _platform


if _platform == 'win32':
    import colorama
    colorama.init()

def Red(value):
        return colored(value, 'red', attrs=['bold'])
    
def Green(value):
    return colored(value, 'green', attrs=['bold'])
    
          
class Logger:
    
    def __init__(self, nolog=False, verbose=False):
        self.NoLog = nolog
        self.Verbose = verbose
        
        
    def WriteLog(self, messagetype, message):
        filename = '{}.log'.format(datetime.strftime(datetime.now(), "%Y%m%d"))
        path = os.path.join('.', 'logs', filename)
        with open(path, 'a') as logFile:
            logFile.write('[{}] {} - {}\n'.format(messagetype, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"), message))
              
              
    def PrintError(self, message):
        """Print/Log error message"""
        if not self.NoLog:
            self.WriteLog('ERROR', message)
        
        print('[{}] {}'.format(Red('ERROR'), message))
    
    
    def PrintResult(self, title, value):
        """print result to terminal"""
        print('{}: {}'.format(title, Green(value)))
    
    
    def Print(self, message):
        """print/log info message"""
        if not self.NoLog:
            self.WriteLog('INFO', message)
            
        if self.Verbose:
            print('[{}] {}'.format(Green('**'), message))
    
    
    def PrintIPGeoLocation(self, ipGeoLocation):
        """print IP Geolocation information to terminal"""
        self.PrintResult('\nTarget', ipGeoLocation.Query)
        self.PrintResult('IP', ipGeoLocation.IP)
        self.PrintResult('ASN', ipGeoLocation.ASN)
        self.PrintResult('City', ipGeoLocation.City)
        self.PrintResult('Country', ipGeoLocation.Country)
        self.PrintResult('Country Code', ipGeoLocation.CountryCode)
        self.PrintResult('ISP', ipGeoLocation.ISP)
        self.PrintResult('Latitude', str(ipGeoLocation.Latitude))
        self.PrintResult('Longtitude', str(ipGeoLocation.Longtitude))
        self.PrintResult('Organization', ipGeoLocation.Organization)
        self.PrintResult('Region Code', ipGeoLocation.Region)
        self.PrintResult('Region Name', ipGeoLocation.RegionName)
        self.PrintResult('Timezone', ipGeoLocation.Timezone)
        self.PrintResult('Zip Code', ipGeoLocation.Zip)
        self.PrintResult('Google Maps', ipGeoLocation.GoogleMapsLink)
        print()
        #.encode('cp737', errors='replace').decode('cp737')
    