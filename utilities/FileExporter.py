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

import csv
from xml.etree import ElementTree as etree
from collections import OrderedDict

class FileExporter:
    
    def __init__(self):
        pass
    
    
    def ExportToCSV(self, ipGeoLocObj, filename):
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Results', 'IPGeolocation'])
                writer.writerow(['IP', ipGeoLocObj.IP])
                writer.writerow(['ASN', ipGeoLocObj.ASN])
                writer.writerow(['City', ipGeoLocObj.City])
                writer.writerow(['Country', ipGeoLocObj.Country])
                writer.writerow(['Country Code', ipGeoLocObj.CountryCode])
                writer.writerow(['ISP', ipGeoLocObj.ISP])
                writer.writerow(['Latitude', ipGeoLocObj.Latitude])
                writer.writerow(['Longtitude', ipGeoLocObj.Longtitude])
                writer.writerow(['Organization', ipGeoLocObj.Organization])
                writer.writerow(['Region', ipGeoLocObj.Region])
                writer.writerow(['Region Name', ipGeoLocObj.RegionName])
                writer.writerow(['Timezone', ipGeoLocObj.Timezone])
                writer.writerow(['Zip', ipGeoLocObj.Zip])
                return True
        except:
            return False
    
    
    def ExportToXML(self, ipGeoLocObj, filename):
        try:
            data = {'IP':ipGeoLocObj.IP, 'ASN':ipGeoLocObj.ASN, 'City':ipGeoLocObj.City, 'Country':ipGeoLocObj.Country, 
                'Country Code':ipGeoLocObj.CountryCode, 'ISP':ipGeoLocObj.ISP, 'Latitude':str(ipGeoLocObj.Latitude),
                'Longtitude':str(ipGeoLocObj.Longtitude), 'Organization':ipGeoLocObj.Organization, 
                'Region':ipGeoLocObj.Region, 'Region Name':ipGeoLocObj.RegionName, 'Timezone':ipGeoLocObj.Timezone, 
                'Zip':ipGeoLocObj.Zip
                }
            orderedData = OrderedDict(sorted(data.items()))
            
            root = etree.Element('Results')
            self.__add_items(etree.SubElement(root, 'IPGeolocation'),
              ((key.replace(' ', ''), value) for key, value in orderedData.items()))
            tree = etree.ElementTree(root)
            tree.write(filename, xml_declaration=True, encoding='utf-8')
            return True
        except:
            return False

    
    def ExportToTXT(self, ipGeoLocObj, filename):
        try:
            with open(filename, 'w') as txtfile:
                txtfile.write('Results IPGeolocation\n')
                txtfile.write('IP: {}\n'.format(ipGeoLocObj.IP))
                txtfile.write('ASN: {}\n'.format(ipGeoLocObj.ASN))
                txtfile.write('City: {}\n'.format(ipGeoLocObj.City))
                txtfile.write('Country: {}\n'.format(ipGeoLocObj.Country))
                txtfile.write('Country Code: {}\n'.format(ipGeoLocObj.CountryCode))
                txtfile.write('ISP: {}\n'.format(ipGeoLocObj.ISP))
                txtfile.write('Latitude: {}\n'.format(ipGeoLocObj.Latitude))
                txtfile.write('Longtitude: {}\n'.format(ipGeoLocObj.Longtitude))
                txtfile.write('Organization: {}\n'.format(ipGeoLocObj.Organization))
                txtfile.write('Region: {}\n'.format(ipGeoLocObj.Region))
                txtfile.write('Region Name: {}\n'.format(ipGeoLocObj.RegionName))
                txtfile.write('Timezone: {}\n'.format(ipGeoLocObj.Timezone))
                txtfile.write('Zip: {}\n'.format(ipGeoLocObj.Zip))
                return True
        except:
            return False
    
    
    def __add_items(self, root, items):
        for name, text in items:
            elem = etree.SubElement(root, name)
            elem.text = text

