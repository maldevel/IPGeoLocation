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

import argparse, sys
from argparse import RawTextHelpFormatter
from geolocation.IpGeoLocationLib import IpGeoLocationLib

VERSION = '1.0'

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description=""" 
    IPGeoLocation {} - Retrieve IP Geolocation information
                Powered by http://ip-api.com
    """.format(VERSION), formatter_class=RawTextHelpFormatter)
    
    parser.add_argument('-t', '--target', metavar='IP', type=str, dest='ip', default=None, help='IP Address')
    parser.add_argument('-u', '--useragent', metavar='UserAgent', type=str, dest='useragent', default=None, help='User Agent')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    
    ipGeoLocRequest = IpGeoLocationLib()
    IpGeoLocObj = ipGeoLocRequest.GetInfo(args.ip, args.useragent)
        
    if IpGeoLocObj:
        print("""
        IPGeoLocation {} - Retrieve IP Geolocation information
                Powered by http://ip-api.com
                
            Results
            
            IP: {}
            ASN: {}
            City: {}
            Country: {}
            Country Code: {}
            ISP: {}
            Latitude: {}
            Longtitude: {}
            Organization: {}
            Region Code: {}
            Region Name: {}
            Timezone: {}
            Zip Code: {}
        """.format(VERSION,
                   IpGeoLocObj.IP,
                   IpGeoLocObj.ASN,
                   IpGeoLocObj.City, 
                   IpGeoLocObj.Country,
                   IpGeoLocObj.CountryCode,
                   IpGeoLocObj.ISP,
                   IpGeoLocObj.Latitude,
                   IpGeoLocObj.Longtitude,
                   IpGeoLocObj.Organization,
                   IpGeoLocObj.Region,
                   IpGeoLocObj.RegionName,
                   IpGeoLocObj.Timezone,
                   IpGeoLocObj.Zip)
               )
        