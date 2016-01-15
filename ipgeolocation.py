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

__author__  = 'maldevel'


import sys
from core.IpGeoLocationLib import IpGeoLocationLib
from core.Logger import PrintError
from core.Menu import parser,args,banner
    
    
def main():

    # no args provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
      
    #single target or multiple targets 
    if(args.target and args.tlist):
        PrintError("You can request Geolocation information either for a single target(-t) or a list of targets(-T). Not both!", args.nolog)
        sys.exit(2)
        
    #my ip address or single target
    if(args.target and args.myip):
        PrintError("You can request Geolocation information either for a single target(-t) or your own IP address. Not both!", args.nolog)
        sys.exit(3)
        
    #multiple targets or my ip address
    if(args.tlist and args.myip):
        PrintError("You can request Geolocation information either for a list of targets(-T) or your own IP address. Not both!", args.nolog)
        sys.exit(4)
    
    #single target and google maps only allowed
    if(args.tlist and args.g):
        PrintError("Google maps location is working only with single targets.", args.nolog)
        sys.exit(5)
    
    #specify user-agent or random
    if(args.uagent and args.ulist):
        PrintError("You can either specify a user-agent string or let IPGeolocation pick random user-agent strings for you from a file.", args.nolog)
        sys.exit(6)
        
    #specify proxy or random
    if(args.proxy and args.xlist):
        PrintError("You can either specify a proxy or let IPGeolocation pick random proxy connections for you from a file.", args.nolog)
        sys.exit(7)
        
        
    #init lib
    ipGeoLocRequest = IpGeoLocationLib()
    
    print(banner)
    
    #retrieve information
    if not ipGeoLocRequest.GetInfo(args.target, args.uagent, args.tlist, 
                                     args.ulist, args.proxy, args.xlist, 
                                     args.noprint, args.verbose, args.nolog, 
                                     args.csv, args.xml, args.txt, args.g):
        PrintError("Retrieving IP Geolocation information failed.")
        sys.exit(8)


if __name__ == '__main__':
    main()
    