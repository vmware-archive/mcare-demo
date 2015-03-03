from flask import request, abort, jsonify, render_template, redirect, url_for, flash
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
from flask.ext.wtf import Form
from flask.ext.moment import Moment
from datetime import datetime
from sqlalchemy import exc
from .forms import NameForm, LoginForm, TicketForm, UserForm, CommentForm
from .forms import CustomerForm, SearchForm
from app import appl
from app.mcexception import MCException
from config import config
import base64
from app import loadDb
from app.db import session
from app.storage.db.model import *
   
moment = Moment(appl)

# Use Flask-Login to  track current user in Flask's session.
login_manager = LoginManager()
login_manager.setup_app(appl)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  """Flask-Login hook to load a User instance from ID. """
  return session.query(User).get(user_id)
   

@login_manager.request_loader
def load_user_from_request(request):

    # first, try to login using the api_key url arg
    #api_key = request.args.get('api_key')
    #if api_key:
    #    user = User.query.filter_by(api_key=api_key).first()
    #    if user:
    #        return user

    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
       
        api_key = api_key.replace('Basic ', '', 1)
    
        try:
            api_key = base64.b64decode(api_key)
            print('decoded api_key ' + str(api_key))
        except TypeError:
            print('base64 decode failed')
            pass
        fldarray = str(api_key).split(":")
        username = fldarray[0]
        username = username[2:]
     
        password = fldarray[1]
        password = password[:-1]
      
        user =   User.authenticate(session.query, username, password)
        #user = User.query.filter_by(email=username).first()
      
        if user[0] is not None and user[1]:
            #user[0].check
            print('User Login Successfull ' + user[0].email)
            return user[0]
        else:
            print('User Login Not Successfull')

    # finally, return None if both methods did not login the user
    return None

@appl.errorhandler(403)
def page_not_found(e):
    print('403 Error ' + str(e))
    return render_template('403.html'), 403

@appl.errorhandler(404)
def page_not_found(e):
    print('404 Error ' + str(e))
    return render_template('404.html'), 404


@appl.errorhandler(500)
def internal_server_error(e):
    print('500 Error ' + str(e))
    return render_template('500.html'), 500

@appl.route('/', methods=['GET'])
def main():
   
    # must call .all() or a unmaterialized Query object is returned
    #tickets = (session.query(Ticket).filter_by(tstate = 'OPEN').all())
    kwargs = {'tstate': 'OPEN'}
    tickets = Ticket.list(filter_by = kwargs)
    print('HERE TICKETS=' + str(tickets))
    # Provide HTML list of all custo
    # Query: Get all customers

    if current_user is None: 
       print("Current User is None")
    else:
       if current_user.is_anonymous(): 
          print("Current User is Anonymous " + str(type(current_user)))
       if current_user.is_authenticated(): 
          print("Current User " + current_user.uname + " is Authenticated")
    print('TICKETs ' + str(tickets))
    print('Ticket Customer ' + str(tickets[0].customer))
    return render_template('index.html', tickets=tickets)


@appl.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('customer_list'))

    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        uname = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = \
            User.authenticate(session.query, uname, password)
        if authenticated:
            login_user(user, remember='y')
            
            return redirect(url_for('customer_list'))
        else:
            print('Error Authenticating ' + form.username.data )
            flash('Incorrect username or password. Try again.')
            return redirect(url_for('login'))
    return render_template('user/login.html', form=form, error=error)


@appl.route('/loginauth')
@login_required
def test():
  return 'OK'

@appl.route('/logout/')
def logout():
    logout_user()
  
    return redirect(url_for('login'))


@appl.route('/loadDb', methods=['GET'])
def loaddb():
    flash('Starting')
    rc, var = loadDb.main()
    if (rc == 0):
         flash('Database Loaded')
    else:
         flash('Database Load Failed:  ' + str(var))
    return redirect(url_for('admin'))
	

@appl.route('/admin', methods=['GET', 'POST'])
def admin():
    dburl = appl.config['SQLALCHEMY_DATABASE_URI']
    return render_template('admin.html', dburl = dburl)


