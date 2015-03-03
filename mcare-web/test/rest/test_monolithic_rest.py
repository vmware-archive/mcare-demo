import sys, os
import unittest
import requests
import json
import base64
from requests.auth import HTTPBasicAuth
from datetime import datetime, date, time

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app import models
from app import db


class Monolithic(unittest.TestCase):
    hdrs = {'Accept': 'application/json'}
    headers = {'content-type': 'application/json'}
    #hdrs = {'Accept': 'application/json', 'content-type': 'application/json'}
    baseurl = os.getenv('HTTP_API_URI')
    apiurl = baseurl + "/api/v1.0"
    uid = 0
    cid = 0
    tid = 0
    mid = 0

    TESTING = True
    print('Using http endpoint ' + baseurl)


    def step0_setup(self):
        # Delete test customer from previous test if it exists.
        # http://192.168.0.12:5000/api/v1.0/users?q={%22uname%22:%22sbspants%22}

        print(self.apiurl +  '/users?q=' + "{\"uname\": \"sbspants\"} ")
        r = requests.get(self.apiurl + '/users?q=' + "{\"uname\": \"sbspants\"} ")
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.text)
        print(data)
        users = data["users"]
        user = users[0]
        self.id =user['id']
        print('status code ' + str(r.status_code))
        print('Found Existing  User ' + str(self.id))

        r = requests.delete(self.apiurl + '/users/' + str(self.id), headers=self.hdrs)
        print('Deleted User  ' + str(self.id))
        print('status code ' + str(r.status_code))
        self.assertEqual(r.status_code, 405)

    # Equivalent to 
    # curl -v --data '{"uname":"cheese"}'  http://192.168.0.17:5000/api/user  --header "Content-Type: application/json"
    def step1_create_user(self):
        payload={ "firstname": "SpongeBob", "lastname" : "SquarePants"  , "phone" : "777-777-7777",  "email" : "bob@bikinibottom.com", "uname" : "sbspants", "password" : "welcome1"}
        r3 = requests.post(self.apiurl + '/users', data=json.dumps(payload), headers=self.headers)
       
        data = json.loads(r3.text)
        if(r3.status_code == 201):
             self.uid = data["id"]
             print('Created Test User ' + str(self.uid))   
        else: 
             print(data)
             print('status code ' + str(r3.status_code))
            

        self.assertEqual(r3.status_code, 201)


    def step2_create_customer(self):
        payload={ "cname": "Test Customer", "email" : "test@testco.com"  , "street" : "anyStreet", "state" : "OH", "user_id" : self.uid}
        r3 = requests.post(self.apiurl + '/customers', data=json.dumps(payload), headers=self.headers)

        data = json.loads(r3.text)
        if(r3.status_code == 201):
             self.cid = data["id"]
             print('Created Test Customer ' + str(self.cid))   
        else: 
             print(data)
             print('status code ' + str(r3.status_code))
            

        self.assertEqual(r3.status_code, 201)


    def step3_create_ticket(self):
        #datetime.time(15, 8, 24, 78915)
        payload={ "ttype": "Late Delivery", "body" : "This is the ticket body",  "timestamp" : str(datetime.utcnow()) , "firstname" : "Peter", \
                  "lastname" : "Baines",  "tstate" : "OPEN", "customer_id" : self.cid, "user_id" : self.uid}
        r3 = requests.post(self.apurl + '/tickets', data=json.dumps(payload), headers=self.headers)
        
        data = json.loads(r3.text)
        if(r3.status_code == 201):
             self.tid = data["id"]
             print('Created Test Ticket ' + str(self.tid))   
        else: 
             print(data)
             print('status code ' + str(r3.status_code))
            

        self.assertEqual(r3.status_code, 201)


    def step4_create_comment(self):
        #datetime.time(15, 8, 24, 78915)
        payload={ "body": "This is a new test comment", "timestamp" : str(datetime.utcnow()) , "notification" : "", "ticket_id" : self.tid, "user_id" : self.uid}
        r3 = requests.post(self.apiurl + '/comments', data=json.dumps(payload), headers=self.headers)
        data = json.loads(r3.text)
        if(r3.status_code == 201):
             print('Created Test Comment ' + str(self.uid))   
        else: 
             print(data)
             print('status code ' + str(r3.status_code))
            

        self.assertEqual(r3.status_code, 201)


    def step4a_create_follower(self):
        payload={ "timestamp": str(datetime.now()), "modified_timestamp" : str(datetime.now())  , "user_id" :  4 , "ticket_id" : 12 }

        r7 = requests.post(self.apiurl + '/followers',  data=json.dumps(payload), headers=headers)
        
        if(r7.status_code == 201):
             self.fid = data["id"]
             print('Created Test Follower ' + str(self.fid))   
        else: 
             print(data)
             print('status code ' + str(r7.status_code))
            

        self.assertEqual(r3.status_code, 201)


    def step5_get_customer(self):
        #datetime.time(15, 8, 24, 78915)
        r = requests.get(self.apiurl + '/customers/' + str(self.cid), headers=self.hdrs)
        data = json.loads(r.text)
        print('status code ' + str(r.status_code))
        print('Retrieved Customer  ' + str(self.mid))
        self.assertEqual(r.status_code, 200)

        
    def step6_get_customer_ticket(self):
        #datetime.time(15, 8, 24, 78915)
        r = requests.get(self.apiurl + '/customers/' + str(self.cid) + '/tickets/' + str(self.tid), headers=self.hdrs)
        data = json.loads(r.text)
        print('status code ' + str(r.status_code))
        print('Retrieved Customer\'s tickets  ' + str(self.mid))
        self.assertEqual(r.status_code, 200)

 


    def step7b_update_follower(self):
        midnight = datetime.combine(date.today(), time.min)

        payload4={ "id": self.fid,  "timestamp" :  str(midnight), "modified_timestamp" : str(midnight), "user_id" : 4, "ticket_id" : 12 }
        print('payload=' + str(payload4))
        r8 = requests.put(self.apiurl + '/followers/' + str(self.fid) + "/", data=json.dumps(payload4), headers=headers)
        print('status code ' + str(r8.status_code))
        self.assertEqual(r8.status_code, 200)
        data4 = json.loads(r8.text)


    def step9_update_follower(self):
        payload5={ "id": self.fid }
        print('payload=' + str(payload5))
        r5 = requests.delete(self.apiurl + '/followers/' + str(self.fid) + "/", data=json.dumps(payload5), headers=headers)
        print('status code ' + str(r5.status_code))


    def step9a_delete_comment(self):
        r = requests.delete(self.apiurl + '/comments/' + str(self.mid), headers=self.hdrs)
        print('status code ' + str(r.status_code))
        print('Deleted Comment  ' + str(self.mid))
        self.assertEqual(r.status_code, 204)

    def step9b_delete_ticket(self):
        r = requests.delete(self.apiurl + '/tickets/' + str(self.tid), headers=self.hdrs)
        print('status code ' + str(r.status_code))
        print('Deleted Ticket  ' + str(self.tid))
        self.assertEqual(r.status_code, 204)

    def step9c_delete_customer(self):
        r = requests.delete(self.apiurl + '/customers/' + str(self.cid), headers=self.hdrs)
        print('status code ' + str(r.status_code))
        print('Deleted Customer  ' + str(self.cid))
        self.assertEqual(r.status_code, 204)

    def step9d_delete_user(self):
        r = requests.delete(self.apiurl + '/users/' + str(self.uid), headers=self.hdrs)
        print('status code ' + str(r.status_code))
        print('Deleted User  ' + str(self.uid))
        self.assertEqual(r.status_code, 204)

    def steps(self):
        for name in sorted(dir(self)):
          if name.startswith("step"):
              yield name, getattr(self, name) 

    def test_steps(self):
        for name, step in self.steps():
        #  try:
            print('Running Step ' + name);
            step()
        #  except Exception as e:
        #    self.fail("{} failed ({}: {})".format(step, type(e), e))



''' http://docs.python-requests.org/en/latest/user/authentication/  '''

headers = {'Accept': 'application/json'}


if __name__ == '__main__':
    unittest.main()
