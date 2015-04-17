
import sys, os, traceback
#sys.path.insert(1, os.path.join(sys.path[0], '../..'))
from app.mcexception import MCException
from werkzeug import check_password_hash
from werkzeug import generate_password_hash
from sqlalchemy.orm import synonym
from sqlalchemy import event, UniqueConstraint
from sqlalchemy import DDL, exc, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db import Base, session, isMemoryDb
from sqlalchemy.orm import relationship, backref

class User(Base):
    __tablename__ = 'user'

    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)

    uname = Column(String(64), unique=True)
    _password = Column('password', String(100))
    firstname = Column(String(16), nullable = True)
    lastname = Column(String(16), nullable = True)
    phone = Column(String(18),  nullable = True)
    email = Column(String(120), nullable = False)
    kinveyuser = Column(String(64))
    kinveypassword = Column(String(64))

    def __repr__(self):
        return '<User %r>' % (self.uname)


    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)

    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self.password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

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
        username = username.strip().lower()
        user = query(cls).filter(cls.uname==username).first()
        if user is None:
            return None, False
        if not user.is_active:
            return user, False
        return user, user.check_password(password)

    @classmethod
    def list(cls, filter_by=None):
        if(filter_by is not None):
            return  session.query(User).filter_by( **filter_by ).all()  # filter_by kwargs**
        else:
            return  session.query(User).all()

    @classmethod
    def detail(cls, pk):
        return session.query(User).filter_by(id=pk).first()


    @classmethod
    def create(cls, uname, password, firstname, lastname, phone, email, kinveyuser, kinveypassword):

        user = User()

        user.uname = uname

        if password:
            password = password.strip()
            user._password = generate_password_hash(password)

        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.email = email
        user.kinveyuser = kinveyuser
        user.kinveypassword = kinveypassword

        try:
          
            session.add(user)
            session.commit()

        except exc.IntegrityError:
            session.rollback()
            raise MCException("Integrity Error, user already exists")

        except exc.DataError:
            session.rollback()
            raise MCException("Data Error, invalid user data")

        return user






    @classmethod
    def update(cls, pk, uname, password, firstname, lastname, phone, email, kinveyuser, kinveypassword):
        try:
            user = session.query(User).filter_by(id=pk).one()
        
            user.uname = uname
            user._password = _set_password(password)
            user.firstname = firstname
            user.lastname = lastname
            user.phone = phone
            user.email = email
            user.kinveyuser = kinveyuser
            user.kinveypassword = kinveypassword
        
            session.add(user)
            session.commit()


        except exc.NoResultFound:
            session.rollback()
            raise MCException("No record found.")
              

        except exc.IntegrityError:
            session.rollback()
            raise MCException("Integrity Error, unable to update User")

        except exc.DataError:
            session.rollback()
            raise MCException("Data Error, invalid user data")

        return user
     


    @classmethod
    def delete(cls, pk):
        user = session.query(User).get(pk)
        
        if user is not None:
            try:
        # Skip if not found

               session.delete(user)
               session.commit()
               print('USER HAS BEEN DELETED')


            except exc.IntegrityError:
               var = traceback.format_exc()
               print("Unexpected Integrity Error " +  str(var))
               session.rollback()
               raise MCException("Integrity Error, unable to delete User")

        else:
            raise MCException("No such User Found")



  
