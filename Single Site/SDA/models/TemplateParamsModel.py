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

__author__ = "Abhishek Chambial"
__email__ = "achambia@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

""" Catalyst Center TemplateParams data model """

from models.RangeModel import RangeModel
from models.SelectionModel import SelectionModel
from enums.DataTypeEnum import DataTypeEnum
from enums.SelectionTypeEnum import SelectionTypeEnum
class TemplateParamsModel:
    """
    TemplateParams data model
    """

    def __init__(self):
        """
        Constructor
        :return: none
        """
        self.binding:str
        self.customOrder:int
        self.dataType:DataTypeEnum
        self.defaultValue:str
        self.description:str
        self.displayName:str
        self.group:str
        self.id:str
        self.instructionText:str
        self.key:str
        self.notParam:bool
        self.order:int
        self.paramArray:bool
        self.parameterName:str
        self.provider:str
        self.range:list[RangeModel]
        self.required:bool
        self.selection:SelectionModel =  SelectionModel()