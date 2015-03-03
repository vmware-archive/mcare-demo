from flask.ext.sqlalchemy import SQLAlchemy
from . import config
from config import config

from app.storage.db.model import *
from datetime import datetime
from sqlalchemy import update
from . import db

import requests
import json
import base64

from requests.auth import HTTPBasicAuth

def main():
  
    # Apple push notification provider
    apnp = config['development'].APNP
    if (apnp == 'KINVEY'):
       kinveyUrl = config['development'].KINVEY_URL
       kinveyAppId = config['development'].KINVEY_APP_ID
       baseurl =  kinveyUrl + '/rpc/' + kinveyAppId + '/custom/pushNotification'
       kinveyUser = config['development'].KINVEY_USER
       kinveyPassword = config['development'].KINVEY_PASSWORD

       encodedCreds = base64.b64decode(kinveyUser + ":" + kinveyPassword)
       basicAuthValue = 'Basic ' + encodedCreds
       hdrs = {'Authorization': basicAuthValue, 'Accept': 'application/json', 'content-type': 'application/json'}
    else:

       baseurl = config['development'].PHP_URL
       hdrs = {'Accept': 'application/json', 'content-type': 'application/json'}

    # get all tickets with tstate = OPEN and has followers
    #
    #    for each ticket's followers
    #      if ticket.modified_timestamp != follower.modified_timestamp
    #         add the follower user to a list
    #         set the follower timestamp = ticket modified_timestamp
    #         update the follower record
    #
    # Call push rest service and pass user list
    #        

    # http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#querying

    # Get open tickets with followers 
    sql2 = db.session.query(Ticket, Follower, User)
    sql2 = sql2.filter(Ticket.id==Follower.ticket_id)
    sql2 = sql2.filter(Follower.user_id==User.id)
    sql2 = sql2.filter(Ticket.tstate=='OPEN')
 
    uList = []
    for t, f, u in sql2.all():
       if(t.modified_timestamp != f.modified_timestamp):
           print ('Ticket ' , t.id, 'Follower ', f.id, 'Ticket Modified Timestamp ', t.modified_timestamp, 'Follower Modified Timestamp ', f.modified_timestamp, 'User ', u.uname);
           uList.append( u.uname )
           #stmt = update(Follower).where(Follower.id==f.id).values(modified_timestamp=t.modified_timestamp)
           #conn.execute(stmt) 
           db.session.add(f)
           db.session.add(t)
           f.modified_timestamp=t.modified_timestamp
           db.session.flush()
           db.session.commit()
           print(str(datetime.now()) + ' Ticket ' + str(t.modified_timestamp) + ' Follower ' + str(f.modified_timestamp))       

    if( len(uList) >0):
        print ('customer ' + t.customer.cname)

        if (apnp == 'KINVEY'):
           payload={ u"username": u.uname, u"customer" : t.customer.cname, u"number" : t.tnumber }
           print('Calling ' + baseurl + ' with payload ' + str(payload) + ' and headers ' + str(hdrs))
           r3 = requests.post(baseurl, data=json.dumps(payload), headers=hdrs)
           print('status code ' + str(r3.status_code))

        else:
           payload={ "customer" : t.customer.cname, "number" : t.tnumber }
           print('Calling ' + baseurl + ' with payload ' + str(payload))
           r3 = requests.get(baseurl, params=payload)
           print('status code ' + str(r3.status_code))
    else:
        print(str(datetime.now()) + ' ticketNotifier: no newly modified tickets')



if __name__ == "__main__":
   # stuff to run when called by a command line vs import 
   main()