class Customer(Base):
    __tablename__ = 'customer'
    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)
    cname = Column(String(64), index=True, unique=True)
    firstname = Column(String(16), nullable = True)
    lastname = Column(String(16), nullable = True)
    email = Column(String(120), index=True)
    street = Column(String(30), index=True, nullable = True)
    city  = Column(String(20), index=True, nullable = True)
    state  = Column(String(30), index=True, nullable = True)
    postal  = Column(String(10), index=True, nullable = True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    # should be removed, not need to list all customers in user rest return payload
    user = relationship('User', backref=backref('customers', lazy='dynamic'))


    @classmethod
    def list(cls, order_by='cname', filter_by=None):
        if(filter_by is not None):
            return  session.query(Customer).filter_by( **filter_by ).order_by(order_by).all()  # filter_by kwargs**
        else:
            return session.query(Customer).order_by( order_by ).all()
    

    @classmethod
    def detail(cls, pk):
        return session.query(Customer).filter_by(id=pk).first()

    @classmethod
    def create(cls, cname, firstname, lastname, email, street, city, state, postal, user_id):

        customer = Customer()

        customer.cname = cname
        customer.firstname = firstname
        customer.lastname = lastname
        customer.email = email
        customer.street = street
        customer.city = city
        customer.state = state    
        customer.postal = postal
        customer.user_id = user_id
  
        try:
            session.add(customer)
       
            session.commit()
 
        except exc.IntegrityError as var:
            session.rollback()
            print("Unexpected Exception " +  str(var))
            raise MCException("Integrity Error, customer already exists")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid customer data")


        return customer


    @classmethod
    def update(cls, pk,  cname, firstname, lastname, email, street, city, state, postal, user_id):
      
        try:
            customer = session.query(Customer).filter_by(id=pk).one() 
        
            customer.cname = cname
            customer.firstname = firstname
            customer.lastname = lastname
            customer.email = email
            customer.street = street
            customer.city = city
            customer.state = state    
            customer.postal = postal
            customer.user_id = user_id
          
            session.add(customer)
            session.commit()

        except exc.NoResultFound as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("No customer found to update.")
              

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, unable to update customer")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid customer data")

  

        return customer



    @classmethod
    def delete(cls, pk):
        customer = session.query(Customer).get(pk)
        
        if customer is not None:
        # Skip if not found
            try:
                session.delete(customer)
                session.commit()

            except exc.IntegrityError as var:
               print("Unexpected Integrity Error " +  str(var))
               session.rollback()
               raise MCException("Integrity Error, unable to delete Customer")

        else:
            raise MCException("No such Customer")


    @classmethod
    def search(cls, pattern):
        return  session.query(Customer).filter(Customer.cname.ilike(pattern)).all()
 

    def open_ticket_count(self):
        return session.query(Ticket).filter(Ticket.customer_id == self.id).filter(Ticket.tstate =='OPEN').count()


    def __repr__(self):
        return '<Customer %r>' % (self.cname)



class Ticket(Base):
    __tablename__ = 'ticket'
    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)

    #tnumber = Column(Integer, autoincrement = True)
    ticketnumber = relationship('TicketNumber', backref=backref('tickets', lazy='dynamic',cascade="all, delete-orphan" ))
    tnumber = Column(Integer, ForeignKey('ticketnumber.id'), nullable = False)
    ttype = Column(String(25))
    tpriority = Column(Integer)
    body = Column(String(140))
    timestamp = Column(DateTime)
    modified_timestamp = Column(DateTime)
    firstname = Column(String(16), nullable = True)
    lastname = Column(String(16), nullable = True)
    phone = Column(String(18),  nullable = True)
    cemail = Column(String(120), nullable = True)
    tstate = Column(String(16), nullable = True)
    
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable = False)
    customer = relationship('Customer', backref=backref('tickets', lazy='dynamic', cascade="all, delete-orphan"))

    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
   
    def hasFollower(self, user_id):

        id = None
      
        for follower in self.followers:
            if follower.user_id == user_id:
                id = follower.id
                break
        print('Follower ' + str(id))
        return id
       


    @classmethod
    def list(cls, order_by='tnumber', filter_by=None):
        print('In Model session is ' + str(session))
        if(filter_by is not None):
            return  session.query(Ticket).filter_by( **filter_by ).order_by(order_by).all()  # filter_by kwargs**
        else:
            return (session.query(Ticket).order_by( order_by ).all())
             
                

    @classmethod
    def detail(cls, pk):
        return session.query(Ticket).filter_by(id=pk).first()

    @classmethod
    def create(cls, ttype, tpriority, body, timestamp, modified_timestamp, firstname, lastname, phone, \
                cemail, tstate, customer_id, user_id):

        try:
            tnum = TicketNumber.create()
            session.add(tnum)
            session.flush()

            ticket = Ticket()

            ticket.tnumber = tnum.id
            ticket.ttype = ttype
            ticket.tpriority = tpriority
            ticket.body = body
            ticket.timestamp = timestamp    
            ticket.modified_timestamp = modified_timestamp
            ticket.firstname = firstname
            ticket.lastname = lastname
            ticket.phone = phone
            ticket.cemail = cemail       
            ticket.phone = phone
            ticket.customer_id = customer_id    
            ticket.user_id = user_id  
            session.add(ticket)
       
            session.commit()

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, ticket already defined")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid ticket data")


        return ticket


    @classmethod
    def update(cls, pk,  ticketnumber, ttype, tpriority, body, timestamp, modified_timestamp, firstname, lastname, phone, \
                cemail, tstate, customer_id, user_id):
        try:
            ticket = session.query(Ticket).filter_by(id=pk).one()
          
            ticket.ticketnumber = ticketnumber
            ticket.ttype = ttype
            ticket.tpriority = tpriority
            ticket.body = body
            ticket.timestamp = timestamp    
            ticket.modified_timestamp = modified_timestamp
            ticket.firstname = firstname
            ticket.lastname = lastname
            ticket.phone = phone
            ticket.cemail = cemail       
            ticket.phone = phone
            ticket.tstate = tstate      
            ticket.customer_id = customer_id    
            ticket.user_id = user_id  

            session.add(ticket)
            session.commit()

        except exc.NoResultFound as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("No ticket found to update.")
              

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, unable to update ticket")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid ticket data")

  

        return ticket


    @classmethod
    def updateModifiedTimestamp(cls, pk,  modified_timestamp):

        try:
            ticket = session.query(Ticket).filter_by(id=pk).one()
            ticket.modified_timestamp = modified_timestamp
            session.add(ticket)
            session.commit()

        except exc.NoResultFound as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("No record found.")
              

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, unable to update ticket modified timestamp")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid timestamp data")

  
        
        return ticket

    @classmethod
    def delete(cls, pk):
        ticket = session.query(Ticket).get(pk)
        
        if ticket is not None:
            tnumber = session.query(TicketNumber).get(ticket.tnumber)
        # Skip if not found
            try:
                print("Deleting ticketnumber " + str(tnumber))
               
                session.delete(ticket)
                session.delete(tnumber)
                session.commit()

            except exc.IntegrityError as var:
               print("Unexpected Integrity Error " +  str(var))
               session.rollback()
               raise MCException("Integrity Error, unable to delete Ticket")
        else:
            raise MCException("No Ticket found to delete")



    @classmethod
    def search(cls, pattern):
        return  session.query(Ticket).filter(Ticket.tnumber.ilike(pattern)).all()


    def __repr__(self):
        return '<Ticket %r>' % (self.body)



