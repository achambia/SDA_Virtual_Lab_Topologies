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

""" Catalyst Center Building data model """

class BuildingModel:
    """
    Building data model
    """
    def __init__(self, name:str, parentName:str, latitude:float, longitude:float) -> None:
        """
        Constructor
        :param name: Name of the building
        :param parentName: Name of the parent site
        :param latitude: Latitude coordinate of the building
        :param longitude: Longitude coordinate of the building 
        :return: none
        """
        self.address:str
        self.country:str
        self.name:str =  name
        self.parentName:str = parentName
        self.latitude:float = latitude
        self.longitude:float = longitude