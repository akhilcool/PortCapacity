import gurobipy as gp
from gurobipy import GRB
from itertools import product
import numpy as np
import pandas as pd
from .models import Ports,Ships

final=Ports.objects.all()
final1=Ships.objects.all()

def solve(user):
    port_name,anc_area,berth_length,ww_length,slots_num,cranes_num,allowable_draft,ship_name,ship_len,ship_draft,ship_cap,port_cap=[],[],[],[],[],[],[],[],[],[],[],[]
    for i in user:
        for f in final:
            if f.name==user[i][0]:
                port_name.append(f.name)
                anc_area.append(f.anc_area)
                berth_length.append(f.berth_length)
                ww_length.append(f.ww_length)
                slots_num.append(f.slots_num)
                #slots_cap.append(float(user["p"+str(i)+"_ac"]))
                cranes_num.append(f.cranes_num)
                #cranes_wh.append(float(user["p"+str(i)+"_ac"]))
                #cranes_moves.append(float(user["p"+str(i)+"_ac"]))
                allowable_draft.append(f.allowable_draft)
                #teu_ratio.append(float(user["p"+str(i)+"_ac"]))
                port_cap.append(np.min([cranes_num[-1]*20*35*1.5,slots_num[-1]*1500*0.7]))
    print('=*'*25)
    print(list(zip(port_name,port_cap)))
    
    for i in user:
        for f in final1:
            if f.name==user[i][0]:  
                ship_name.append(f.name)
                ship_len.append(f.length)
                ship_draft.append(f.max_draft)
                ship_cap.append(f.capacity)
                break 
    p=range(len(port_name))
    n=range(len(ship_name))

    m=gp.Model('port')
    x=m.addVars(list(product(n,p,p)),vtype=GRB.CONTINUOUS)

    
    m.addConstrs((gp.quicksum(x[(i,j,j)] for j in p)==0 for i in n))
    m.addConstrs((gp.quicksum(x[(j,k,i)] for k in p)==0 for i in p for j in n if (allowable_draft[i]<=ship_draft[j])))
    m.addConstrs((gp.quicksum(x[(j,i,k)] for k in p)==0 for i in p for j in n if (allowable_draft[i]<=ship_draft[j])))
    #m.addConstrs((gp.quicksum(x[(i,j,k)]*22*(ship_len[i]+40)**2/7e6  for i in n)<=anc_area[k] for j in p for k in p if k!=j))
    m.addConstrs((gp.quicksum(x[(i,j,k)]*22*(ship_len[i]+40)**2/7e6  for i in n for j in p if j!=k )<=anc_area[k]  for k in p ))

    m.addConstrs((gp.quicksum(x[(i,j,k)]*ship_len[i]*2 for i in n for j in p if k!=j )<=ww_length[k]*1000*0.65 for k in p ))
    m.addConstrs((gp.quicksum(x[(i,j,k)]*(ship_len[i]+15) for i in n for j in p if k!=j )<=berth_length[k] for k in p ))
    m.addConstrs((gp.quicksum(x[(i,j,k)]*ship_cap[i]  for i in n for j in p if k!=j)<=slots_num[k]*1500*0.7  for k in p ))
    m.addConstrs((gp.quicksum(x[(i,j,k)]*ship_cap[i]  for i in n for j in p if k!=j)<=cranes_num[k]*20*35*1.5  for k in p ))
    
    m.setObjective(gp.quicksum(x[(i,j,k)] * ship_cap[i] for i in n for j in p for k in p),GRB.MAXIMIZE)

    m.optimize()

    a,b,c,d=[],[],[],[]
    for i in range(len(x.keys())):
        a.append(x.keys()[i][0])
        b.append(x.keys()[i][1])
        c.append(x.keys()[i][2])
        d.append(x[x.keys()[i]].x)
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    d=np.array(d)
    print("d is :",a,b,c,d)

    if all(np.array(d)==0):
        all_zero=True
    else:
        all_zero=False

    indices=list(np.where(np.array(d)>0)[0])
    a=a[indices]
    b=b[indices]
    c=c[indices]
    d=d[indices]
    d1=np.ceil(d)
    d2=d/d1

    print("d is :",list(zip(a,b,c,d)))

    ship,num_ships,port_a,port_b,load=[],[],[],[],[]
    for i,j,k,l,m in zip(a,b,c,d1,d2):
        print(i,j,k,l,m)
        print(f"{l} Ship of type {ship_name[i]} moving from port {port_name[j]} to port {port_name[k]} with load {np.ceil(ship_cap[i]*m)} TEU {round(m*100,2)} % ")
        ship.append(ship_name[i])
        num_ships.append(l)
        port_a.append(port_name[j])
        port_b.append(port_name[k])
        load.append(np.ceil(ship_cap[i]*m))

    d_ports={}
    for i in zip(port_b,load,num_ships):
        d_ports[i[0]]=d_ports.get(i[0],0)+i[1]*i[2]

    print("="*50)
    print(d_ports)

    percent=[]
    for idx,i in enumerate(port_name):
        percent.append(round(d_ports.get(i,0)*100/port_cap[idx],2))
    print("="*50)
    print(percent)

    df=pd.DataFrame()
    df["Ship"]=ship
    df["Number of ships"]=num_ships
    df["Port 1"]=port_a
    df["Port 2"]=port_b
    df["Load"]=load
    

    return df,ship,num_ships,port_a,port_b,load,port_name,port_cap,percent,all_zero
           