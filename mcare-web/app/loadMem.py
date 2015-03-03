
import traceback
import sys, os
import unittest
import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime, date, time
from app.storage.mem.model import User, Customer, Ticket
from app.storage.mem.memstore import MemStore
#from app import memorystore

def jdefault(obj):
    if hasattr(obj, 'isoformat'):
           return obj.isoformat()
    return obj.__dict__

def main(memorystore):

        if memorystore == None:
            memorystore =  MemStore()

        u1 = User.create(uname='bwebster', email="bwebster@vmware.com", password="welcome1", firstname='bob', lastname='webster', \
                  phone='777-777-7777', kinveyuser="bwebster", kinveypassword="welcome1")
    
        print ('Added User ' + str(u1.id))


        # Customer 1
        c1 = Customer.create(cname='James Distribution', firstname="Susan", lastname="Wright", email='swright@jamesdistco.com', \
                      street='3445 North First Street', city='Afton', state='MN', postal='55001', user_id = u1.id )
      
        print ('Added Customer ' + str(c1.id))

        print(json.dumps(c1, indent=4, default=jdefault))

        MemStore.addValue(c1.id, [c1.cname], c1)   # pkey, altKeys, obj
         
        cnew = MemStore.getValue(c1.id)
        print('Retrieved ' + str(cnew))

        # Customer 2
        c2 = Customer.create(cname='Western Medical Supply', firstname="Alfred", lastname="Chang", email='alred.chang@westmedsupply.com', \
                     street='3445 North First Street', city='San Jose', state='CA', postal='95101', user_id = u1.id)
      
        print ('Added Customer ' + str(c2.id))


        c1t1 = Ticket.create(ttype='Shipment Issue', body='Shipment 4233 on July 13 arrived late.', timestamp= datetime.now(), \
                      customer_id=c1.id, firstname='Ellis', lastname='James', phone='480-425-1836', \
                      cemail='ellis@westmedsupply.com', user_id=u1.id, tstate='OPEN', tpriority=3 )

        print(json.dumps(c1t1, indent=4, default=jdefault))
  
       
        c2t2 = Ticket.create(ttype='Customer Inquiry', body='Customer inquired whether shipments can be held over the holidays. ', \
                      timestamp= datetime.now(),  customer_id=c2.id,  firstname='Ellis', lastname='James', \
                      phone='480-425-1836', cemail='ellis@westmedsupply.com', user_id=u1.id, tstate='CLOSED', tpriority=2)


        print ('Added Ticket ' + str(c1t1.id))


if __name__ == "__main__":
   # stuff to run when called by a command line vs import 
   main(memorystore)
