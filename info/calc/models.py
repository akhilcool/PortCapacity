from django.db import models

# Create your models here.

class ports:
    id: int
    ship:str
    num_ships:int
    port1:str
    port2:str
    load:float
    
class port_cap_class:
    id:int
    name:str
    capacity:float
    percent:float


class Ports(models.Model):
    name=models.CharField(max_length=100)
    anc_area=models.FloatField()
    berth_length=models.FloatField()
    ww_length=models.FloatField()
    slots_num=models.IntegerField()
    cranes_num=models.IntegerField()
    allowable_draft=models.FloatField()
    
class Ships(models.Model):
    name=models.CharField(max_length=100)
    length=models.FloatField()
    max_draft=models.FloatField()
    capacity=models.FloatField()


