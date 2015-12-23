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

from time import gmtime, strftime

class Logger:
    
    @staticmethod
    def WriteLog(message):
        filename = '{}.log'.format(strftime("%Y%m%d", gmtime()))
        with open(filename, 'a') as logFile:
            logFile.write('{} - {}\n'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), message))
            