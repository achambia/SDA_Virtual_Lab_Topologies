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

""" Catalyst Center API reserved values to represent SNMP V3 auth protocol types """

from enum import Enum

# 
# Inheriting from 'str' so that it can be JSON serializable
#
class SnmpV3AuthTypeEnum(str, Enum):
    """
    Enumeration to represent SNMP V3 auth protocol types
    """
    SHA:str = 'SHA'
    MD5:str = 'MD5'
    #
    # Override so that the Enum value is returned instead of the Enum name
    # For example, if SomeEnum.SOMEVALUE = 'value', referencing SomeEnum.SOMEVALUE would 
    # return 'SomeEnum.SOMEVALUE' instead of 'value'
    # The latter is the desired result
    #
    def __str__(self):
        return self.value