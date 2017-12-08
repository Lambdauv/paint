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
                    if (excludepoly == None)|(not gdspy.inside([addtup(ax0pt,ax1pt)],excludepoly)[0]) :
                        refcell=gdspy.CellReference(holecell,addtup(ax0pt,ax1pt))
                        self.holearray.add(refcell)
        elif (numpy.array(holecell).shape == arrayperiods) :
            for i in range(self.Periods[0]):
                ax0pt=addtup((0,0),scalartup(i,self.Axes[0]))
                for j in range(self.Periods[1]):
                    ax1pt=addtup((0,0),scalartup(j,self.Axes[1]))
                    if (excludepoly == None)|(not gdspy.inside([addtup(ax0pt,ax1pt)],excludepoly)[0]) :
                        refcell=gdspy.CellReference(holecell[i,j],addtup(ax0pt,ax1pt))
                        self.holearray.add(refcell)
        else:
            raise ValueError("Error in the holecell input! Not right dimention")
class cross(object):
    def __init__(self,ct,ch,fillet=0,layer=0,datatype=0):
        self.spec={'layer': layer, 'datatype': datatype}
        Harm=gdspy.Path(ct,(-ch/2,0))
        Harm.segment(ch,0,**(self.spec))
        Varm=gdspy.Path(ct,(0,-ch/2))
        Varm.segment(ch,numpy.pi/2,**(self.spec))
        self.paths=[Harm,Varm]
        if (fillet != 0):
            filletwid=fillet*numpy.sqrt(2)
            filletlen=filletwid/2+fillet
            for psign in [-1,1]:
                for qsign in [-1,1]:
                    for len1 in [ct/2,ch/2]:
                        for len2 in [ct/2,ch/2]:
                            pt=(psign*len1,qsign*len2)
                            if (len1 == ch/2)&(len2 == ch/2):
                                continue
                            elif (len1 == ct/2)&(len2 == ct/2):
                                direction=(-psign/numpy.sqrt(2),-qsign/numpy.sqrt(2))
                                p=gdspy.Path(filletwid,(pt[0]-direction[0]*filletwid/2,pt[1]-direction[1]*filletwid/2))
                                #p=gdspy.Path(filletwid,pt)
                                p.segment(filletlen,numpy.arctan2(direction[1],direction[0]),final_width=0)
                                self.paths.append(p)
                            else:
                                direction=(psign/numpy.sqrt(2),qsign/numpy.sqrt(2))
                                p=gdspy.Path(filletwid,(pt[0]-direction[0]*filletwid/2,pt[1]-direction[1]*filletwid/2))
                                #p=gdspy.Path(filletwid,pt)
                                p.segment(filletlen,numpy.arctan2(direction[1],direction[0]),final_width=0)
                                self.paths.append(p)
    def add2cell(self,cell):
        self.cell=cell
        for p in self.paths:
            cell.add(p)

class circle(object):
    def __init__(self,rad,rad_in=None,layer=0,datatype=0):
        self.spec={'layer': layer, 'datatype': datatype}
        self.rad=rad
        if rad_in == None :
            self.circle = gdspy.Round((0, 0), rad,**(self.spec))
        else:
            self.circle = gdspy.Round((0, 0), rad,inner_radius=rad_in,**(self.spec))
            self.rad_in=rad_in
    def add2cell(self,cell):
        self.cell=cell
        cell.add(self.circle)