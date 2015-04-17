from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from . import appl 
from datetime import datetime
from config import config
from flask import request, jsonify, abort, make_response
from app.mcexception import MCException
import json

from app.storage.db.model import Comment, Follower, User, Ticket, Customer


class CustomerResource():
   


    @appl.route('/api/v1.0/customers', methods=['GET'])
    def customer_list_json():

        querystring = request.args.get('q')
        if (querystring is not None):
            querymap = json.loads(querystring)
            customers = Customer.list(filter_by=querymap)
        else:
            customers = Customer.list()

           # No Such Customer
        if customers is None:
            value = dict()
            return jsonify({'customers': value})

        customerList = list()
        for customer in customers:
            customerList.append( CustomerResource.customer_json(customer))
    
        return jsonify( {'customers': customerList} )
      

     

     


    @appl.route('/api/v1.0/customers/<int:pk>', methods=['GET'])
    def customer_detail_json(pk):

        customer = Customer.detail(pk)

        # No Such Customer
        if customer is None:
            return make_response(jsonify({'error': 'Not found'}), 404)

        return jsonify({'customer': CustomerResource.customer_json(customer)})

    
    @appl.route('/api/v1.0/customers/<int:cpk>/tickets/<int:tpk>', methods=['GET'])
    def customer_ticket_json(cpk, tpk):

        customer = Customer.detail(cpk)

        # No Such Customer
        if customer is None:
            return make_response(jsonify({'error': 'Customer Not found'}), 404)

        ticket = Ticket.detail(tpk)
        if ticket is None:
            return make_response(jsonify({'error': 'Ticket Not found'}), 404)

        return jsonify({'ticket': TicketResource.ticket_json(ticket)})



    @appl.route('/api/v1.0/customers', methods=['POST'])
    def customer_create_json():
        
        if not request.json or not 'cname' in request.json:
            abort(400)

        try:
           customer = Customer.create(request.json.get('cname'), request.json.get('firstname'), request.json.get('lastname'), \
                                request.json.get('email') , request.json.get('street') , request.json.get('city'), \
                                request.json.get('state'), request.json.get('postal'), request.json.get('user_id') ) 

        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

       
        return jsonify({'customer': CustomerResource.customer_json(customer)}), 201


    @appl.route('/api/v1.0/customers/<int:pk>', methods=['PUT'])
    def customer_update_json(pk):

        if not request.json or not 'cname' in request.json:
            abort(400)

        try:
            customer = Customer.update(pk, request.json.get('cname'), request.json.get('firstname'), request.json.get('lastname'), \
                                request.json.get('email') , request.json.get('street') , request.json.get('city'), \
                                request.json.get('state'), request.json.get('postal'), request.json.get('user_id') ) 
     
        
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

      
        return jsonify({'customer':CustomerResource.customer_json(customer)})



    @appl.route('/api/v1.0/customers/<int:pk>', methods=['DELETE'])
    def customer_delete_json(pk):

       Customer.delete(pk)
       return jsonify({'result': True})

    @classmethod
    def customer_json(cls, customer):


        inner_user = { 
            'id':customer.user.id,
            'uname':customer.user.uname,
            'firstname':customer.user.firstname,
            'lastname': customer.user.lastname,
            'phone': customer.user.phone,
            'email':customer.user.email,
            'kinveyuser':customer.user.kinveyuser,
            'kinveypassword': customer.user.kinveypassword,
            }

        inner_tickets = list()

        for ticket in customer.tickets:  
                inner_tickets.append( {
                'id': ticket.id,
                'tnumber': ticket.ticketnumber.id,
                'ttype': ticket.ttype,
                'tpriority': ticket.tpriority,
                'body': ticket.body,
                'timestamp': ticket.timestamp,
                'modified_timestamp': ticket.modified_timestamp,
                'firstname': ticket.firstname,
                'lastname': ticket.lastname,
                'phone': ticket.phone,
                'cemail': ticket.cemail,
                'tstate':  ticket.tstate,
                'customer_id':  ticket.customer_id,
                'user_id': ticket.user_id,
               
                })

        value =  {
                'id': customer.id,
                'cname': customer.cname,
                'firstname':customer.firstname,
                'lastname': customer.lastname,
                'email': customer.email,
                'street': customer.street, 
                'city': customer.city,
                'state': customer.state,
                'postal': customer.postal, 
                'user_id': customer.user_id, 
                'user': inner_user,
                'tickets': inner_tickets,
                'opentickets': customer.open_ticket_count()
                }     

        return value


