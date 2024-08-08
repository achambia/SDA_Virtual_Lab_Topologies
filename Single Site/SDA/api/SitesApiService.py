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

""" Catalyst Center Sites REST API """

from api.ApiService import ApiService
from params.GetSiteParams import GetSiteParams
from reqs.SiteRequest import SiteRequest
from params.GetSiteDeviceAssociationparam import GetSiteDeviceAssociationparam

class SitesApiService(ApiService):
    """
    Sites API
    """
    def __init__(self, url:str, token:str) -> None:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        super().__init__(url, token)

    def getSite(self, getSiteParams:GetSiteParams=GetSiteParams()) -> dict:
        """
        Get Site API
        :param getSiteParams: Object containing all the query string parameters (optional, defaulted to new instance of SiteParams class)
        :return: All sites if no parameters are provided or specific sites based on input parameters
        """
        return self.get('/dna/intent/api/v2/site', getSiteParams)

    def createSite(self, createSiteRequest:SiteRequest) -> dict:
        """
        Create Site API
        :param createSiteRequest: Request object containing information for site creation
        :return: API response
        """
        return self.post('/dna/intent/api/v1/site', createSiteRequest)

    def getSiteCount(self, id:str=None) -> dict:
        """
        Get Site Count API (count of the specified site's sub-hierarchy including 
        the provided site)
        :param id: Site ID (optional, defaulted to None)  
        :return: Number of sites
        """
        params = {
                "id": id
                }
        return self.get('/dna/intent/api/v2/site/count', params)

    def deleteSite(self, siteId:str) -> dict:
        """
        Delete Site API
        :param siteId: Site ID
        :return: API response
        """
        return self.delete('/dna/intent/api/v1/site/' + siteId)

    def updateSite(self, siteId:str, updateSiteRequest:SiteRequest) -> dict:
        """
        Update Site API
        :param siteId: Site ID
        :param updateSiteRequest: Request object containing information to be updated
        :return: API response
        """
        return self.put('/dna/intent/api/v1/site/' + siteId, updateSiteRequest)

    def getSiteDeviceassociated(self,siteId:str,getSiteDeviceAssociationparam:GetSiteDeviceAssociationparam = GetSiteDeviceAssociationparam()) ->dict:
        """
        Get Site Device Association API
        :param siteId: Site ID of the interested site
        :param GetSiteDeviceAssociationparam: Object containing all the query string parameters (optional, defaulted to memberType of networkdevice)
        :return: All sites if no parameters are provided or specific sites based on input parameters
        """
        return self.get(f'/dna/intent/api/v1/site-member/{siteId}/member', getSiteDeviceAssociationparam)
