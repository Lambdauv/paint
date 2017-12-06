######################################################################
#                                                                    #
#  Copyright 2017- Lambdauv.                                        #
#  This file is part of paint, distributed under the terms of the    #
#  MIT License                                                       #
#  
#  This module contains classes for constructing Mechanical elements #
######################################################################
import gdspy
import numpy
import operator

class holes(object):
    def __init__(self,name,arrayaxes=((1,0),(0,1)),arrayperiods=(1,1)):
        self.Name=name
        self.Axes=arrayaxes
        self.Periods=arrayperiods