class TicketResource(object):


    @appl.route('/api/v1.0/tickets', methods=['GET'])
    def ticket_list_json():


        querystring = request.args.get('q')
        if (querystring is not None):
            querymap = json.loads(querystring)
            tickets = Ticket.list(filter_by=querymap)
        else:
            tickets = Ticket.list()

        # No Tickets
        if tickets is None:
            value = dict()
            return jsonify({'tickets': value})

        ticketList = list()
        for ticket in tickets:

            ticketList.append(TicketResource.ticket_json(ticket) )

        return jsonify({'tickets': ticketList})
     

    # GET /api/tickets/<pk>/ 
    @appl.route('/api/v1.0/tickets/<int:pk>', methods=['GET'])
    def ticket_detail_json( pk):

        ticket = Ticket.detail(pk)

        # No Such Tickets
        if ticket is None:
            if ticket is None:
                return make_response(jsonify({'error': 'Not found'}), 404)

    
        return jsonify({'ticket': TicketResource.ticket_json(ticket)})




    @appl.route('/api/v1.0/tickets', methods=['POST'])
    def ticket_create_json():

        if not request.json or not 'ttype' in request.json:
            abort(400)
        print('REQUEST ' + str(request.json))

        try:
           ticket = Ticket.create(ttype=request.json.get('ttype') , tpriority=request.json.get('tpriority') , body=request.json.get('body'), \
                                  timestamp=request.json.get('timestamp'), modified_timestamp=request.json.get('timestamp'), \
                                  firstname=request.json.get('firstname'), \
                                  lastname=request.json.get('lastname'),  phone=request.json.get('phone'), \
                                  cemail=request.json.get('cemail'), tstate=request.json.get('tstate'), \
                                  customer_id=request.json.get('customer_id'), user_id=request.json.get('user_id') ) 
           print('TICKET=' + str(ticket))
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)


        return jsonify({'ticket': TicketResource.ticket_json(ticket)}), 201


    @appl.route('/api/v1.0/tickets/<int:pk>', methods=['PUT'])
    def ticket_update_json( pk):

        if not request.json or not 'ttype' in request.json:
            abort(400)

        try:
             ticket = Ticket.update(pk, request.json.get('tnumber'), request.json.get('ttype') , request.json.get('tpriority') , request.json.get('body'), \
                                request.json.get('timestamp'), request.json.get('modified_timestamp'), request.json.get('firstname') , request.json.get('lastname'),  \
                                request.json.get('phone'), request.json.get('cemail'), request.json.get('tstate'), request.json.get('customer_id'), request.json.get('user_id') ) 
    
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

 

        return jsonify({'ticket': TicketResource.ticket_json(ticket)})


    @appl.route('/api/v1.0/tickets/<int:pk>', methods=['DELETE'])
    def ticket_delete_json( pk):

        Ticket.delete(pk)
        return jsonify({'result': True})


    @classmethod
    def ticket_json(cls, ticket):

        inner_customer = {
            'id': ticket.customer.id,
            'cname': ticket.customer.cname,
            'email': ticket.customer.email,
            'street': ticket.customer.street,
            'city': ticket.customer.city,
            'state': ticket.customer.state,
            'postal': ticket.customer.postal,
            'user_id': ticket.customer.user_id,
            }

        inner_comments = list()
        commentList = ticket.comments

        for comment in commentList:
            inner_comments.append( {
            'id': comment.id,
            'timestamp': comment.timestamp,
            'notification': comment.notification, 
            'body':  comment.body,
            'email': comment.email,
            'user_id': comment.user_id,
            'ticket_id':  comment.ticket_id,
            })

        

        value =  {
            'id': ticket.id,
            'tnumber': ticket.ticketnumber.id,
            'ttype': ticket.ttype,
            'tpriority': ticket.tpriority,
            'body': ticket.body,
            'timestamp': ticket.timestamp,
            'modified_timestamp': ticket.modified_timestamp,
            'firstname': ticket.firstname,
            'lastname': ticket.lastname,
            'phone': ticket.phone,
            'cemail': ticket.cemail,
            'tstate':  ticket.tstate,
            'comments': inner_comments,
            'customer_id':  ticket.customer_id,
            'user_id': ticket.user_id,
            'customer': inner_customer,
    
        }

        return value


