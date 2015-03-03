
import os, sys, json
from config import config
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
 

isMemoryDb = False
session = None
dburl = None
Base = declarative_base() 
engine = None


def configure():

    global isMemoryDb
    global session 
    global dburl
    global Base
    global engine

    # Check if running on Cloud Foundry

    isMemoryDb = False
    if os.getenv('VCAP_APP_PORT',0) != 0:   # Running in Cloud Foundry?
                                            # if so use values from config.py
        # Running on Cloud Foundry
        try:

            found = False
            # Check for mySql as a User Provided Service
            ups_services = json.loads(os.environ['VCAP_SERVICES'])['user-provided']
            for service in ups_services:
                svcname = service['name']
                if  svcname == 'remote-mysql':
                 
                    credentials = service['credentials']
                    sqlhost = str(credentials['host'])
                    print('sqlhost=' + sqlhost)
                    sqlport = str(credentials['port'])
                    print('sqlport=' + sqlport)
                    sqluser = str(credentials['user'])
                    print('sqluser=' + sqluser)
                    sqlpassword = str(credentials['password'])
                    print('sqlpassword=' + sqlpassword)
                    dburl="mysql+pymysql://" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/customer_database"
                    #url="postgresql://postgres:" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/postgres"
                    # Override config.py with Cloud Foundry DB URI
               #     appl.config['SQLALCHEMY_DATABASE_URI'] = dburl
                    found = True

            # Check for mySql as a Service
            if not found:
                  mysqlservices = json.loads(os.environ['VCAP_SERVICES'])['mysql']
                  for service in mysqlservices:
                      svcname = service['name']
                      if  svcname == 'customer-service-mysql':
                 
                        credentials = service['credentials']
                        sqlhost = str(credentials['host'])
                        print('sqlhost=' + sqlhost)
                        sqlport = str(credentials['port'])
                        print('sqlport=' + sqlport)
                        sqluser = str(credentials['user'])
                        print('sqluser=' + sqluser)
                        sqlpassword = str(credentials['password'])
                        print('sqlpassword=' + sqlpassword)
                        dburl="mysql+pymysql://" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/customer_database"
                        #url="postgresql://postgres:" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/postgres"
                        # Override config.py with Cloud Foundry DB URI
                        appl.config['SQLALCHEMY_DATABASE_URI'] = dburl
                        found = True

            # Use sqlLite in memory DB
            if not found:
                  dburl="sqlite://"
                  #url="postgresql://postgres:" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/postgres"
                  # Override config.py with Cloud Foundry DB URI
           #       appl.config['SQLALCHEMY_DATABASE_URI'] = dburl
                  isMemoryDb = True
             


        except KeyError as e:
            print ('Error: Could not locate user provided service or sql Service in VCAP_SERVICES env variable')
            print ('VCAP_SERVICES=', os.environ['VCAP_SERVICES'])
            print (' To run outside Cloud Foundry Supply command line parameters')
            sys.exit(2) 

    else:
         # Running locally, use config setting.
        
         dburl = config['development'].SQLALCHEMY_DATABASE_URI
      #   appl.config['SQLALCHEMY_DATABASE_URI'] = dburl

    # Create Database Engine

    if isMemoryDb:
       engine = create_engine(dburl, connect_args={'check_same_thread':False}, poolclass=StaticPool)
    else:   
       try:
          engine = create_engine(dburl)
       except ex:
                  print("Unable to connect to DB at " + dburl + " switching to in Memory DB.")
                  dburl="sqlite://"
                  #url="postgresql://postgres:" + sqluser + ":" + sqlpassword + "@" + sqlhost + ":" + sqlport + "/postgres"
                  # Override config.py with Cloud Foundry DB URI
               #   appl.config['SQLALCHEMY_DATABASE_URI'] = dburl
                  isMemoryDb = True
  

    # Create DB Session

    session = scoped_session(lambda: create_session(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True))

    Base.query = session.query_property()


    return dburl



def init_db():

        global Base
        # import all modules here that might define models so that
        # they will be registered properly on the metadata. 
        import app.storage.db.model
        print('init_db() engine ' + str(engine))  
        print('init_db() Session object is ' + str(session))
        Base.metadata.create_all(bind=engine)

        print('TABLES: ')
        for t in Base.metadata.sorted_tables:
      
            print(str(t))
        print(" ") # \n

        from app import views
        from app import api
        
        # Load Sample data if using MemoryDb
        if isMemoryDb:
           loadDb.main()






    




