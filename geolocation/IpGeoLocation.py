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


class IpGeoLocation:
    """Represents an IP Geolocation information object"""
    
    def __init__(self, jsonData = None):
        self.ASN = '-'
        self.City = '-'
        self.Country = '-'
        self.CountryCode = '-'
        self.ISP = '-'
        self.Latitude = 0.0
        self.Longtitude = 0.0
        self.Organization = '-'
        self.IP = '0.0.0.0'
        self.Region = '-'
        self.RegionName = '-'
        self.Status = '-'
        self.Timezone = '-'
        self.Zip = '-'
            
        if jsonData != None:
            if type(jsonData) is dict:
                if 'as' in jsonData: 
                    self.ASN = jsonData['as']
                
                if 'city' in jsonData:
                    self.City = jsonData['city']
                 
                if 'country' in jsonData:
                    self.Country = jsonData['country']
                   
                if 'countryCode' in jsonData:
                    self.CountryCode = jsonData['countryCode']
                   
                if 'isp' in jsonData:
                    self.ISP = jsonData['isp']
                   
                if 'lat' in jsonData:
                    self.Latitude = jsonData['lat']
                  
                if 'lon' in jsonData:
                    self.Longtitude = jsonData['lon']
                  
                if 'org' in jsonData:
                    self.Organization = jsonData['org']
                   
                if 'query' in jsonData:
                    self.IP = jsonData['query']
                  
                if 'region' in jsonData:
                    self.Region = jsonData['region']
                  
                if 'regionName' in jsonData:
                    self.RegionName = jsonData['regionName']
                  
                if 'status' in jsonData:
                    self.Status = jsonData['status']
                   
                if 'timezone' in jsonData:
                    self.Timezone = jsonData['timezone']
                   
                if 'zip' in jsonData:
                    self.Zip = jsonData['zip']
                