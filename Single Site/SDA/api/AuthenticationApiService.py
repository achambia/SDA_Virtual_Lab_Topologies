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

""" Catalyst Center Authentication REST API """

import logging
import requests
from requests.auth import HTTPBasicAuth

class AuthenticationApiService:
    """
    Authentication API
    """
    def __init__(self, user:str, password:str, url:str) -> None:
        """
        Constructor
        :param user: Catalyst Center API user
        :param password: Catalyst Center API password
        :param url: Catalyst Center Authentication URL
        :return: none
        """
        #
        # Save logger with current file name
        #
        self.logger = logging.getLogger(self.__class__.__name__)
        #
        # Initialize members
        #
        self.url:str = url
        self.user:str = user
        self.password:str = password


    def authenticate(self) -> str:
        """
        Authenticate user
        :return: authorization token to be used in all API calls
        """
        url = self.url + '/api/system/v1/auth/token'
        header = {'content-type': 'application/json'}

        try:
            response = requests.post(url, auth=HTTPBasicAuth(self.user, self.password), headers=header, verify=False)

            #
            # Check if request is unsuccessful
            #
            if response.status_code != 200:
                #
                # Log error and return error response
                #
                self.logger.error(response.text.strip())
                return ""

            #
            # return access token
            #
            return response.json()['Token']
        
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return ""
