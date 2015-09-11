
import uuid, json
from datetime import datetime
from app import memorystore

class User(object):
  
    def __init__(self, uname, password, firstname, lastname, phone, email, kinveyuser, kinveypassword):
        self.id = str(uuid.uuid4())
        self.uname = uname
        self._password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
        self.kinveyuser = kinveyuser
        self.kinveypassword = kinveypassword
        self.customers = list()

    def __repr__(self):
        return '<User %r>' % (self.uname)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        pass

    def check_password(self, password):
        pass

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @classmethod
    def authenticate(cls, query, username, password):
        pass

    @staticmethod
    def list(filter_by=None):
        return list(memorystore.users.values())

    @classmethod
    def detail(cls, pk):
        return db.session.query(User).filter_by(id=pk).first()

    @staticmethod
    def create(uname, password, firstname, lastname, email,  phone="", kinveyuser="", kinveypassword=""):
        user = User(uname, password, firstname, lastname, phone, email, kinveyuser, kinveypassword)
        memorystore.users[user.id] = user
        print('Memorystore user' + str(memorystore.users))
        return user

    @classmethod
    def update(cls, pk, uname, password, firstname, lastname, phone, email, kinveyuser, kinveypassword): 
        return user
     
    @classmethod
    def delete(cls, pk):
        print('NOT IMPLEMENTED')
        pass
      

  
class Customer(object):
   
    def __init__(self, cname, firstname, lastname, email, street, city, state, postal, user_id):
        self.id = str(uuid.uuid4())
        self.cname = cname
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.street = street
        self.city = city
        self.state = state
        self.postal = postal
        self.user_id = user_id
        self.tickets = list()


    @property
    def user(self):
        return memorystore.users.get(self.user_id)

   
    @classmethod
    def list(cls, order_by='cname', filter_by=None):
        return list(memorystore.customers.values())
    
  
    @classmethod
    def detail(cls, pk):
        return memorystore.customers.get(pk)

   
    @classmethod
    def create(cls, cname, firstname, lastname, email, street, city, state, postal, user_id):
        cust = Customer(cname, firstname, lastname, email, street, city, state, postal, user_id)
      
        memorystore.customers[cust.id] = cust

        print('memorystore customers'  + str(memorystore.customers))
        #memorystore.users[str(user_id)].customers.append(cust)
        print('create created customer ' + cust.id)
        return cust

    @classmethod
    def update(cls, pk,  cname, firstname, lastname, email, street, city, state, postal, user_id):
        return customer

    @classmethod
    def delete(cls, pk):
        customer = db.session.query(Customer).get(pk)
        

    @classmethod
    def search(cls, pattern):
        return  db.session.query(Customer).filter(Customer.cname.ilike(pattern)).all()
 

    def open_ticket_count(self):
    #    return db.session.query(Ticket).filter(Ticket.customer_id == self.id).filter(Ticket.tstate =='OPEN').count()
         return 0

    def __repr__(self):
        return '<Customer id=%r, cname=%r, firstname=%r, lastname=%r, email=%r, street=%r, city=%r \
                state=%r, postal=%r, user_id=%r, tickets=%r >' % \
                (self.id, self.cname, self.firstname, self.lastname, self.email, self.street, self.city, \
                 self.state, self.postal, self.user_id, str(self.tickets))
        



