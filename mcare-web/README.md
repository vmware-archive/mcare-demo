vca-callcenterapp-demo
======================

A basic Call Center Ticket Management App 

![WebSnapshot](https://github.com/vmware/mcare-demo/blob/master/docs/resources/mCareWeb.png)

The mCare Application supports both Web and ios mobile clients.
A REST API is available to support extension to other client types

The App can be run locally in a unix shell or deployed to Cloud Foundry.

####Just Run It Mode!

The mCare application will run locally using it's default configuration.

Get the App

```
mkdir mcare
cd mcare
git clone https://github.com/vmware/mcare-demo
```

```
pip install -r requirements.txt
python runApp.py
```

One the application has started, open a browser to the url 

http://localhost:5000


Configuration
=============
A single configuration file named config.py contains all configuration options for the application.

The application will successfully run using the default configuration settings.
The default configuration utilizes an im-memory database with sample data.
Any additions or modifications to the data will be lost when the application is shutdown.

To configure a persistent mySql Database, which will save data across restarts, refer to the configuring
a database section.


Deploying mCare
===============

### Deploying Locally 

Follow the 'Just Run It Mode ' steps above to install the application.



### Deploying to Cloud Foundry

mCare has been tested with Pivotal Cloud Foundry 1.3

During deployment to Cloud Foundry the application will search for a mySql database service
exposed either as a mySQL service or as a Cloud Foundry User Provided Service.
A mySql database exposed as a UPS can be located locally or remotely from the Cloud Foundry Servers.
If no service definition is found, the application will default to the in-memory default database.

A default Cloud Foundry manifest file has been provided.

```
cf login
cd mcare
cf push . customer-service

```


One the application has started, open a browser to the url provided by Cloud Foundry
For example

urls: customer-service.22.22.222.219.xip.io


#### Configuring a mySql Database


##### Configure the Database as a Cloud Foundry User Provided Service


To connect to a mySql database running outside of Cloud Foundry,
a Cloud Foundry User Provided Service must be configured, before deploying the app.
This can be easily done using the Cloud Foundry CLI to create the service

For Example

```
cf cups remote-mysql -p '{"host":"192.168.109.2","port":"3306","database":"customer_database","user":"bob","password":"welcome1"}'
```

Note that the name of the user provided service must be 'remote-mysql' as shown above


#### Configure the Database as a mySQL Service within Cloud Foundry


Using the Cloud Foundry CLI create a mySql Service.

For Example

```
cf cups remote-mysql -p '{"host":"192.168.109.2","port":"3306","database":"customer_database","user":"bob","password":"welcome1"}'
```






####Configure the local mySql database 

Assuming you have a running mySql Server,
Create a database named 'customer_database' using the command line (shown below) 

```
mysql -u root -p
welcome1

mysql> create database customer_database;
mysql> quit

```


Edit the config.py file and set the SQLALCHEMY_DATABASE_URI for the mySql Database Server.

For example:

```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bob:welcome1@localhost:3306/customer_database'

```






- Demo documentation | [vca-mycustomerDemo](https://github.com/rdbwebster/vca-callcenterapp-demo-docs)  