class TicketNumber(Base):
    __tablename__ = 'ticketnumber'
    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)
    @classmethod
    def create(cls):

        try:
            tnum = TicketNumber()

            session.add(tnum)
            session.commit()

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, TicketNumber already exists")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid TicketNumber data")

        return tnum;

if not isMemoryDb:
    event.listen(
       TicketNumber.__table__,
       "after_create",
       DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10000;")
    )

    
class Comment(Base):
    __tablename__ = 'comment'
   
    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    notification = Column(String(64))
    email = Column(String(60), nullable = True)
    
    ticket_id = Column(Integer, ForeignKey('ticket.id'), nullable = False)
    ticket = relationship('Ticket', backref=backref('comments', lazy='dynamic', cascade="all, delete-orphan"))

    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    user = relationship('User', backref=backref('comments', lazy='dynamic'))
       

    def __repr__(self):
        return '<Comment %r>' % (self.body)

    @classmethod
    def list(cls, order_by='timestamp', filter_by=None):
        if(filter_by is not None):
            return  session.query(Comment).filter_by( **filter_by ).order_by(order_by).all()  # filter_by kwargs**
        else:
            return session.query(Comment).order_by( order_by ).all()
    

    @classmethod
    def detail(cls, pk):
        comment = session.query(Comment).filter_by(id=pk).first()

        return comment

    @classmethod
    def create(cls, body, timestamp, notification, email, user_id, ticket_id):


        try:

            comment = Comment()

            comment.body = body
            comment.timestamp = timestamp
            comment.notification = notification
            comment.email = email
            comment.user_id = user_id
            comment.ticket_id = ticket_id
          
            session.add(comment)
            session.commit()


        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, comment already exists")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid comment data")

        # update modified date for ticket
        Ticket.updateModifiedTimestamp(ticket_id, datetime.now())


        return comment



    @classmethod
    def update(cls, pk, body, timestamp, notification, email, user_id, ticket_id):
        try:
            comment = session.query(Comment).filter_by(id=pk).one()

          
            comment.body = body
            comment.timestamp = timestamp
            comment.notification = notification
            comment.email = email
            comment.user_id = user_id
            comment.ticket_id = ticket_id

            session.add(comment)
            session.commit()

        except exc.NoResultFound as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("No record found.") 

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, unable to update Commment")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid comment data")

        return comment

    @classmethod
    def delete(cls, pk):
        comment = session.query(Comment).get(pk)
        
        if comment is not None:
            try:
        # Skip if not found
                session.delete(comment)
                session.commit()

            except exc.IntegrityError as var:
               print("Unexpected Integrity Error " +  str(var))
               session.rollback()
               raise MCException("Integrity Error, unable to delete Comment")
        else:
            raise MCException("No Comment Found to delete")


 
#class Contact(Model):
#    __tablename__ = 'contact'
#    __table_args__ = {'mysql_engine':'InnoDB'} 
#    id = Column(Integer, primary_key = True, autoincrement = True)
#    title = Column(String(5), nullable = True)
#    firstname = Column(String(32))
#    lastname = Column(String(32))
#    suffix = Column(String(32), nullable = True)
#    email = Column(String(60), nullable = True)

#    phone1 = Column(String(18),  nullable = True)
#    phone2 = Column(String(18),  nullable = True)
#    phone2 = Column(String(18),  nullable = True)