@appl.route('/register/', methods=['GET', 'POST'])
def user_create():
    """Provide HTML for to create a new user"""
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
      
        form.populate_obj(user)
   
        try:
          session.add(user)
          session.commit()

        except MCException as e:
                 session.rollback()
                 flash(e.value)
                 return render_template('user/edit.html', form=form) 
      
        # Success. Send user back the login
        return redirect(url_for('login'))
    else:
        print('Form is not valid ' + str(len(form.errors)) + ' ' + str(form.errors))
    # Either first load or validation error at this point
    return render_template('user/edit.html', form=form)



@appl.route('/user/edit', methods=['GET', 'POST'])
def user_edit():
    key = request.args.get('user_id')
    if(key != None):
       user = (session.query(User).filter_by(id=key).first())
       if user is None:
           abort(404)
       print('returned user ' + str(user.id ))
 #      users = (session.query(User).filter_by(id = user.id).all())
    else:
       abort(404)

    form = UserForm(request.form, user)
    
    # remove password field for edit, otherwise validation of required
    del form.password

    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        session.commit()
        # Success, Send the user back to the detail view
        print('Updated User')
        return redirect(url_for('user_list', user_id=user.id))

    if not form.validate():
        print("Form is not valid")
        print(str(form.errors))
 
    return render_template('user/edit.html', form=form, user=user)



@appl.route('/users/', methods=['GET', 'POST'])
def user_list():
   
    # Provide HTML list of all users
   
    users = (session.query(User).order_by(User.uname).all())
    print('returned users ' + str(len(users) ))
    return render_template('user/users.html', users=users)
   


@appl.route('/customers/', methods=['GET', 'POST'])
def customer_list():
   
    # Provide HTML list of all customers
    # Query: Get all customers
    key = request.args.get('key')
    if(key == None):
       print ('ckey is None')
       customers = Customer.list()
       #customers = (session.query(Customer).order_by(Customer.cname).all())
    else:
       pattern = "%" + key + "%"
       print("Pattern " + pattern)

       #customers = (session.query(Customer).filter(Customer.cname.ilike(pattern)).all())
       customers = Customer.search(pattern)

    return render_template('customer/customers.html', customers=customers)

@appl.route('/customer/create', methods=['GET', 'POST'])
@login_required
def customer_create():
    """Provide HTML for to create a new customer"""
    form = CustomerForm(request.form)
    form.state.choices = [(g.abbr, g.sname) for g in States.query.order_by('sname')]
    
    if request.method == 'POST' and form.validate():
      #  customer = Customer()
      
       # form.populate_obj(customer)

       
       # customer.user_id = current_user.id

        try:
            Customer.create( form.cname.data, form.firstname.data, form.lastname.data, form.email.data, form.street.data, \
                             form.city.data, form.state.data, form.postal.data, current_user.id)
          #  session.add(customer)
       
          #  session.commit()

        except MCException as e:
                 flash(e.value)
                 return render_template('customer/edit.html', form=form)

        # Success. Send user back the new customer
        return redirect(url_for('customer_list'))
    else:
        print('Form is not valid ' + str(len(form.errors)) + ' ' +str(form.errors))
    # Either first load or validation error at this point
    return render_template('customer/edit.html', form=form)




@appl.route('/customer/', methods=['GET', 'POST'])
def customer():
    key = request.args.get('customer_id')
    if(key != None):
       #customer = (session.query(Customer).filter_by(id=key).first())
       customer = Customer.detail(key)
       print('CUSTOMER ' + key + ' ' +  str(customer))
       if customer is None:
             abort(404)
       else:
           print('returned customer ' + str(customer.id ))
           #tickets = (session.query(Ticket).filter_by(customer_id = customer.id).all())
           kwargs = {'customer_id': customer.id}
           tickets = customer.tickets
           #tickets = Ticket.list(order_by = 'ticket.id', filter_by = kwargs)   // THIS SHOULD BE CUSTOMER.getTickets
           #if (len(tickets) == 0):
           #    tickets = list()
           #tickets = Ticket.list(filter_by = "customer_id = " + str(customer.id))
    else:
        abort(404)

 
    return render_template('customer/detail.html', customer=customer, tickets=tickets)


