import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

  
  SECRET_KEY = 'mysecret42'


class DevelopmentConfig(Config):
 
  '''
  LOCAL Execution Config
  '''

  # These values are only used if the app is not running in Cloud Foundry
  PYTHON_HOST= 'bwebster-mbpro'
  PYTHON_PORT= '5000'
 


  '''
  DATABASE Configuration
  '''

  # Database for local executions, not in cloud foundry.
  # If an active database is not found at the specified url, an in memory sqlite database will be used.

  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bob:welcome1@localhost:3306/customer_database'


  # Database for unit tests which maybe local or remote outside of Cloud Foundry
  TEST_SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bob:welcome1@locatlhos:3306/customer_database'
  # Rest service test endpoint, maybe local or running in cloud foundry, Jenkins passes CF app url using HTTP_API_URI
  TEST_HTTP_API_URI= os.environ.get('HTTP_API_URI') or PYTHON_HOST + ':' + PYTHON_PORT
  # Note when debug=TRUE scheduler may execute tasks twice
  DEBUG = True


  '''
  Apple push Notifications Config
  '''
  APNP_ENABLED=True      # True or False
  APNP= 'KINVEY'         # KINVEY or PHP
  APNP_POLL_RATE = 60    # rate for push notifications (Minutes)

  KINVEY_URL='http://baas.kinvey.com'
  KINVEY_APP_ID='kid_-1nYpMgDv'
  KINVEY_USERNAME='bwebster@vmware.com'
  KINVEY_PASSWORD=''

  PHP_URL= 'http://localhost:8000/simplepush.php'


  ''' 
  Enumeration lists
  '''

  TICKET_TYPES = [("Shipment Issue", "Shipment Issue"), ("Customer Inquiry", "Customer Inquiry"), ("Billing Issue", "Billing Issue"),
                   ("Other", "Other") ]

  TICKET_PRIORITIES = [ (1, "High"), (2, "Normal"), (3, "Low") ]

class TestingConfig(Config):
  DEBUG = False
  #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:welcome1@localhost:5432/postgres'

class ProductionConfig(Config):
  DEBUG = False
  
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production' : ProductionConfig,

    'default': DevelopmentConfig
}