class CommentResource(object):

    
    @appl.route('/api/v1.0/comments', methods=['GET'])
    def comment_list_json():

        querystring = request.args.get('q')
        if (querystring is not None):
            querymap = json.loads(querystring)
            comments = Comment.list(filter_by=querymap)
        else:
            comments = Comment.list()

        # No Comments
        if comments is None:
            value = dict()
            return jsonify({'comments': value})

        commentList = list()
        for comment in comments:
            commentList.append( CommentResource.comment_json(comment) )
               
        return jsonify({'comments': commentList})



    @appl.route('/api/v1.0/comments/<int:pk>', methods=['GET'])
    def comment_detail_json( pk):

        comment = Comment.detail(pk)
      
        # No Comment
        if comment is None:
               return make_response(jsonify({'error': 'Not found'}), 404)

                
        return jsonify({'comment': CommentResource.comment_json(comment)})

     

    @appl.route('/api/v1.0/comments', methods=['POST'])
    def comment_create_json():

        if not request.json or not 'body' in request.json:
            abort(400)

        try:
            comment = Comment.create(request.json.get('body'), request.json.get('timestamp'), request.json.get('notification'), request.json.get('email'),\
                                request.json.get('user_id'), request.json.get('ticket_id')  )

        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

        return jsonify({'comment': CommentResource.comment_json(comment)}), 201



    @appl.route('/api/v1.0/comments/<int:pk>', methods=['PUT'])
    def comment_update_json(pk):

        if not request.json or not 'body' in request.json:
            abort(400)

        try:
            comment = Follower.update(pk, request.json.get('body'), request.json.get('timestamp'), request.json.get('notificationn'), request.json.get('email'), \
                               request.json.get('user_id'), request.json.get('ticket_id') )
     
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)
          
        return jsonify({'comment': CommentResource.comment_json(comment)})



    @appl.route('/api/v1.0/comments/<int:pk>', methods=['DELETE'])
    def comment_delete_json( pk):

        Comment.delete(pk)
        return jsonify({'result': True})

    @classmethod
    def comment_json(cls, comment):

        value =  {
               'id': comment.id,
               'body': comment.body,
               'timestamp': comment.timestamp,
               'notification': comment.notification,
               'email': comment.email,
               'user_id': comment.user_id,
               'ticket_id': comment.ticket_id,
                } 

        return value


class FollowerResource(object):


    @appl.route('/api/v1.0/followers', methods=['GET'])
    def follower_list_json():

        querystring = request.args.get('q')
        if (querystring is not None):
            querymap = json.loads(querystring)
            followers = Follower.list(filter_by=querymap)
        else:
            followers = Follower.list()

        # No Followers
        if followers is None:
            value = dict()
            return jsonify({'followers': value})

        followerList = list()
        for follower in followers:
            followerList.append( FollowerResource.follower_json(follower) )
                
        return jsonify({'followers': followerList})

   
    @appl.route('/api/v1.0/followers/<int:pk>', methods=['GET'])
    def follower_detail_json(pk):

        follower = Follower.detail(pk)

        # No Such Follower
        if follower is None:
            return make_response(jsonify({'error': 'Not found'}), 404)

        return jsonify({'follower': FollowerResource.follower_json(follower)})


    @appl.route('/api/v1.0/followers', methods=['POST'])
    def follower_create_json():

        if not request.json or not 'ticket_id' in request.json:
            abort(400)

        try:

            follower = Follower.create(request.json.get('timestamp'), request.json.get('modified_timestamp'), \
                                request.json.get('user_id'), request.json.get('ticket_id')  ) 


        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

        return jsonify({'follower': FollowerResource.follower_json(follower)}),  201


    @appl.route('/api/v1.0/followers/<int:pk>', methods=['PUT'])
    def follower_update_json(pk):

        if not request.json or not 'ticket_id' in request.json:
            abort(400)

        try:
            follower = Follower.update(pk, request.json.get('timestamp'), request.json.get('modified_timestamp'), \
                               request.json.get('user_id'), request.json.get('ticket_id') )
    
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)


        return jsonify({'follower': FollowerResource.follower_json(follower)})



    @appl.route('/api/v1.0/followers/<int:pk>', methods=['DELETE'])
    def follower_delete_json(pk):

        Follower.delete(pk)
        return jsonify({'result': True})
    

    @classmethod
    def follower_json(cls, follower):
        value =  {
               'id': follower.id,
               'timestamp': follower.timestamp,
               'modified_timestamp': follower.modified_timestamp,
               'user_id': follower.user_id,
               'ticket_id': follower.ticket_id,
        }

        return value


