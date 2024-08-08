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

""" Catalyst Center Network Settings REST API """

from api.ApiService import ApiService
from reqs.GlobalPoolRequest import GlobalPoolRequest
from reqs.NetworkSettingsRequest import NetworkSettingsRequest
from reqs.ReserveIPPoolRequest import ReserveIpPoolReq
from params.GetReserveIPPool import GetReserveIPPool

class NetworkSettingsApiService(ApiService):
    """
    Network Settings API
    """
    def __init__(self, url:str, token:str) -> None:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        super().__init__(url, token)

    def getNetwork(self, siteId:str) -> dict:
        """
        Get Network API
        :param siteId: Site ID
        :return: Network settings for provided Site ID
        """
        params = {
                "siteId": siteId
                }
        return self.get('/dna/intent/api/v2/network', params)

    def createNetwork(self, siteId:str, createNetworkSettingsRequest:NetworkSettingsRequest) -> dict:
        """
        Create Network API
        :param siteId: Site ID
        :param createNetworkSettingsRequest: Request object containing information for network creation
        :return: API response
        """
        return self.post('/dna/intent/api/v2/network/' + siteId, createNetworkSettingsRequest)

    def updateNetwork(self, siteId:str, updateNetworkSettingsRequest:NetworkSettingsRequest) -> dict:
        """
        Update Network API
        :param siteId: Site ID
        :param updateNetworkSettingsRequest: Request object containing information to be updated
        :return: API response
        """
        return self.put('/dna/intent/api/v2/network/' + siteId, updateNetworkSettingsRequest)

    def createGlobalPool(self, createGlobalPoolRequest:GlobalPoolRequest) -> dict:
        """
        Create Global IP Address Pool API
        :param createGlobalPoolRequest: Request object containing information for global IP pool creation
        :return: API response
        """
        return self.post('/dna/intent/api/v1/global-pool', createGlobalPoolRequest)

    def getGlobalPool(self, offset:int=None, limit:int=None) -> dict:
        """
        Get Global IP Address Pool API
        :param offset: Offset/starting row
        :param limit: Number of Global Pools to be retrieved
        :return: Global IP Pool
        """
        params = {
                "offset": offset,
                "limit": limit
                }
        return self.get('/dna/intent/api/v1/global-pool', params)

    def deleteGlobalPool(self, id:str) -> dict:
        """
        Delete Global IP Address Pool API
        :param id: IP Pool ID
        :return: API response
        """
        return self.delete('/dna/intent/api/v1/global-pool/' + id)

    def reserveIPPool(self, id:str, reserveIpv4PoolReq:ReserveIpPoolReq) -> dict:
        '''
        Reserve IP Pool API
        :param id:IP Pool ID
        :param ReserveIpv4PoolReq: Request object containing information for Reserving an IP Pool
        :return: API response
        '''

        return self.post('/dna/intent/api/v1/reserve-ip-subpool/' + id, reserveIpv4PoolReq)

    def getReserveIPPool(self , getReserveIpPool:GetReserveIPPool) -> dict:
        """
        Get Reserve IP Address Pool API
        :param getReserveIpPool: Filter for Reserve IP Pool to be retrieved
        :return: ID of Reserve IP Pool
        """
        return self.get('/dna/intent/api/v1/reserve-ip-subpool', getReserveIpPool)

    def deleteReserveIPPool(self , id:str) -> dict:
        """
        Delete Reserve IP Address Pool API
        :param id: ID of Reserve IP Pool to be deleted
        :return: Global IP Pool
        """
        return self.delete(f'/dna/intent/api/v1/reserve-ip-subpool/{id}')
