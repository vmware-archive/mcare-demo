
import sys, os
import requests
import json
import traceback
from datetime import datetime, date, time
#
from config import config
from app.mcexception import MCException


headers = {'content-type': 'application/json', 'Accept': 'application/json'}


def step1_create_user(apiurl):
        payload={ "firstname": "Bob", "lastname" : "Webster"  , "phone" : "777-777-7777",  "email" : "bwebster@vmware.com", \
                  "uname" : "bwebster", "password" : "welcome1"}
        r = requests.post(apiurl + '/users', data=json.dumps(payload), headers=headers)
        print('calling ' + apiurl)
      

        if(r.status_code == 201):
            data = json.loads(r.text)
            user = data["user"]
            user1_id =user['id']
        else: 
            print('status code ' + str(r.status_code))
            raise MCException('status code ' + str(r.status_code) + " " + str(r.text))

        return user1_id
       

def step2_create_customer1( apiurl, uid):

        payload={ "cname": "James Distribution", "firstname" : "Susan"  , "lasname" : "Wright",  "email" : "swright@jamesdistco.com", \
                  "street" : "3445 North First Street", "city" : "Afton", "state" : "MN", "postal" : "55001", "user_id" : uid }
        r = requests.post(apiurl + '/customers', data=json.dumps(payload), headers=headers)

        if(r.status_code == 201):
            data = json.loads(r.text)
            customer = data["customer"]
            customer_id = customer['id']
        else: 
            print('status code ' + str(r.status_code))
            raise MCException('status code ' + str(r.status_code) + " " + str(r.text))

        return customer_id


def step3_create_ticket1( apiurl, uid, cid):

 
        payload={ "ttype" : "Shipment Issue", "body" : "Shipment 4233 on July 13 arrived late.", \
                  "customer_id": cid, "firstame" : "Ellis", "lastname" : "James",  \
                  "phone" : "480-425-1836", "cemail" : "ellis@westmedsupply.com", \
                  "user_id" : uid, "tstate": "OPEN", "tpriority":3, "timestamp" : str(datetime.now()) }

        r = requests.post(apiurl + '/tickets', data=json.dumps(payload), headers=headers)

        if(r.status_code == 201):
            data = json.loads(r.text)
            ticket = data["ticket"]
            ticket_id = ticket['id']
        else: 
            print('status code ' + str(r.status_code))
            raise MCException('status code ' + str(r.status_code) + " " + str(r.text))

        return ticket_id


def main():

    try: 

        pythonPort = config['development'].PYTHON_PORT
        pythonHost = config['development'].PYTHON_HOST

        apiurl = "http://" + pythonHost + ":" + pythonPort  + "/api/v1.0"

        user1_id = step1_create_user(apiurl=apiurl)
        print('Created User ' + user1_id)   

        cust1_id = step2_create_customer1(apiurl=apiurl, uid=user1_id)
        print('Created Customer ' + cust1_id)  

        ticket1_id = step3_create_ticket1(apiurl=apiurl, uid=user1_id, cid=cust1_id) 
        print('Created Ticket ' + ticket1_id) 

        return 0

    except MCException as e:
           
        var = traceback.format_exc()
        print ("LoadStorage Caught Unexpected error:", e)
        return -1

if __name__ == "__main__":
   # stuff to run when called by a command line vs import 
   main()
