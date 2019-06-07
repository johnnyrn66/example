#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:42:46 2019

@author: kiki
"""

from gurobipy import *

AllN = [0,1,2,3,4,5,6] #all nodes
SN = [0] #start node
EN = [1] #end node
PN = [2,3,4,5,6] #passenger nodes

M = 150 # a littl larger than the largest distance/time cost.
TM = 1000
service = 15 #min
StartT = 8*60 #time to start this route

cost = [[M,	M,	89,	13,	94,	66,	66],
        [M,	M,	50,	14,	58,	49,	36],
        [89,	50,	M,	10,	33,	86,	83],
        [13,	14,	10,	M,	37,	18,	18],
        [94,	58,	33,	37,	M,	40,	76],
        [66,	49,	86,	18,	40,	M,	21],
        [66,	36,	83,	18,	76,	21,	M]]

m = Model('Post')

x = {}
for i in AllN:
    for j in AllN:
        x[i,j] = m.addVar(vtype=GRB.BINARY,name='x_%s%s' % (i, j))
time = {}
for i in AllN:
    time[i] = m.addVar(name='time_%s' % (i))

m.update()
m.setObjective(quicksum(cost[i][j]*x[i,j] for i in AllN for j in AllN), GRB.MINIMIZE)
m.addConstrs((quicksum(x[i,j] for j in PN)==1 for i in SN),'start')
m.addConstrs((quicksum(x[i,j] for i in PN)==1 for j in EN),'end')
m.addConstrs((quicksum(x[i,j] for j in AllN)==1 for i in PN),'visitP')
m.addConstrs((quicksum(x[i,j] for i in AllN)-quicksum(x[j,k] for k in AllN)==0 for j in PN),'flow_in_out')
m.addConstrs((time[j]-(time[i]+service+cost[i][j])>=(x[i,j]-1)*TM for i in AllN for j in AllN),'count_time')
m.addConstrs((time[i]>=StartT for i in SN),'start_time')
m.setParam('OutputFlag', False)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print 'objective: %f' % m.ObjVal
    for v in m.getVars():
        if v.x > 0:
            print '%s: %f' % (v.varName, v.x)
else:
    print 'Infeasible!'