import requests
import json
from requests.auth import HTTPBasicAuth
import base64

''' http://docs.python-requests.org/en/latest/user/authentication/  '''

headers = {'Accept': 'application/*+xml;version=5.6'}

# Get URIs

payload={ "firstname": "SpongeBob", "lastname" : "SquarePants"  , "phone" : "777-777-7777",  "email" : "bob@bikinibottom.com", "uname" : "sbspants" }


url1 = 'http://customer-service.23.92.225.219.xip.io/loginauth'
url2 = 'http://bwebster-mbpro:5000/loginauth'

# Test Success
r3 = requests.get(url1, auth=HTTPBasicAuth('bwebster', 'welcome1'))
print('Headers ' + r3.request.headers['Authorization'])
#print('Response Text ' + r3.text)
print('status code ' + str(r3.status_code))
print('final url  ' + str(r3.url))

# Success final url  http://bwebster-mbpro:5000/loginauth
# final url  http://bwebster-mbpro:5000/loginauth

# Test Fail
# status code 200
# final url  http://bwebster-mbpro:5000/login/?next=%2Floginauth

#r4 = requests.get('http://localhost:5000/loginauth', auth=HTTPBasicAuth('bwebste', 'welcome2'))
#print('Headers ' + r4.request.headers['Authorization'])
#print('Response Text ' + r4.text)
#print('status code ' + str(r4.status_code))
#print('final url  ' + str(r4.url))

