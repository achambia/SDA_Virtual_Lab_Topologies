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

""" Base class for Catalyst Center REST API """

import inspect
import json
import logging
import requests

class ApiService:
    """
    Base class for API
    """
    def __init__(self, url:str, token:str) -> None:
        """
        Constructor
        :param url: Catalyst Center URL
        :param token: Authentication token
        :return: none
        """
        #
        # Save logger with current file name
        #
        self.logger = logging.getLogger(self.__class__.__name__)
        #
        # Make sure base class cannot be instantiated
        #
        if type(self) == ApiService:
            self.logger.error(f"Only children of {self.__class__.__name__} may be instantiated.")
        #
        # Initialize members
        #
        self.url:str = url
        self.token:str = token
        self.headers:dict = {'content-type': 'application/json', 
                            '__runsync': str(True),
                            '__timeout': str(30),
                            '__persistbapioutput': str(True),
                            'x-auth-token': self.token}
        
    def __http(self, method:str, uri:str, params:dict={}, body:dict={}) -> dict:
        """
        Private method used in all public HTTP methods
        :param uri: URI for the API call
        :return: Response dictionary
        """
        url = self.url + uri
        self.logger.debug('API URL = ' + url)

        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, verify=False)
            
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, data=json.dumps(body), verify=False)
            
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, params=params, verify=False)
            
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, data=json.dumps(body), verify=False)

            #
            # Check if request is successful
            #
            if response.status_code == 200:
                #
                # Log INFO & DEBUG messages
                #
                self.logger.info(f"{inspect.stack()[2].function}() executed successfully")
                self.logger.debug(response.text.strip())

            elif response.status_code == 202:
                #
                # Log INFO & DEBUG messages
                #
                self.logger.info(f"{inspect.stack()[2].function}() queued successfully")
                self.logger.debug(response.text.strip())

            else:
                #
                # Log ERROR and return error response
                #
                self.logger.error(response.json())
                return json.loads(response.text.strip())
            
            #
            # Log message
            #
            self.logger.debug('Response = ' + json.dumps(response.json()))

            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return {}
        
    def __toDict(self, classObject) -> dict:
        """
        Private method to convert any class object to JSON
        :param classObject: Class object to be converted
        :return: Converted JSON
        """
        return self.__trim(json.loads((json.dumps(classObject, default=lambda o: o.__dict__))))
    
    
    def __trim(self, value:list|dict) -> list|dict:
        """
        Private method to remove empty dict and list objects
        :param value: list or dict to be trimmed
        :return: Trimmed list or dict
        """
        if isinstance(value, dict):
            value = {
                k: v
                for k, v in ((k, self.__trim(v)) for k, v in value.items())
                if v not in ("", None, {}, [])
            }
            
        elif isinstance(value, list):
            value = [v for v in (self.__trim(v) for v in value) if v not in ("", None, {}, [])]

        return value
        
    def get(self, uri:str, params:dict={}) -> dict:
        """
        HTTP GET
        :param uri: URI for the API call
        :return: Response dictionary
        """
        toDict = self.__toDict(params)

        self.logger.info(f"Entering {inspect.stack()[0].function}() from {inspect.stack()[1].function}()")
        self.logger.debug('Params = ' + json.dumps(toDict))

        return self.__http('GET', uri, params=toDict)

    def post(self, uri:str, body:dict={}) -> dict:
        """
        HTTP POST
        :param uri: URI for the API call
        :param body: POST payload
        :return: Response dictionary
        """
        toDict = self.__toDict(body)

        self.logger.info(f"Entering {inspect.stack()[0].function}() from {inspect.stack()[1].function}()")
        self.logger.debug('Request = ' + json.dumps(toDict))

        return self.__http('POST', uri, body=toDict)

    def delete(self, uri:str, params:dict={}) -> dict:
        """
        HTTP DELETE
        :param uri: URI for the API call
        :param body: DELETE payload
        :return: Response dictionary
        """
        toDict = self.__toDict(params)

        self.logger.info(f"Entering {inspect.stack()[0].function}() from {inspect.stack()[1].function}()")
        self.logger.debug('Params = ' + json.dumps(toDict))

        return self.__http('DELETE', uri, params=toDict)

    def put(self, uri:str, body:dict={}) -> dict:
        """
        HTTP PUT
        :param uri: URI for the API call
        :param body: PUT payload
        :return: Response dictionary
        """
        toDict = self.__toDict(body)

        self.logger.info(f"Entering {inspect.stack()[0].function}() from {inspect.stack()[1].function}()")
        self.logger.debug('Request = ' + json.dumps(toDict))

        return self.__http('PUT', uri, body=toDict)