class Ticket(object):

    def __init__(self, ttype, tpriority, body, firstname, \
                 lastname, phone, cemail, tstate, comments, followers, customer_id, user_id, timestamp):
        self.id = str(uuid.uuid4())
        self.tnumber = TicketNumber.next()
        self.ttype = ttype
        self.tpriority = tpriority
        self.body = body
        self.timestamp = timestamp
        self.modified_timestamp = self.timestamp
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.cemail = cemail
        self.tstate = tstate
        self.comments = comments
        self.followers = followers
        self.user_id = user_id
        self.customer_id = customer_id


    
    @property
    def customer(self):
        return memorystore.customers[str(self.customer_id)]


    @classmethod
    def list(cls, order_by='tnumber', filter_by=None):
        return list(memorystore.tickets.values())

    @classmethod
    def detail(cls, pk):
        return memorystore.tickets.get(pk)

 
    @classmethod
    def create(cls, ttype, tpriority, body, firstname, lastname, phone, cemail, tstate, customer_id, user_id, timestamp = None):
        followers = list()
        comments = list()
        if timestamp == None:

            ticket = Ticket( ttype=ttype, tpriority=tpriority, body=body, firstname=firstname, lastname=lastname, \
                             phone=phone, cemail=cemail, tstate=tstate, comments=comments, followers=followers, \
                             customer_id=customer_id, user_id=user_id, timestamp=datetime.now())
        else:
            ticket = Ticket( ttype=ttype, tpriority=tpriority, body=body,  firstname=firstname, lastname=lastname, \
                             phone=phone, cemail=cemail, tstate=tstate, comments=comments, followers=followers, \
                             customer_id=customer_id, user_id=user_id, timestamp=timestamp)
       
        memorystore.tickets[ticket.id] = ticket
        memorystore.customers[customer_id].tickets.append(ticket)
        print('Create created ticket ' + ticket.id)
        return ticket

    @classmethod
    def update(cls, pk,  tnumber, ttype, tpriority, body, timestamp, modified_timestamp, firstname, lastname, phone, \
                cemail, tstate, customer_id, user_id):
        return ticket

    @classmethod
    def updateModifiedTimestamp(cls, pk,  modified_timestamp):
        return ticket

    @classmethod
    def delete(cls, pk):
        pass
       
    @classmethod
    def search(cls, pattern):
        return  db.session.query(Ticket).filter(Ticket.tnumber.ilike(pattern)).all()

    def hasFollower(self, user_id):

        id = None
      
        for follower in self.followers:
            if follower.user_id == user_id:
                id = follower.id
                break
        print('Follower ' + str(id))
        return id
        

    def __repr__(self):
        return '<Ticket pk=%r, tnumber=%r, body=%r, timestamp=%r, modified_timestamp=%r, firstname=%r, lastname=%r \
                phone=%r, cemail=%r, tstate=%r, customer_id=%r, user_id=%r >' % \
                (self.id, self.tnumber, self.body, self.timestamp, self.modified_timestamp, self.firstname, self.lastname, \
                 self.phone, self.cemail, self.tstate, self.customer_id, self.user_id) 
        


class TicketNumber(object):
 
    _id = 10000

    @staticmethod
    def next():
        TicketNumber._id = TicketNumber._id + 1
        return TicketNumber._id 


    
class Comment(object):
   
    def __init__(id, body, timestamp, notification, email):
        self.id = id
        self.body = body
        self.timestamp = timestamp
        self.notification = notification
        self.email = email
     
    def __repr__(self):
        return '<Comment %r>' % (self.body)

    @classmethod
    def list(cls, order_by='timestamp', filter_by=None):
        pass

    @classmethod
    def detail(cls, pk):
        return comment

    @classmethod
    def create(cls, body, timestamp, notification, email, user_id, ticket_id):
        return comment

    @classmethod
    def update(cls, pk, body, timestamp, notification, email, user_id, ticket_id):
        return comment

 
class Follower(object):
  
    def __init__(self, id, timestamp, modified_timestamp, user, ticket):
        self.id = id
        self.timestamp = timestamp
        self.modified_timestamp = modified_timestamp
        self.user = user
        self.ticket = ticket
   
    def __repr__(self):
        return '<Follower %r>' % (self.user_id)

    @classmethod
    def list(cls):
        return  db.session.query(Follower).all()

    @classmethod
    def detail(cls, pk):
        return db.session.query(Follower).filter_by(id=pk).first()

    @classmethod
    def create(cls, timestamp, modified_timestamp, user_id, ticket_id):
        return follower

    @classmethod
    def update(cls, pk, timestamp, modified_timestamp, user_id, ticket_id):
        return follower

    @classmethod
    def delete(cls, pk):
        pass
       



