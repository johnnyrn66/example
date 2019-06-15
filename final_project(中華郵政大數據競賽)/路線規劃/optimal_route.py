#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:02:56 2019

@author: kiki
"""

from gurobipy import *

n = 192
SN = [0] #start node
EN = [n+1] #end node
#PN = [i for i in range(1,n+1)] #passenger nodes
K = ['morn','after']

DM = 1500.0 # a littl larger than the largest distance/time cost.
TM = 20000.0 #running time upper bound
Mf = 300.0 #upper bound of function (720-480)
mf = -400.0 #lower bound of function (720-1020)
tolerence = 0.0001
mb = 0.2 #objective weight

service = 10 #min
StartT = 8*60.0 #time to start this route
EndT = 17*60.0

#function of clean read data
def clean(row,i):
    b=row.strip().replace("\xc2\xa0", "").replace("\xef\xbb\xbf", "").split(',')[i]
    return b

PN = []#passenger nodes
Rate_Mon = dict()
Rate_Tue = dict()
Rate_Wed = dict()
Rate_Thur = dict()
Rate_Fri = dict()
for i,row in enumerate(open('/Users/kiki/Desktop/final_project/830024/20180109郵務車路線資料(三角分布).csv')):
    if (i >= 1) and (i <= 30):
        if int(clean(row,0)) in PN:
            pass
        else:
            PN.append(int(clean(row,0)))
            a = int(clean(row,0))
            Rate_Mon[a] = dict()
            Rate_Tue[a] = dict()
            Rate_Wed[a] = dict()
            Rate_Thur[a] = dict()
            Rate_Fri[a] = dict()
            Rate_Mon[a]['morn'] = float(clean(row,5))
            Rate_Tue[a]['morn'] = float(clean(row,7))
            Rate_Wed[a]['morn'] = float(clean(row,9))
            Rate_Thur[a]['morn'] = float(clean(row,11))
            Rate_Fri[a]['morn'] = float(clean(row,13))
            Rate_Mon[a]['after'] = float(clean(row,6))
            Rate_Tue[a]['after'] = float(clean(row,8))
            Rate_Wed[a]['after'] = float(clean(row,10))
            Rate_Thur[a]['after'] = float(clean(row,12))
            Rate_Fri[a]['after'] = float(clean(row,14))

AllN = SN+PN+EN

Distance = dict()

for i,row in enumerate(open('/Users/kiki/Desktop/final_project/830024/830024_ODpairs_morn.csv')):
    if i >= 1:
        if int(clean(row,0)) == 0:
            Distance[int(clean(row,0)),int(clean(row,3))] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['morn'] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))]['morn'] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['morn']['Dist']=float(clean(row,6))
            Distance[int(clean(row,3)),int(clean(row,0))]['morn']['Dist']=DM
            Distance[int(clean(row,0)),int(clean(row,3))]['morn']['TT']=float(clean(row,8))
            Distance[int(clean(row,3)),int(clean(row,0))]['morn']['TT']=DM
        else:
            Distance[int(clean(row,0)),int(clean(row,3))] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['morn'] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))]['morn'] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['morn']['Dist']=float(clean(row,6))
            Distance[int(clean(row,3)),int(clean(row,0))]['morn']['Dist']=float(clean(row,6))
            Distance[int(clean(row,0)),int(clean(row,3))]['morn']['TT']=float(clean(row,8))
            Distance[int(clean(row,3)),int(clean(row,0))]['morn']['TT']=float(clean(row,8))

for i,row in enumerate(open('/Users/kiki/Desktop/final_project/830024/830024_ODpairs_after.csv')):
    if i >= 1:
        if int(clean(row,0)) == 0:
            Distance[int(clean(row,0)),int(clean(row,3))]['after'] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))]['after'] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['after']['Dist']=float(clean(row,6))
            Distance[int(clean(row,3)),int(clean(row,0))]['after']['Dist']=DM
            Distance[int(clean(row,0)),int(clean(row,3))]['after']['TT']=float(clean(row,8))
            Distance[int(clean(row,3)),int(clean(row,0))]['after']['TT']=DM
        else:
            Distance[int(clean(row,0)),int(clean(row,3))]['after'] = dict()
            Distance[int(clean(row,3)),int(clean(row,0))]['after'] = dict()
            Distance[int(clean(row,0)),int(clean(row,3))]['after']['Dist']=float(clean(row,6))
            Distance[int(clean(row,3)),int(clean(row,0))]['after']['Dist']=float(clean(row,6))
            Distance[int(clean(row,0)),int(clean(row,3))]['after']['TT']=float(clean(row,8))
            Distance[int(clean(row,3)),int(clean(row,0))]['after']['TT']=float(clean(row,8))

for i in AllN:
    Distance[i,i] = dict()
    Distance[i,i]['after'] = dict()
    Distance[i,i]['morn'] = dict()
    Distance[i,i]['after']['Dist'] = DM
    Distance[i,i]['after']['TT'] = DM
    Distance[i,i]['morn']['Dist'] = DM
    Distance[i,i]['morn']['TT'] = DM

#add a new end node distance information
for i in AllN:
    if i == 0:
        Distance[EN[0],i] = dict()
        Distance[i,EN[0]] = dict()
        Distance[EN[0],i]['after'] = dict()
        Distance[i,EN[0]]['after'] = dict()
        Distance[EN[0],i]['morn'] = dict()
        Distance[i,EN[0]]['morn'] = dict()
        Distance[EN[0],i]['after']['Dist'] = DM
        Distance[EN[0],i]['after']['TT'] = DM
        Distance[i,EN[0]]['after']['Dist'] = DM
        Distance[i,EN[0]]['after']['TT'] = DM
        Distance[EN[0],i]['morn']['Dist'] = DM
        Distance[EN[0],i]['morn']['TT'] = DM
        Distance[i,EN[0]]['morn']['Dist'] = DM
        Distance[i,EN[0]]['morn']['TT'] = DM
    elif i == EN[0]:
        Distance[EN[0],i] = dict()
        Distance[EN[0],i]['after'] = dict()
        Distance[EN[0],i]['morn'] = dict()
        Distance[EN[0],i]['after']['Dist'] = DM
        Distance[EN[0],i]['after']['TT'] = DM
        Distance[EN[0],i]['morn']['Dist'] = DM
        Distance[EN[0],i]['morn']['TT'] = DM
    else:
        Distance[EN[0],i] = Distance[i,0]
        Distance[i,EN[0]] = Distance[0,i]

m = Model('Post')

x = {}
for i in AllN:
    for j in AllN:
        x[i,j] = m.addVar(vtype=GRB.BINARY,name='x_%s_%s' % (i, j))

w = {}
for i in AllN:
    for k in K:
        w[i,k] = m.addVar(vtype=GRB.BINARY,name='w_%s_%s' % (i, k))

time = {}
for i in AllN:
    time[i] = m.addVar(lb = 0, name='time_%s' % (i))

m.update()
#m.setObjective(quicksum(x[i,j]*Distance[i,j]['morn']['TT'] for i in AllN for j in AllN)-mb*quicksum(w[i,k]*Rate_Mon[i][k] for i in PN for k in K), GRB.MINIMIZE)
m.setObjective(quicksum(time[i] for i in EN)-mb*quicksum(w[i,k]*Rate_Tue[i][k] for i in PN for k in K), GRB.MINIMIZE)

m.addConstrs((quicksum(x[i,j] for j in AllN)==1 for i in SN),'start')
m.addConstrs((quicksum(x[i,j] for i in AllN)==0 for j in SN),'nobackstart')
m.addConstrs((quicksum(x[i,j] for i in AllN)==1 for j in EN),'end')

m.addConstrs((quicksum(x[i,j] for j in AllN)==0 for i in EN),'nooutend')
m.addConstrs((quicksum(x[i,j] for j in AllN) == 1 for i in PN ),'visitP')
#m.addConstrs((quicksum(x[i,j] for i in AllN) == 1 for j in PN),'visitP')
m.addConstrs(((quicksum(x[i,j] for i in AllN)-quicksum(x[j,l] for l in AllN))==0 for j in PN),'flow_in_out')

m.addConstrs((time[j]-(time[i]+service+quicksum(w[i,k]*Distance[i,j][k]['TT'] for k in K))>=(x[i,j]-1)*TM for i in PN+SN for j in PN+EN),'count_time')

m.addConstrs((time[i] >= StartT for i in AllN),'start_time')
m.addConstrs((time[i] <= EndT for i in AllN),'end_time')


m.addConstrs((720-time[i]<=w[i,'morn']*Mf for i in AllN),'function_1')
m.addConstrs((720-time[i]>=(1-w[i,'morn'])*(mf-tolerence)+tolerence for i in AllN),'function_2')

m.addConstrs((quicksum(w[i,k] for k in K)==1 for i in AllN), 'function_3')

#m.setParam('OutputFlag', False)
m.setParam('MIPGAP',0.42)

m.optimize()

if m.status == GRB.Status.OPTIMAL:
    print 'objective: %f' % m.ObjVal
    for v in m.getVars():
        if v.x > 0:
            print '%s: %f' % (v.varName, v.x)
else:
    print 'Infeasible!'

count = 0
for i in AllN:
    for j in AllN:
        count += x[i,j].x*Distance[i,j]['morn']['TT']
        
print count