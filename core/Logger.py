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

from datetime import datetime
import os
from termcolor import colored
from sys import platform as _platform

if _platform == 'win32':
    import colorama
    colorama.init()
            
            
def WriteLog(messagetype, message):
    filename = '{}.log'.format(datetime.strftime(datetime.now(), "%Y%m%d"))
    path = os.path.join('.', 'logs', filename)
    with open(path, 'a') as logFile:
        logFile.write('[{}] {} - {}\n'.format(messagetype, datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"), message))
          
          
def PrintError(message, nolog=False):
    """Print/Log error message"""
    if not nolog:
        WriteLog('ERROR', message)
    
    print('[{}] {}'.format(colored('ERROR', 'red', attrs=['bold']), message))


def PrintResult(title, value):
    """print result to terminal"""
    print('{}: {}'.format(title, colored(value, 'green', attrs=['bold'])))


def Print(message, nolog=False, verbose=False):
    """print/log info message"""
    if not nolog:
        WriteLog('INFO', message)
        
    if verbose:
        print('[{}] {}'.format(colored('**', 'green', attrs=['bold']), message))


def PrintIPGeoLocation(ipGeoLocation):
    """print IP Geolocation information to terminal"""
    PrintResult('\nTarget', ipGeoLocation.Query)
    PrintResult('IP', ipGeoLocation.IP)
    PrintResult('ASN', ipGeoLocation.ASN)
    PrintResult('City', ipGeoLocation.City)
    PrintResult('Country', ipGeoLocation.Country)
    PrintResult('Country Code', ipGeoLocation.CountryCode)
    PrintResult('ISP', ipGeoLocation.ISP)
    PrintResult('Latitude', str(ipGeoLocation.Latitude))
    PrintResult('Longtitude', str(ipGeoLocation.Longtitude))
    PrintResult('Organization', ipGeoLocation.Organization)
    PrintResult('Region Code', ipGeoLocation.Region)
    PrintResult('Region Name', ipGeoLocation.RegionName)
    PrintResult('Timezone', ipGeoLocation.Timezone)
    PrintResult('Zip Code', ipGeoLocation.Zip)
    PrintResult('Google Maps', ipGeoLocation.GoogleMapsLink)
    print()
    #.encode('cp737', errors='replace').decode('cp737')
    