class UserResource(object):

    @appl.route('/api/v1.0/users', methods=['GET'])
    def user_list_json():

        # get the value of the q queryparm (i.e. ?q=some-value)
        # example http://192.168.0.12:5000/api/v1.0/users?q={%22uname%22:%20%22bwebster%22}

        querystring = request.args.get('q')
        if (querystring is not None):
            querymap = json.loads(querystring)
            users =User.list(filter_by=querymap)
        else:
            users = User.list()

        # No Users
        if users is None:
            value = dict()
            return jsonify({'users': value})

        userList = list()
        for user in users:
            userList.append( UserResource.user_json(user) )
        
        return jsonify({'users': userList})
                

    @appl.route('/api/v1.0/users/<int:pk>', methods=['GET'])
    def user_detail_json(pk):

        user = User.detail(pk)

        # No Such User
        if user is None:
            #value = dict()
            #return jsonify({'user': value})
            return make_response(jsonify({'error': 'Not found'}), 404)
        

        return jsonify({'user': UserResource.user_json(user) })
      
       

    # GET /api/users/<pk>/ 
    @appl.route('/api/v1.0/users', methods=['POST'])
    def user_create_json():

        if not request.json or not 'uname' in request.json:
            abort(400)

        try:
            user = User.create(uname=request.json.get('uname'), password=request.json.get('password'), firstname=request.json.get('firstname'), \
                              lastname=request.json.get('lastname'), phone=request.json.get('phone'), email=request.json.get('email'), \
                              kinveyuser=request.json.get('kinveyuser'), kinveypassword=request.json.get('kinveypassword')  )
      
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)


        return jsonify({'user': UserResource.user_json(user)}), 201
         


    # PUT /api/users/<pk>/
    @appl.route('/api/v1.0/users/<int:pk>', methods=['PUT'])
    def user_update_json(pk):

        if not request.json or not 'uname' in request.json:
            abort(400)

        try:
            user = User.update(id=pk, suname=request.json.get('uname'), password=request.json.get('password'), firstname=request.json.get('firstname'), \
                              lastname=request.json.get('lastname'), phone=request.json.get('phone'), email=request.json.get('email'), \
                              kinveyuser=request.json.get('kinveyuser'), kinveypassword=request.json.get('kinveypassword')  )
        
        
        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

        return jsonify({'user': UserResource.user_json(user)})



    @appl.route('/api/v1.0/users/<int:pk>', methods=['DELETE'])
    def user_delete_json(pk):

        try:
            User.delete(pk)
            print("In User Delete api.py")

        except MCException as e:
            return make_response(jsonify({'error': e.value}), 500)

        return jsonify({'result': True})



    @classmethod
    def user_json(cls, user):

        inner_customers = list()

        for customer in user.customers:
            customer =  {
                'id': customer.id,
                'cname': customer.cname,
                'email': customer.email,
                'street': customer.street, 
                'city': customer.city,
                'state': customer.state,
                'postal': customer.postal, 
                'user_id': customer.user_id, 
                'opentickets': customer.open_ticket_count()
                }     

            inner_customers.append(customer)


        value = {
            'id': user.id,
            'uname': user.uname,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone': user.phone,
            'email': user.email,
            'kinveyuser': user.kinveyuser,
            'kinveypassword': user.kinveypassword,
            'customers': inner_customers
    
        }



        return value




 