@appl.route('/customer/edit/', methods=['GET', 'POST'])
@login_required
def customer_edit():
    key = request.args.get('customer_id')
    if(key != None):
       #customer = (session.query(Customer).filter_by(id=key).first())
       customer = Customer.detail(key)
       if customer is None:
           abort(404)
       print('returned customer ' + str(customer.id ))

    form = CustomerForm(request.form, customer)
    form.state.choices = [(g.abbr, g.sname) for g in States.query.order_by('sname')]

    if request.method == 'POST' and form.validate():

        form.populate_obj(customer)
        try:
           Customer.update(pk=customer.id, cname=form.cname.data, firstname=form.firstname.data, lastname=form.lastname.data, \
                           email=form.email.data, street=form.street.data, city=form.city.data, state=form.state.data, \
                           postal=form.postal.data, user_id=customer.user_id)
          # session.commit()

        except MCException as e:
                 flash(e.value)
                 return render_template('customer/edit.html', customer = customer, form=form )

        # Success, Send the user back to the detail view
        print('Updated Customer')
        return redirect(url_for('customer', customer_id=customer.id))

    return render_template('customer/edit.html', customer=customer, form=form)
    
   

@appl.route('/customer/<int:customer_id>/delete/', methods=['DELETE'])
@login_required
def customer_delete(customer_id):
    """ Delete record using HTTP Delete, response with JSON """
    print('Customer ID for delete is ' + str(customer_id))
    #customer = session.query(Customer).get(customer_id)
    customer = Customer.detail(customer_id)
    if customer is None:
        # Abort with Not Found, but with simple JSON Response
        response = jsonify({'status': 'Not Found'})
        return response

    if customer.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})
        return response

   # session.delete(customer)
   # session.commit()
    Customer.delete(customer_id)

    return jsonify({'status': 'ok'})


@appl.route('/ticket/', methods=['GET', 'POST'])
def ticket():
   
    key = request.args.get('ticket_id')
    if(key != None):
       #ticket = (session.query(Ticket).filter_by(id=key).first())
       ticket = Ticket.detail(key)
       if ticket is None:
             abort(404)
       else:
           #comments = (session.query(Comment).filter_by(ticket_id = ticket.id).all())
           kwargs = {'ticket_id': ticket.id}
           comments = Comment.list(filter_by = kwargs)   
           if(len(comments) == 0):
               comments = list()

           if current_user.is_authenticated(): 
               follower_id = ticket.hasFollower(current_user.id)
               print('see follower' + str(follower_id))
           else:
               follower_id = None
           
    else:
       ticket = list()
       comments = list()
 
    return render_template('ticket/detail.html',  ticket=ticket, comments=comments, follower_id=follower_id)



@appl.route('/tickets/', methods=['GET', 'POST'])
def ticket_list():
    key = request.args.get('skey')
    if(key == None):
       # all() returns a list
       #tickets = (session.query(Ticket).order_by(Ticket.tnumber).all())
       tickets = Ticket.list(order_by='ticket.tnumber')
    else:
       pattern = "%" + skey + "%"
       print("Search Pattern " + pattern)
       # must call .all() or a unmaterialized Query object is returned
       tickets = Tickets.search(pattern)
      #tickets = (session.query(Ticket).filter(Ticket.tnumber.ilike(pattern)).all())
   
    # Provide HTML list of all custo
    # Query: Get all customers
    
    print('returned tickets ' + str(len(tickets)))
  
    return render_template('ticket/tickets.html', tickets=tickets)



