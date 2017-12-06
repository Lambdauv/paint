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

class cpw(object):
    def __init__(self,Name,TraceWid,GapWid,x,y,layer):
        self.name=Name
        self.tracewid=TraceWid
        self.gapwid=GapWid
        self.x=x
        self.y=y
        self.cell = gdspy.Cell(Name)
        self.paths=[gdspy.Path(GapWid, (x, y), number_of_paths=2, distance=TraceWid+GapWid)]
        self.spec = {'layer': layer, 'datatype': 1}
    def addsegment(self,Direction,Length,final_TraceWid=None,final_GapWid=None):
        self.paths[0].segment(Length,Direction,**(self.spec),final_distance=final_TraceWid+final_GapWid,final_width=final_GapWid)
    def addturn(self,angle,radius,final_TraceWid=None,final_GapWid=None):
        self.paths[0].turn(radius,angle,final_distance=final_TraceWid+final_GapWid,final_width=final_GapWid,**(self.spec))
    def addcurve(self,curve,dcurve=None,Widths=None,Neval=600,layer=0):
        self.paths[0].parametric(curve,dcurve,final_width=Widths,number_of_evaluations=Neval,layer=layer)
    def addlauncher(self,final_TraceWid,final_GapWid,final_Length,tran_Length):
        if (self.x == self.paths[0].x) & (self.y == self.paths[0].y):
            dirction=self.paths[0].direction
            self.addsegment(dirction+numpy.pi,tran_Length,final_TraceWid,final_GapWid)
            self.addsegment(dirction+numpy.pi,final_Length)
            rightend=addtup(endctrpt,0.5*(final_TraceWid+final_GapWid)*(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2)))
            pathlaunch = gdspy.Path(final_GapWid, rightend)
            pathlaunch.segment((final_TraceWid+final_GapWid,dirction+numpy.pi/2))
            self.paths[0].x=self.x
            self.paths[0].y=self.y
        else:
            self.finalx=self.paths[0].x
            self.finaly=self.paths[0].y
            dirction=self.paths[0].direction
            self.addsegment(dirction,tran_Length,final_TraceWid,final_GapWid)
            self.addsegment(dirction,final_Length)
            endctrpt=(paths[0].x, paths[0].y)
            rightend=addtup(endctrpt,0.5*(final_TraceWid+final_GapWid)*(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2)))
            pathlaunch = gdspy.Path(final_GapWid,rightend )
            pathlaunch.segment((final_TraceWid+final_GapWid,dirction+numpy.pi/2))
            self.paths[0].x=self.finalx
            self.paths[0].y=self.finaly
    def add2cell(self,cell):
        for p in self.paths:
            cell.add(p)