#    street = Column(String(30), index=True, nullable = True)
#    city  = Column(String(20), index=True, nullable = True)
#    state  = Column(String(30), index=True, nullable = True)
#    postal  = Column(String(10), index=True, nullable = True)
    
#    ticket_id = Column(Integer, ForeignKey('ticket.id'), nullable = True)
#    contacts = relationship('Ticket', backref=backref('ticket', lazy='dynamic'))

#    customer_id = Column(Integer, ForeignKey('customer.id'), nullable = True)
#    contacts = relationship('Customer', backref=backref('customer', lazy='dynamic'))


#    def __repr__(self):
#        return '<Contact %r>' % (self.body)

#    @classmethod
#    def list(cls, order_by='lastname', filter_by=None):
#        if(filter_by is not None):
#            return  session.query(Contact).filter_by( **filter_by ).order_by(order_by).all()  # filter_by kwargs**
#        else:
#            return session.query(Contact).order_by( order_by ).all()
    

#    @classmethod
#    def detail(cls, pk):
#        contact = session.query(Contact).filter_by(id=pk).first()

#        return comment

#    @classmethod
#    def create(cls, title, firstname, lastname, suffix, email, phone1, phone2, phone3, street, city, state, postal):

#        contact = Contact()

#        contact.title = title
#        contact.firstname = firstname
#        contact.lastname = lastname
#        contact.suffix = suffix
#        contact.email = email
#        contact.phone1 = phone1
#        contact.phone2 = phone2
#        contact.phone3 = phone3
#        contact.street = street
#        contact.city = city
#        contact.state = state
#        contact.postal = postal


#        try:
          
#            session.add(contact)
#            session.commit()

#        except exc.IntegrityError:
#            session.rollback()
#            raise

#        except exc.DataError:
#            session.rollback()
#            raise

#        return contact




class Follower(Base):
    __tablename__ = 'follower'
    if not isMemoryDb:
        __table_args__ = {'mysql_engine':'InnoDB'} 
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)
    timestamp = Column(DateTime)
    modified_timestamp = Column(DateTime)
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    ticket_id = Column(Integer, ForeignKey('ticket.id'), nullable = False)
    ticket = relationship('Ticket', backref=backref('followers', lazy='dynamic', cascade="all, delete-orphan"))

    def __repr__(self):
        return '<Follower %r>' % (self.user_id)

    @classmethod
    def list(cls, filter_by=None):
        if(filter_by is not None):
            return  session.query(Follower).filter_by( **filter_by ).all()  # filter_by kwargs**
        else:
            return  session.query(Follower).all()


    @classmethod
    def detail(cls, pk):
        return session.query(Follower).filter_by(id=pk).first()

    @classmethod
    def create(cls, timestamp, modified_timestamp, user_id, ticket_id):

        try:
            follower = Follower()

            follower.timestamp = timestamp
            follower.modified_timestamp = modified_timestamp
            follower.user_id = user_id
            follower.ticket_id = ticket_id

            session.add(follower)
       
            session.commit()

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, Follower already exists")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid Follower data")


        return follower


    @classmethod
    def update(cls, pk, timestamp, modified_timestamp, user_id, ticket_id):
   
        try:
         #   follower = session.query(Follower).filter_by(id=pk).one()
            follower = session.query(Follower).get(pk)

            follower.timestamp = timestamp
            follower.modified_timestamp = modified_timestamp
            follower.user_id = user_id
            follower.ticket_id = ticket_id

            session.add(follower)
            session.commit()

        except exc.NoResultFound as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("No record found.") 

        except exc.IntegrityError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Integrity Error, unable to update Follower")

        except exc.DataError as var:
            print("Unexpected Exception " +  str(var))
            session.rollback()
            raise MCException("Data Error, invalid follower data")

        return follower

    @classmethod
    def delete(cls, pk):
        follower = session.query(Follower).get(pk)
        
        if follower is not None:
        # Skip if not found
            try:
                session.delete(follower)
                session.commit()

            except exc.IntegrityError as var:
               print("Unexpected Integrity Error " +  str(var))
               session.rollback()
               raise MCException("Integrity Error, unable to delete Follower")
        else:
            raise MCException("No such Follower")





class States(Base):  # pylint: disable-msg=R0903
    """
    Holds States names

    """
    __tablename__ = "states"

    if not isMemoryDb:
        id = Column(Integer, primary_key = True, autoincrement = True)
    else:
        id = Column(Integer, primary_key = True)
    sname = Column(String(30), unique=True)
    abbr = Column(String(2), unique=True)

    def __init__(self, sname, abbr):
        """
        Used to create a State object in the python server scope
        """
        self.sname = sname
        self.abbr = abbr

