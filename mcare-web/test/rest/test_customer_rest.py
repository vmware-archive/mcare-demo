import os, sys
import unittest
import requests
import json

from requests.auth import HTTPBasicAuth
from datetime import datetime

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app import models
from app import db
from app import models 
from app import db


class MyTest(unittest.TestCase):
    hdrs = {'Accept': 'application/json'}
    headers = {'content-type': 'application/json'}
    #hdrs = {'Accept': 'application/json', 'content-type': 'application/json'}
    baseurl = os.getenv('HTTP_API_URI') 

    print('Using http endpoint ' + baseurl)

    TESTING = True

    def create_app(self):
        print('')

    def setUp(self):
        print('')

    def tearDown(self):
        print('')
       

#
#   Test
#

    # get a customers tickets
#    def test_customer_rest(self):

    #    r1 = requests.get(self.baseurl + '/api/v1.0/customers/', headers=self.hdrs)
    #    self.assertEqual(r1.status_code, 200)
    #    print('status code ' + str(r1.status_code))
        #print('response = ' + r1.text)
   #     print('Query 1 Done')

      #  r2 = requests.get(self.baseurl + '/api/v1.0/customers/1/tickets/', headers=self.hdrs)
      #  self.assertEqual(r2.status_code, 200)

       # print('status code ' + str(r2.status_code))
      #  print('response = ' + r2.text)
      #  print('Query2 Done')

    if __name__ == '__main__':
        unittest.main()
