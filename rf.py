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
    def endgap(self):
        gapwid=self.gapwid
        tracewid=self.tracewid
        if (self.x == self.paths[0].x) & (self.y == self.paths[0].y):
            dirction=self.paths[0].direction
            endctrpt=(self.paths[0].x, self.paths[0].y)
            rightend=addtup(addtup(endctrpt,scalartup(0.5*gapwid,(numpy.cos(dirction+numpy.pi),numpy.sin(dirction+numpy.pi)))),scalartup(0.5*(tracewid+2*gapwid),(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2))))
            endcap = gdspy.Path(gapwid, rightend)
            endcap.segment(tracewid+2*gapwid,dirction+numpy.pi/2)
            self.paths.append(endcap)
        else:
            dirction=self.paths[0].direction
            endctrpt=(self.paths[0].x, self.paths[0].y)
            rightend=addtup(addtup(endctrpt,scalartup(0.5*gapwid,(numpy.cos(dirction),numpy.sin(dirction)))),scalartup(0.5*(tracewid+2*gapwid),(numpy.cos(dirction-numpy.pi/2),numpy.sin(dirction-numpy.pi/2))))
            endcap = gdspy.Path(gapwid, rightend)
            endcap.segment(tracewid+2*gapwid,dirction+numpy.pi/2)
            self.paths.append(endcap)
    def addmeander(self,firstlen,lastlen,straightlen,turnrad,Nturns):
        dirction=self.paths[0].direction
        self.addsegment(dirction,firstlen)
        self.addturn(numpy.pi,turnrad)
        for t in range(Nturns-1) :
            self.addsegment(dirction+(t+1)*numpy.pi,straightlen)
            self.addturn(((-1)**(t+1))*numpy.pi,turnrad)
        self.addsegment(dirction+Nturns*numpy.pi,lastlen)
    def add2cell(self,cell):
        for p in self.paths:
            cell.add(p)
class squid(object):
    def __init__(self,leaddist,leadlen,leadwid,squidheight,layer=0,datatype=1):
        self.spec = {'layer': layer, 'datatype': datatype}
        self.LeadDist=leaddist
        self.LeadWid=leadwid
        self.SquidHeight=squidheight
        self.LeadLen=leadlen
        midlead=gdspy.Path(leadwid,(0,0))
        midlead.segment(leadlen,-numpy.pi/2,**(self.spec))
        midlead.segment(leadlen,-numpy.pi/2,final_width=0,**(self.spec))
        sideleads=gdspy.Path(leadwid,(0,-squidheight),number_of_paths=2,distance=leaddist)
        sideleads.segment(leadlen,numpy.pi/2,**(self.spec))
        sideleads.segment(leadlen,numpy.pi/2,final_width=0,**(self.spec))
        self.paths=[midlead,sideleads]
    def addwires(self,wirewids,extralen=0,layer=0,datatype=1):
        self.spec_wire = {'layer': layer, 'datatype': datatype}
        midlead=gdspy.Path(wirewids[0],(-self.LeadDist/2-extralen,-2*self.LeadLen))
        midlead.segment(self.LeadDist+extralen*2,0,**(self.spec_wire))
        sidelead1=gdspy.Path(wirewids[1],(-self.LeadDist/2,-squidheight+2*self.LeadLen))
        sidelead1.segment(self.SquidHeight-4*self.LeadLen+extralen,numpy.pi/2,**(self.spec_wire))
        sidelead2=gdspy.Path(wirewids[2],(self.LeadDist/2,-squidheight+2*self.LeadLen))
        sidelead2.segment(self.SquidHeight-4*self.LeadLen+extralen,numpy.pi/2,**(self.spec_wire))
        self.paths=self.paths+[midlead,sidelead1,sidelead2]
    def add2cell(self,cell):
        for p in self.paths:
            cell.add(p)