@appl.route('/ticket/create', methods=['GET', 'POST'])
@login_required
def ticket_create():
    """Provide HTML for to create a new ticket"""
    customer_id = request.args.get('customer_id')
    form = TicketForm(request.form)
    form.ttype.choices = config['development'].TICKET_TYPES
    form.tpriority.choices = config['development'].TICKET_PRIORITIES
    del form.tstate
    if request.method == 'POST' and form.validate():

        
      try:

        #tnum = TicketNumber.create()

      #  ticket = Ticket()

     
        Ticket.create(ttype=form.ttype.data, tpriority=form.tpriority.data, body=form.body.data, timestamp=datetime.now(), \
                      modified_timestamp = datetime.now(), firstname=form.firstname.data, lastname=form.lastname.data, \
                      phone=form.phone.data, cemail=form.cemail.data, tstate = 'OPEN', customer_id = customer_id, \
                      user_id=current_user.id)


        # Success. Send user back the new customer
        return redirect(url_for('customer', customer_id=customer_id))

    
      except MCException as e:
                 flash(e.value)
                 return render_template('ticket/edit.html', show_edit=False, form=form, customer_id = customer_id)
                 
       
    else:
        print('Form is not valid ' + str(len(form.errors)) + ' ' +str(form.errors))
    # Either first load or validation error at this point
    return render_template('ticket/edit.html', show_edit=False, form=form, customer_id = customer_id)


@appl.route('/ticket/edit/', methods=['GET', 'POST'])
@login_required
def ticket_edit():
    key = request.args.get('ticket_id')
    if(key != None):
       #ticket = (session.query(Ticket).filter_by(id=key).first())
    
       ticket = Ticket.detail(key)
       if ticket is None:
           abort(404)
       print('returned ticket ' + str(ticket.id ))

    form = TicketForm(request.form, ticket)
    form.ttype.choices = config['development'].TICKET_TYPES
    form.tpriority.choices = config['development'].TICKET_PRIORITIES
  
    if request.method == 'POST' and form.validate():

        Ticket.update(pk=ticket.id, ttype=form.ttype.data, tpriority=form.tpriority.data, body=form.body.data, timestamp=ticket.timestamp, \
                      modified_timestamp = datetime.now(), firstname=form.firstname.data, lastname=form.lastname.data, \
                      phone=form.phone.data, cemail=form.cemail.data, tstate = form.tstate.data, customer_id = ticket.customer_id, \
                      user_id=ticket.user_id, ticketnumber=ticket.ticketnumber)

       # form.populate_obj(ticket)
       # session.commit()
        # Success, Send the user back to the detail view
        return redirect(url_for('ticket', ticket_id=ticket.id))

    return render_template('ticket/edit.html', form=form, tnumber=ticket.tnumber, ticket_id=ticket.id)
    
   

@appl.route('/ticket/<int:ticket_id>/delete/', methods=['DELETE'])
@login_required
def ticket_delete(ticket_id):
    print('Ticket ID for delete is ' + str(ticket_id))
    #ticket = session.query(Ticket).get(ticket_id)
    ticket = Ticket.detail(ticket_id)
    if ticket is None:
        # Abort with Not Found, but with simple JSON Response
        response = jsonify({'status': 'Not Found'})
     
        return response

    if ticket.customer.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})

        return response

    Ticket.delete(ticket_id)
    #session.delete(ticket)
    #session.commit()
    return jsonify({'status': 'ok'})


@appl.route('/comment/create', methods=['GET', 'POST'])
@login_required
def comment_create():
    """Provide HTML for to create a new ticket"""
    ticket_id = request.args.get('ticket_id')
    form = CommentForm(request.form)
    if request.method == 'POST' and form.validate():

        try:
  
            Comment.create(body=form.body.data, timestamp=datetime.now(), email=form.email.data, notification="", \
                           user_id = current_user.id, ticket_id=ticket_id)

             # Success. Send user back the new customer
            return redirect(url_for('ticket', ticket_id=ticket_id))

        except MCException as e:
                 flash(e.value)
                 return render_template('comment/edit.html', form=form, ticket_id = ticket_id)

       
    else:
        print('Form is not valid ' + str(len(form.errors)) + ' ' +str(form.errors))
    # Either first load or validation error at this point
    return render_template('comment/edit.html', form=form, ticket_id = ticket_id)


