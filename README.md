# A vCloud Air Application Services Demo


This demo highlights the use of Application Services on VMWare vCloud Air

##Demo Scenario
The ficticous company *MediStuff* wants to mobile enable it's sales workforce as soon as possible.
The new mobile application should enable sales reps to view Customer Service calls placed by their accounts.


####The demo illustrates the following

- Pivotal Cloud Foundry (PCF) on vCloud Air exposing REST services to a mobile client.
- A PCF User Provided Service connecting to a remote on-premise mySQL Database
- A mobile client utilizing Kinvey mBaaS for Push Notifications

![DemoSnapshot](https://github.com/vmware/mcare-demo/blob/master/docs/resources/DemoSnapshot.png)

###### The demo is composed of a number of components each with their own gitHub repository



mCare Web Client
----------------

![WebSnapshot](https://github.com/vmware/mcare-demo/blob/master/docs/resources/mCareWeb.png)



#### mCare Web Client Use Cases

#####Search

1.  Search for Customer by Name
2.  Search for Customer by Contact Phone Number
3.  Search for all Customers
4.  Search for Ticket by Ticket Number
5.  Search for all Tickets

#####User

1. Create a new User
2. Edit a User
3. Delete a User
4. List all Users
5. Login as a user
6. Logout


##### Customers

1. Add a New Customer
2. Edit a Customer
3. Delete a Customer
4. View a Customer's tickets 
5. Change Customer User/Owner


##### Tickets

1. Create a New Ticket for a customer
2. Edit a Ticket
3. Delete a Ticket
4. View a Ticket Detail and its Comments
5. List a customers tickets
6. Close a Ticket
7. Reopen a Ticket
8. Set Ticket Priority


##### Comments

1. Create a New Comment on a Ticket
2. Delete a Comment on a ticket


##### Followers

1. Add a user as a follower to a ticket
2. Remove a user as a follower to a ticket

##### Admin

1. Create the database
2. Reload the database with sample  data


mCare Mobile Client
--------------------

![WebMobileSnapshot](https://github.com/vmware/mcare-demo/blob/master/docs/resources/mCare_mobile.png)

#### mCare Mobile Client Use Cases

1. Login
2. Logout  
3. List all Customers for the current User
4. List all Tickets for all the current User's Customers 
5. List all Tickets for a given Customer
6. View the Ticket's Comments
7. Add a New Comment to an open Ticket
8. Receive an Apple push notification whan a Customer Ticket is modified




## Developer Workstation Installation Steps


#### Install Python and Python Virtual Env

if python virtualEnv is not already on the workstation

```

   $virtualenv --version
   

   $ sudo pip install virtualenv
```

Then once virtualenv is installed

```
   $ mkdir ~/vcademo/virtualEnvs
   $ cd ~/vcademo/virtualEnvs

   $ virtualenv mcare
   $ cd mcare
   $ source ./bin/activate
   (mcare) $
```

#### Checkout the mcare project from github

```
   $ git clone https://github.com/vmware/mcare-demo.git
```


#### Open the mcare Python Web Project 

Open the project with an editor such as sublime.
Note sublime opens the directory and treats it as a project.
File-> Open 
Browse to
/Users/bwebster/vcademo/virtualEnvs/mcare/mcare-demo/mcare-web


#### Running the Web Project locally

The project should be executed within a python virtual env
to keep python modules separate the base python install on your workstation.

Ensure the python virtual env is activated, you should see a command prompt
that includes the the virtual env name 

For example

(mcare)$ 

If is not activated then run

```
$ cd mcare
$ source ./bin/activate

$ pip install -r requirements.txt
$ python runApp.py

```

Once the application has started, open a browser to the url http://localhost:5000


```

to deactivate run at some point in the future, rather than simply
closing the terminal window

```
(mcare)$ deactivate
```

## Mac xcode project

Using Apple Xcode 6.1 or greater

Open the project

~/vcaDemo/pythonVirtualEnvs/mcare/mcare-demo/mcare-mobile/mcare.xcodeproj

Deploy to iphone or iphone  emulator

Use home button to go to iPhone settings.
Open mCare app and set local flask server url

For example

##### Local flask server testing:

The values should set in the config.py

  PYTHON_HOST= '192.168.0.10'
  PYTHON_PORT= '5000'

  The host value depends

Use a value of localhost if you don’t need to connect from iPhone, set PYTHON_HOST to localhost and use
http://localhost:5000

Use a value of the local nic ip address if connecting from a browser and an iPhone, for example
http://192.168.0.10:5000

##### Cloud Foundry testing
For Cloud Foundry use the following url in the phone, no need to set PYTHON_HOST in the config.py file.
http://customer-service.23.92.225.219.xip.io


login with user  bwebster / welcome1
or another registered user created through the Web version of the App.

