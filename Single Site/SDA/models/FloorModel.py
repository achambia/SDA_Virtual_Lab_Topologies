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

""" Catalyst Center Floor data model """

from SDA.enums.RfModelEnum import RfModelEnum


class FloorModel:
    """
    Floor data model
    """
    def __init__(self, name:str, parentName:str, rfModel:RfModelEnum, height:float, length:float, width:float) -> None:
        """
        Constructor
        :param name: Name of the floor
        :param parentName: Name of the parent site
        :param rfModel: Type of floor
        :param height: Height of the floor in feet
        :param length: Length of the floor in feet
        :param width: Width of the floor in feet
        :return: none
        """
        self.name:str =  name
        self.parentName:str =  parentName
        self.rfModel:RfModelEnum =  rfModel
        self.floorNumber:int
        self.height:float =  height
        self.length:float = length
        self.width:float = width
