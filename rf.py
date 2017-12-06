######################################################################
#                                                                    #
#  Copyright 2017- Lambdauv.                                        #
#  This file is part of paint, distributed under the terms of the    #
#  MIT License                                                       #
#  
#  This module contains classes for constructing RF elements         #
######################################################################
import gdspy
import numpy
import operator
def addtup(a,b):
    return tuple(map(operator.add, a, b))
def scalartup(a,v):
    return tuple([a*e for e in v])
class cpw(object):
    def __init__(self,Name,TraceWid,GapWid,x,y,layer=0,datatype=1,direction=0):
        self.name=Name
        self.tracewid=TraceWid
        self.gapwid=GapWid
        self.x=x
        self.y=y
        self.cell = gdspy.Cell(Name)
        self.paths=[gdspy.Path(GapWid, (x, y), number_of_paths=2, distance=TraceWid+GapWid)]
        self.paths[0].direction=direction
        self.spec = {'layer': layer, 'datatype': datatype}
    def addsegment(self,Direction,Length,final_TraceWid=None,final_GapWid=None):
        if (final_TraceWid != None)&(final_GapWid != None):
            self.paths[0].segment(Length,Direction,**(self.spec),final_distance=final_TraceWid+final_GapWid,final_width=final_GapWid)
        else:
            self.paths[0].segment(Length,Direction,**(self.spec))
    def addturn(self,angle,radius,final_TraceWid=None,final_GapWid=None):
        if (final_TraceWid != None)&(final_GapWid != None):
            self.paths[0].turn(radius,angle,final_distance=final_TraceWid+final_GapWid,final_width=final_GapWid,**(self.spec))
        else:
            self.paths[0].turn(radius,angle,**(self.spec))
    def addcurve(self,curve,dcurve=None,Widths=None,Neval=600):
        self.paths[0].parametric(curve,dcurve,final_width=Widths,number_of_evaluations=Neval,**(self.spec))
    def addlauncher(self,final_TraceWid,final_GapWid,final_Length,tran_Length):
        if (self.x == self.paths[0].x) & (self.y == self.paths[0].y):
            dirction=self.paths[0].direction
            self.addsegment(dirction+numpy.pi,tran_Length,final_TraceWid,final_GapWid)
            self.addsegment(dirction+numpy.pi,final_Length)
            endctrpt=(self.paths[0].x, self.paths[0].y)
            rightend=addtup(addtup(endctrpt,scalartup(0.5*final_GapWid,(numpy.cos(dirction+numpy.pi),numpy.sin(dirction+numpy.pi)))),scalartup(0.5*(final_TraceWid+2*final_GapWid),(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2))))
            pathlaunch = gdspy.Path(final_GapWid, rightend)
            pathlaunch.segment(final_TraceWid+2*final_GapWid,dirction+numpy.pi/2)
            self.paths[0].x=self.x
            self.paths[0].y=self.y
            self.paths[0].distance=self.tracewid+self.gapwid
            self.paths[0].w=self.gapwid/2
            self.paths.append(pathlaunch)
        else:
            self.finalx=self.paths[0].x
            self.finaly=self.paths[0].y
            dirction=self.paths[0].direction
            self.addsegment(dirction,tran_Length,final_TraceWid,final_GapWid)
            self.addsegment(dirction,final_Length)
            endctrpt=(self.paths[0].x, self.paths[0].y)
            rightend=addtup(addtup(endctrpt,scalartup(0.5*final_GapWid,(numpy.cos(dirction),numpy.sin(dirction)))),scalartup(0.5*(final_TraceWid+2*final_GapWid),(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2))))
            pathlaunch = gdspy.Path(final_GapWid,rightend )
            pathlaunch.segment(final_TraceWid+2*final_GapWid,dirction+numpy.pi/2)
            self.paths[0].x=self.finalx
            self.paths[0].y=self.finaly
            self.paths.append(pathlaunch)
    def add2cell(self,cell):
        for p in self.paths:
            cell.add(p)

