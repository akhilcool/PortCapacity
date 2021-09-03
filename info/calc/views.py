from django.shortcuts import render
from django.http import HttpResponse
from .models import Ports,ports,Ships,port_cap_class

# Create your views here.

#from calc.gur import *
from calc.uttej import *
from calc.capacity import *

def main(request):
    return render(request,'main.html')

def home_cap(request):
    final=Ports.objects.all()
    final1=Ships.objects.all()
    return render(request,'first.html',{'final':final,'final1':final1})

def home_opt(request):
    final=Ports.objects.all()
    final1=Ships.objects.all()
    return render(request,'first1.html',{'final':final,'final1':final1}) 

def port_capacity(request):
    user=dict(request.POST)
    port_name,port_cap=cap(user)
    print('*#'*50)
    print(user)
    final_res1=[]
    for i in range(len(port_cap)):
        temp=port_cap_class()
        temp.name=port_name[i]
        temp.capacity=port_cap[i]
        final_res1.append(temp)
    print(final_res1)
    return render(request,'capacity.html',{"final":final_res1})

def optimise(request):
    user=dict(request.POST)
    df,ship,num_ships,port_a,port_b,load,port_name,port_cap,percent,all_zero=solve(user)
    print(user)
    final_res,final_res1=[],[]
    for i in range(len(num_ships)):
        temp=ports()
        temp.ship=ship[i]
        temp.num_ships=num_ships[i]
        temp.port1=port_a[i]
        temp.port2=port_b[i]
        temp.load=load[i]
        final_res.append(temp)
    print(final_res)

    for i in range(len(port_cap)):
        temp=port_cap_class()
        temp.name=port_name[i]
        temp.capacity=port_cap[i]
        temp.percent=percent[i]
        final_res1.append(temp)
    print(final_res1)
    return render(request,'result.html',{"final":final_res,"final1":final_res1,"all_zero":all_zero})



