"""
    IPGeoLocation - Retrieve IP Geolocation information (http://ip-api.com)
    Copyright (C) 2015  maldevel

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

class IpGeoLocationLib:
    """Retrieve IP Geolocation information using http://ip-api.com website"""
    
    def __init__(self):
        self.UserAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'
        self.URL = 'http://ip-api.com/json/{}'
        pass 
    
    def GetInfo(self, ip, userAgent=None):
        """Retrieve information"""
        
        if self._isValidIPAddress(ip):
            
            try:
                if userAgent != None:
                    self.UserAgent = userAgent
                
                req = request.Request(self.URL.format(ip), data=None, headers={
                  'User-Agent':self.UserAgent
                })
                
                response = request.urlopen(req)
                
                if response.code == 200:
                    encoding = response.headers.get_content_charset()
                    return IpGeoLocation(json.loads(response.read().decode(encoding)))
                
            except:
                pass
            
        return False
        
        
    def _isValidIPAddress(self, ip):
        """Check if ip is a valid IPv4/IPv6 address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except:
            return False