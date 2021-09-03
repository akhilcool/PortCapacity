import numpy as np
import pandas as pd
from .models import Ports,Ships

final=Ports.objects.all()
final1=Ships.objects.all()

def cap(user):
    port_name,anc_area,berth_length,ww_length,slots_num,cranes_num,allowable_draft,ship_name,ship_len,ship_draft,ship_cap,port_cap=[],[],[],[],[],[],[],[],[],[],[],[]
    
    for i in user:
        for f in final1:
            if f.name==user[i][0]:  
                ship_name.append(f.name)
                ship_len.append(f.length)
                ship_draft.append(f.max_draft)
                ship_cap.append(f.capacity)
                break 

    if len(ship_draft)>1:
        draft_min=min(ship_draft)
    else:
        draft_min=ship_draft[0]
    print(f"min draft is {draft_min}")
    for i in user:
        for f in final:
            if f.name==user[i][0]:
                port_name.append(f.name)
                slots_num.append(f.slots_num)
                #slots_cap.append(float(user["p"+str(i)+"_ac"]))
                cranes_num.append(f.cranes_num)
                #cranes_wh.append(float(user["p"+str(i)+"_ac"]))
                #cranes_moves.append(float(user["p"+str(i)+"_ac"]))
                #allowable_draft.append(f.allowable_draft)
                #teu_ratio.append(float(user["p"+str(i)+"_ac"]))
                print(f"allowable draft for port {f.name} = {f.allowable_draft}")
                if f.allowable_draft >draft_min :
                    port_cap.append(np.min([cranes_num[-1]*20*35*1.5,slots_num[-1]*1500*0.7]))
                else:
                    port_cap.append(0) 
    print('=*'*25)
    print(list(zip(port_name,port_cap)))
    return port_name,port_cap