@appl.route('/comment/edit/', methods=['GET', 'POST'])
@login_required
def comment_edit():
    key = request.args.get('comment_id')
    if(key != None):
       #comment = (session.query(Comment).filter_by(id=key).first())
       comment = Comment.detail(key)
       if comment is None:
           abort(404)
       print('returned comment ' + str(comment.id ))

    form = CommentForm(request.form, comment)

   
    if request.method == 'POST' and form.validate():
        
        try:
            Comment.update(pk=comment.id, body=form.body.data, timestamp=comment.timestamp, notification="",
                       email=form.email.data, user_id=comment.user_id, ticket_id=comment.ticket_id)

        except MCException as e:
                 flash(e.value)
                 return render_template('comment/edit.html', form=form, comment_id=comment.id, ticket_id = comment.ticket_id)
  
      #  form.populate_obj(comment)
      #  session.commit()
        # Success, Send the user back to the detail view
        return redirect(url_for('ticket', ticket_id=comment.ticket_id))
    print('FOO ' + str(comment.ticket_id))
    return render_template('comment/edit.html', form=form, comment_id=comment.id, ticket_id = comment.ticket_id)
    

@appl.route('/comment/<int:comment_id>/delete/', methods=['DELETE'])
@login_required
def comment_delete(comment_id):
    """ Delete record using HTTP Delete, response with JSON """
    print('Comment ID for delete is ' + str(comment_id))
    #comment = session.query(Comment).get(comment_id)
    comment = Comment.detail(comment_id)
    if comment is None:
        # Abort with Not Found, but with simple JSON Response
        response = jsonify({'status': 'Not Found'})
     
        return response

    if comment.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Forbidden'})
       
        return response

    Comment.delete(comment_id)
    #session.delete(comment)
    #session.commit()
    return jsonify({'status': 'ok'})


@appl.route('/followers/', methods=['GET', 'POST'])
def follower_list():

    followers = Follower.list()
    
    print('returned followers ' + str(len(followers)))
  
    return render_template('follower/followers.html', followers=followers)


@appl.route('/follower/', methods=['GET', 'POST'])
def follower_create():

    """Provide HTML for to create a new follower"""
    ticket_id = request.args.get('ticket_id')

    try:  
         
          Follower.create( timestamp=datetime.now(), modified_timestamp=datetime.now(),  \
                           user_id = current_user.id, ticket_id=ticket_id)
          flash('Now Following Ticket')

    except MCException as e:
          flash(e.value)
         

    return redirect(url_for('ticket', ticket_id=ticket_id))
  


@appl.route('/follower/<int:id>/delete/', methods=['DELETE'])
@login_required
def follower_delete(id):
 
   
    follower = Follower.detail(id)
    if follower is None:
        # Abort with Not Found, but with simple JSON Response
        response = jsonify({'status': 'Follower Not Found'})
        # return 200, javascrip delete function will deal with errors
        #response.status_code = 404
        return response

    if follower.user_id != current_user.id:
        # Abort with simple response indicating forbidden.
        response = jsonify({'status': 'Delete Forbidden'})
        return response

    Follower.delete(id)
  

    return jsonify({'status': 'ok'})


@appl.route('/search/', methods=['GET'])
def search():
    #form = SearchForm(request.form)
  
    key = "None"
    if request.method == 'GET':
    
        # post    myvar = request.form["myvar"]
        # get     myvar = request.args.get("myvar")
        ckey = request.args.get('ckey')
        tkey = request.args.get('tkey')
    
       
        if(ckey != ''):
           return redirect(url_for('customer_list', key=ckey))


        if(tkey != ''):
              kwargs = {'tnumber': tkey}
              tickets = Ticket.list(order_by = 'ticket.id', filter_by = kwargs)
              return render_template('ticket/tickets.html', tickets=tickets)
    
    return redirect(url_for('main'))
  


