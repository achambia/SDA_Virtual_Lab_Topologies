#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Atul Trasi"
__email__ = "atrasi@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

""" Catalyst Center getDeviceList REST API Query Parameters """

class GetDeviceListParams:
    """
    getDeviceList API query parameters
    """
    def __init__(self) -> None:
        """
        Constructor
        :return: none
        """
        #
        # Default values set as per Catalyst Center API specification
        #
        self.hostname:list[str]
        self.managementIpAddress:list[str]
        self.macAddress:list[str]
        self.locationName:list[str]
        self.serialNumber:list[str]
        self.location:list[str]
        self.family:list[str]
        self.type:list[str]
        self.series:list[str]
        self.collectionStatus:list[str]
        self.collectionInterval:list[str]
        self.notSyncedForMinutes:list[str]
        self.errorCode:list[str]
        self.errorDescription:list[str]
        self.softwareVersion:list[str]
        self.softwareType:list[str]
        self.platformId:list[str]
        self.role:list[str]
        self.reachabilityStatus:list[str]
        self.upTime:list[str]
        self.associatedWlcIp:list[str]
        self.licenseName:list[str] = []
        self.licenseType:list[str] = []
        self.licenseStatus:list[str] = []
        self.moduleName:list[str] = []
        self.moduleEqupimentType:list[str] = []
        self.moduleServiceState:list[str] = []
        self.moduleVendorEquipmentType:list[str] = []
        self.modulePartNumber:list[str] = []
        self.moduleOperationStateCode:list[str] = []
        self.id:str
        self.deviceSupportLevelstring:str
        self.offset:int = 1
        self.limit:int = 500

        #
        # Several parameters (those starting with 'license' and 'module') 
        # have illegal characters ('.' and '+') for variable names
        # These variables need to modified in the __dict__ attribute so 
        # it can be used downstream in the getDeviceList API
        #
        self.__fixDict()

    def __fixDict(self):
        self.__dict__['license.name'] = self.__dict__['licenseName']
        del self.__dict__['licenseName']
        self.__dict__['license.type'] = self.__dict__['licenseType']
        del self.__dict__['licenseType']
        self.__dict__['license.status'] = self.__dict__['licenseStatus']
        del self.__dict__['licenseStatus']
        self.__dict__['module+name'] = self.__dict__['moduleName']
        del self.__dict__['moduleName']
        self.__dict__['module+equpimenttype'] = self.__dict__['moduleEqupimentType']
        del self.__dict__['moduleEqupimentType']
        self.__dict__['module+servicestate'] = self.__dict__['moduleServiceState']
        del self.__dict__['moduleServiceState']
        self.__dict__['module+vendorequipmenttype'] = self.__dict__['moduleVendorEquipmentType']
        del self.__dict__['moduleVendorEquipmentType']
        self.__dict__['module+partnumber'] = self.__dict__['modulePartNumber']
        del self.__dict__['modulePartNumber']
        self.__dict__['module+operationstatecode'] = self.__dict__['moduleOperationStateCode']
        del self.__dict__['moduleOperationStateCode']