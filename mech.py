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

def addtup(a,b):
    return tuple(map(operator.add, a, b))
def scalartup(a,v):
    return tuple([a*e for e in v])

class holes(object):
    def __init__(self,name,holecell,arrayaxes=((1,0),(0,1)),arrayperiods=(1,1),excludepoly=None):
        self.Name=name
        self.Axes=arrayaxes
        self.Periods=arrayperiods
        self.holearray=gdspy.Cell(name)
        self.hole=holecell
        self.excludepoly=excludepoly
        if (len(numpy.array(holecell).shape) == 0) :
            for i in range(self.Periods[0]):
                ax0pt=addtup((0,0),scalartup(i,self.Axes[0]))
                for j in range(self.Periods[1]):
                    ax1pt=addtup((0,0),scalartup(j,self.Axes[1]))
                    if (excludepoly == None)|(not gdspy.inside(addtup(ax0pt,ax1pt),excludepoly)) :
                        refcell=gdspy.CellReference(holecell,addtup(ax0pt,ax1pt))
                        self.holearray.add(refcell)
        elif (numpy.array(holecell).shape == arrayperiods) :
            for i in range(self.Periods[0]):
                ax0pt=addtup((0,0),scalartup(i,self.Axes[0]))
                for j in range(self.Periods[1]):
                    ax1pt=addtup((0,0),scalartup(j,self.Axes[1]))
                    if (excludepoly == None)|(not gdspy.inside(addtup(ax0pt,ax1pt),excludepoly)) :
                        refcell=gdspy.CellReference(holecell[i,j],addtup(ax0pt,ax1pt))
                        self.holearray.add(refcell)
        else:
            raise ValueError("Error in the holecell input! Not right dimention")
class cross(object):
    def __init__(self,ct,ch,layer=0,datatype=0):
        self.spec={'layer': layer, 'datatype': datatype}
        Harm=gdspy.Path(ct,(-ch/2,0))
        Harm.segment(ch,0,**(self.spec))
        Varm=gdspy.Path(ct,(0,-ch/2))
        Varm.segment(ch,numpy.pi/2,**(self.spec))
        self.paths=[Harm,Varm]
    def add2cell(self,cell):
        self.cell=cell
        for p in self.paths:
            cell.add(p)