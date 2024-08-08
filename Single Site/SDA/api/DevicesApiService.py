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

""" Catalyst Center Devices REST API """

from SDA.api.ApiService import ApiService
from SDA.params.GetDeviceCountParams import GetDeviceCountParams
from SDA.params.GetDeviceListParams import GetDeviceListParams

class DevicesApiService(ApiService):
    """
    Devices API
    """
    def __init__(self, url:str, token:str) -> None:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        super().__init__(url, token)

    def getDeviceList(self, getDeviceListParams:GetDeviceListParams=GetDeviceListParams()) -> dict:
        """
        Get Device List API
        :param getDeviceListParams: Object containing all the query string parameters (optional, defaulted to new instance of GetDeviceListParams class)
        :return: Device list
        """
        return self.get('/dna/intent/api/v1/network-device', getDeviceListParams)

    def getDeviceById(self, id:str) -> dict:
        """
        Get Device By ID API
        :param id: Device ID
        :return: Device by ID
        """
        return self.get('/dna/intent/api/v1/network-device/' + id)

    def getDeviceCount(self, getDeviceCountParams:GetDeviceCountParams=GetDeviceCountParams()) -> dict:
        """
        Get Device Count API
        :param getDeviceCountParams: Object containing all the query string parameters (optional, defaulted to new instance of GetDeviceCountParams class)
        :return: Number of devices
        """
        return self.get('/dna/intent/api/v1/network-device/count', getDeviceCountParams)

    def deleteDeviceById(self, id:str, cleanConfig:bool=False) -> dict:
        """
        Delete Device By ID API
        :param id: Device ID
        :param cleanConfig: Clean device config (optional, defaulted to False)
        :return: API response
        """
        params = {
                "cleanConfig": cleanConfig
                }
        return self.delete('/dna/intent/api/v1/network-device/' + id, params)

    def createUserDefinedField(self, name:str, description:str) -> dict:
        """
        Create User Defined Field API
        :param name: User defined field name
        :param description: User defined field description
        :return: API response
        """
        body = {
                "name": name,
                "description": description
                }
        return self.post('/dna/intent/api/v1/network-device/user-defined-field', body)
