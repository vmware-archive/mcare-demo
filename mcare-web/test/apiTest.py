import requests
import json
from datetime import datetime, date, time
from requests.auth import HTTPBasicAuth
import base64

''' http://docs.python-requests.org/en/latest/user/authentication/  '''

headers = {'Accept': 'application/json'}

# URIs

url1 = 'http://customer-service.23.92.225.219.xip.io/api'
url2 = 'http://bwebster-mbpro:5000/api'

# curl -v --data '{"uname":"cheese"}'  http://192.168.0.17:5000/api/user  --header "Content-Type: application/json"

# 
# Create Follower
#

payload={ "timestamp": str(datetime.now()), "modified_timestamp" : str(datetime.now())  , "user_id" :  4 , "ticket_id" : 12 }

r3 = requests.post(url2 + '/followup/', data=json.dumps(payload), headers=headers)
print('status code ' + str(r3.status_code))
data = json.loads(r3.text)
print( data)
id =  data["id"]
timestamp = data["timestamp"]
print ("id= " + str(id))


# 
# Update  Follower
#


midnight = datetime.combine(date.today(), time.min)

payload4={ "id": id,  "timestamp" :  str(midnight), "modified_timestamp" : str(midnight), "user_id" : 4, "ticket_id" : 12 }
print('payload=' + str(payload4))
r4 = requests.put(url2 + '/followup/' + str(id) + "/", data=json.dumps(payload4), headers=headers)
print('status code ' + str(r4.status_code))
data4 = json.loads(r4.text)
print( data4)


# 
# Delete Follower
#

payload5={ "id": id }
print('payload=' + str(payload5))
r5 = requests.delete(url2 + '/followup/' + str(id) + "/", data=json.dumps(payload5), headers=headers)
print('status code ' + str(r5.status_code))


