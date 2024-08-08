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

""" Catalyst Center API reserved values to represent Data Type """

from enum import Enum

class FailurePolicyEnum(str, Enum):
    """
    Enumeration to represent Selection Type
    """
    ABORT_ON_ERROR:str = 'ABORT_ON_ERROR'
    CONTINUE_ON_ERROR:str = 'CONTINUE_ON_ERROR'
    ROLLBACK_ON_ERROR:str = 'ROLLBACK_ON_ERROR'
    ROLLBACK_TARGET_ON_ERROR:str = 'ROLLBACK_TARGET_ON_ERROR'
    ABORT_TARGET_ON_ERROR:str = 'ABORT_TARGET_ON_ERROR'
    #
    # Override so that the Enum value is returned instead of the Enum name
    # For example, if SomeEnum.SOMEVALUE = 'value', referencing SomeEnum.SOMEVALUE would
    # return 'SomeEnum.SOMEVALUE' instead of 'value'
    # The latter is the desired result
    #
    def __str__(self):
        return self.value