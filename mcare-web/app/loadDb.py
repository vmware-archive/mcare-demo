


from datetime import datetime
import sys, traceback
from config import config

from app import db

from app.storage.db.model import *
from app.db import engine
from app.storage.db.model import Follower, Comment, Ticket, Customer, User

def main():



    try: 

        # List Existing DB Tables

        from sqlalchemy import inspect
        inspector = inspect(engine)
        print("Current Tables in DB")
        for table_name in inspector.get_table_names():
            print("Table: " + table_name)
            for column in inspector.get_columns(table_name):
              print("Column: %s" % column['name'])

        # List all known Tables according to MetaData
        from sqlalchemy import MetaData
        print("Current Tables defined by Model MetaData")
        m = MetaData()
        m.reflect(engine)
        for table in m.tables.values():
           print("Table: " + table.name)
           for column in table.c:
               print(column.name)
           print("")


        session.commit()
       
        # use these over db.drop_all() so deletes can happen without server shutdown
        # Order must be maintained or constraint dependency exceptions will occur
        Follower.query.delete()
        Comment.query.delete()
        Ticket.query.delete()
        Customer.query.delete()
        User.query.delete()
       
        States.query.delete()

        session.commit()

        session.add(States(sname='Alabama', abbr='AL'))
        session.add(States(sname='Alaska',  abbr='AK'))
        session.add(States(sname='Arizona ', abbr='AZ'))
        session.add(States(sname='Arkansas',    abbr='AR'))
        session.add(States(sname='California',  abbr='CA'))
        session.add(States(sname='Colorado',    abbr='CO'))
        session.add(States(sname='Connecticut', abbr='CT'))
        session.add(States(sname='Delaware',    abbr='DE'))
        session.add(States(sname='Florida', abbr='FL'))
        session.add(States(sname='Georgia', abbr='GA'))
        session.add(States(sname='Hawaii',  abbr='HI'))
        session.add(States(sname='Idaho',   abbr='ID'))
        session.add(States(sname='Illinois',  abbr='IL'))
        session.add(States(sname='Indiana', abbr='IN'))
        session.add(States(sname='Iowa',    abbr='IA'))
        session.add(States(sname='Kansas',  abbr='KS'))
        session.add(States(sname='Kentucky',   abbr='KY'))
        session.add(States(sname='Louisiana',   abbr='LA'))
        session.add(States(sname='Maine',   abbr='ME'))
        session.add(States(sname='Maryland',    abbr='MD'))
        session.add(States(sname='Massachusetts',   abbr='MA'))
        session.add(States(sname='Michigan',    abbr='MI'))
        session.add(States(sname='Minnesota',   abbr='MN'))
        session.add(States(sname='Mississippi', abbr='MS'))
        session.add(States(sname='Missouri',   abbr='MO'))
        session.add(States(sname='Montana', abbr='MT'))
        session.add(States(sname='Nebraska',  abbr='NE'))
        session.add(States(sname='Nevada', abbr='NV'))
        session.add(States(sname='New Hampshire',  abbr='NH'))
        session.add(States(sname='New Jersey',  abbr='NJ'))
        session.add(States(sname='New Mexico',  abbr='NM'))
        session.add(States(sname='New York',    abbr='NY'))
        session.add(States(sname='North Carolina',  abbr='NC'))
        session.add(States(sname='North Dakota',    abbr='ND'))
        session.add(States(sname='Ohio',    abbr='OH'))
        session.add(States(sname='Oklahoma',    abbr='OK'))
        session.add(States(sname='Oregon',  abbr='OR'))
        session.add(States(sname='Pennsylvania',    abbr='PA'))
        session.add(States(sname='Rhode Island',    abbr='RI'))
        session.add(States(sname='South Carolina ', abbr='SC'))
        session.add(States(sname='South Dakota',    abbr='SD'))
        session.add(States(sname='Tennessee',   abbr='TN'))
        session.add(States(sname='Texas',   abbr='TX'))
        session.add(States(sname='Utah',   abbr='UT'))
        session.add(States(sname='Vermont', abbr='VT'))
        session.add(States(sname='Virginia',    abbr='VA'))
        session.add(States(sname='Washington',  abbr='WA'))
        session.add(States(sname='West Virginia',   abbr='WV'))
        session.add(States(sname='Wisconsin',   abbr='WI'))
        session.add(States(sname='Wyoming', abbr='WY'))
        
        session.add(States(sname='American Samoa',  abbr='AS'))
        session.add(States(sname='District of Columbia',   abbr='DC'))
        session.add(States(sname='Federated States of Micronesia', abbr='FM'))
        session.add(States(sname='Guam',    abbr='GU'))
        session.add(States(sname='Marshall Islands',    abbr='MH'))
        session.add(States(sname='Northern Mariana Islands',    abbr='MP'))
        session.add(States(sname='Palau',   abbr='PW'))
        session.add(States(sname='Puerto Rico', abbr='PR'))
        session.add(States(sname='Virgin Islands',  abbr='VI'))
        session.flush()
        print ('Added States')
        
        u1 = User(uname='bwebster', email="bwebster@vmware.com", password="welcome1", kinveyuser="bwebster", kinveypassword="welcome1")
        session.add(u1);
        session.flush()
        print ('Added User ' + str(u1.id))

    

        # Customer 1
        c1 = Customer(cname='James Distribution', firstname="Susan", lastname="Wright", email='swright@jamesdistco.com', \
                      street='3445 North First Street', city='Afton', state='MN', postal='55001', user_id = u1.id )
        session.add(c1);
        session.flush()
        print ('Added Customer ' + str(c1))

        # Contact 1
      #  n1 = Contact(title="Ms.", firstname="Susan", lastname="Wright", email='swright@jamesdistco.com', \
      #                street='3445 North First Street', city='Afton', state='MN', postal='55001', customer_id = c1.id )
      #  session.add(n1);
      #  print ('Added Contact ' + str(c1))


        # Customer 2
        c2 = Customer(cname='Western Medical Supply', firstname="Alfred", lastname="Chang", email='alred.chang@westmedsupply.com', \
                     street='3445 North First Street', city='San Jose', state='CA', postal='95101', user_id = u1.id)
        session.add(c2);
        print ('Added Customer ' + str(c2))

        # flush to access sequence generated keys of earlier objects
        session.flush()

        tnum1 = TicketNumber()
        session.add(tnum1)
        session.flush()
        print ('ticketnumber id ' + str(tnum1.id))
     #   c2t1 = Ticket(tnumber='23513', ttype='Shipment Issue', body='Shipment 4233 on July 13 arrived late.', timestamp= datetime.now(), 
     #                   modified_timestamp=datetime.now(), customer_id=c2.id, firstname='Ellis', lastname='James', phone='480-425-1836', cemail='ellis@westmedsupply.com', user_id=u1.id, tstate='OPEN')
        c2t1 = Ticket(tnumber=tnum1.id, ttype='Shipment Issue', body='Shipment 4233 on July 13 arrived late.', timestamp= datetime.now(), \
                      modified_timestamp=datetime.now(), customer_id=c2.id, firstname='Ellis', lastname='James', phone='480-425-1836', \
                       cemail='ellis@westmedsupply.com', user_id=u1.id, tstate='OPEN', tpriority=3)
     
        session.add(c2t1);
        session.flush()

        tnum2 = TicketNumber()
        session.add(tnum2)
        session.flush()
        c2t2 = Ticket(tnumber=tnum2.id, ttype='Customer Inquiry', body='Customer inquired whether shipments can be held over the holidays. ', \
                      timestamp= datetime.now(),  modified_timestamp=datetime.now(), customer_id=c2.id,  firstname='Ellis', lastname='James', \
                      phone='480-425-1836', cemail='ellis@westmedsupply.com', user_id=u1.id, tstate='CLOSED', tpriority=2)
        session.add(c2t2);
        session.flush()

        # Customer 3
        c3 = Customer(cname='Rite Aid', firstname='Mary', lastname='Gonzalis', email='m.gonzalis@riteaid.com', street='130 South Detroit Street', city='Kenton', state='OH', postal='43326', user_id = u1.id)
        session.add(c3);
        print ('Added Customer ' + str(c3))
        session.flush()

        tnum3 = TicketNumber()
        session.add(tnum3)
        session.flush()
        c3t1 = Ticket(tnumber=tnum3.id, ttype='Shipment Issue', body='Customer states packages shipped with order #5644 were lightly damaged, no damage to product.', \
                      timestamp= datetime.now(), modified_timestamp=datetime.now(), customer_id=c3.id, firstname='Mary', lastname='Gonazlis', \
                      phone='480-425-4435', cemail='m.gonzalis@riteaid.com', user_id=u1.id, tstate='OPEN', tpriority=2)
        session.add(c3t1);
        session.flush()

        tnum4 = TicketNumber()
        session.add(tnum4)
        session.flush()
        c3t2 = Ticket(tnumber=tnum4.id, ttype='Customer Inquiry', body='Customer inquiry regarding availability of product XCL-226', timestamp= datetime.now(), \
                      modified_timestamp=datetime.now(), customer_id=c3.id, firstname='Mary', lastname='Gonazlis', phone='480-425-4435', \
                      cemail='m.gonzalis@riteaid.com', user_id=u1.id, tstate='CLOSED', tpriority=2)
        session.add(c3t2);
        session.flush()

        tnum5 = TicketNumber()
        session.add(tnum5)
        session.flush()
        c3t3 = Ticket(tnumber=tnum5.id, ttype='Billing Issue', body='Issue with July Invoice', timestamp= datetime.now(),  modified_timestamp=datetime.now(), \
                      customer_id=c3.id, firstname='Mary', lastname='Gonazlis', phone='480-425-4435', cemail='m.gonzalis@riteaid.com', \
                      user_id=u1.id, tstate='OPEN', tpriority=1)
        session.add(c3t3);
        session.flush()

        c3t2m1 = Comment(body='Confimred we can still obtain the Regular size collars for Product XCL-226, salesrep to fulfill with custom order.', timestamp=datetime.now(), ticket_id=c3t2.id, user_id=u1.id, email=u1.email)
        session.add(c3t2m1);
        session.flush()
        print ('Added Comment to ticket ')

        c3t3m1 = Comment(body='The $19.00 credit line item was a charge related to Order #442 which has a partical return.', timestamp=datetime.now(), ticket_id=c3t3.id, user_id=u1.id, email=u1.email)
        session.add(c3t3m1);
        session.flush()
        print ('Added Comment to ticket ')

        c3t3m2 = Comment(body='Customer called to indicate that the credit should be applied to the remaining balance.', timestamp=datetime.now(), ticket_id=c3t3.id, user_id=u1.id, email=u1.email)
        session.add(c3t3m2);
        session.flush()
        print ('Added Comment to ticket ')

        c3t3m3 = Comment(body='Note sent to Accounts Receivable Dept.', timestamp=datetime.now(), ticket_id=c3t3.id, user_id=u1.id, email=u1.email)
        session.add(c3t3m3);
        session.flush()
        print ('Added Comment to ticket ')

        c3t3f1 = Follower(timestamp=datetime.now(), ticket_id=c3t3.id, user_id=u1.id) 
        session.add(c3t3f1);
        print ('Added Follower f1')

        c3t3f2 = Follower(timestamp=datetime.now(), ticket_id=c3t2.id, user_id=u1.id) 
        session.add(c3t3f2);
        print ('Added Follower f2')

        session.commit()

        return 0, None

    except Exception as var:
     #   var = traceback.format_exc()
        print ("LoadDb Caught Unexpected error:", str(var))
        return -1, var

if __name__ == "__main__":
   # stuff to run when called by a command line vs import 
   main()
