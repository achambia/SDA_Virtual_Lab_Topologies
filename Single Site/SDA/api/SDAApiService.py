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

""" Catalyst Center SDA REST API """

from SDA.api.ApiService import ApiService
from SDA.params.GetFabricSitesParams import GetFabricSitesParams
from SDA.reqs.FabricSitesRequest import FabricSitesRequest

class SDAApiService(ApiService):
    """
    SDA API
    """
    def __init__(self, url:str, token:str) -> None:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        super().__init__(url, token)

    def addFabricSites(self, addFabricSitesRequestList:list[FabricSitesRequest]) -> dict:
        """
        Add Fabric Site API
        :param addFabricSitesRequestList: List of 'FabricSitesRequest' objects containing information for adding fabric sites
        :return: API response
        """
        return self.post('/dna/intent/api/v1/sda/fabricSites', addFabricSitesRequestList)

    def deleteFabricSiteByName(self, siteNameHierarchy:str=None) -> dict:
        """
        Delete Fabric Site ny name API (deletes all fabric sites if no site hierarchy is provided)
        :param siteNameHierarchy: Name of the site hierarchy
        :return: API response
        """
        params = {
                "siteNameHierarchy": siteNameHierarchy
                }
        return self.delete('/dna/intent/api/v1/sda/fabricSites', params)

    def deleteFabricSiteById(self, id:str) -> dict:
        """
        Delete Fabric Site by ID API (deletes all fabric sites if no site hierarchy is provided)
        :param id: Fabric site ID
        :return: API response
        """
        return self.delete('/dna/intent/api/v1/sda/fabricSites/' + id)

    def gerFabricSites(self, getFabricSitesParams:GetFabricSitesParams=GetFabricSitesParams()) -> dict:
        """
        Get Fabric Site API (returns all fabric sites if no params are provided)
        :param getFabricSitesParams: Object containing all the query string parameters (optional, defaulted to new instance of GetFabricSitesParams class)
        :return: API response
        """
        return self.get('/dna/intent/api/v1/sda/fabricSites', getFabricSitesParams)

    def getSdaDeviceInfo(self,deviceManagementIpAddress:str) ->dict:
        """
        Get Fabric Site Device Info API (returns all fabric sites if no params are provided)
        :param deviceManagementIpAddress: Mgmt IP of the device)
        :return: API response
        """
        params = {
                "deviceManagementIpAddress": deviceManagementIpAddress
                }
        return self.get('/dna/intent/api/v1/business/sda/device',params)

    def getSdaBorderInfo(self,deviceManagementIpAddress:str) ->dict:
        """
        Get Fabric Border Device Info API (returns all fabric sites if no params are provided)
        :param deviceManagementIpAddress: Mgmt IP of the device)
        :return: API response
        """
        params = {
                "deviceManagementIpAddress": deviceManagementIpAddress
                }
        return self.get('/dna/intent/api/v1/business/sda/border-device',params)
