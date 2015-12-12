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
        pass 
    
    def GetInfo(self, ip):
        """Retrieve information"""
        if self._isValidIPAddress(ip):
            try:
                req = request.urlopen('http://ip-api.com/json/{:s}'.format(ip))
                if req.code == 200:
                    encoding = req.headers.get_content_charset()
                    return IpGeoLocation(json.loads(req.read().decode(encoding)))
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