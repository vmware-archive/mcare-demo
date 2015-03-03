from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import *
from config import config
from apscheduler.schedulers.background import BackgroundScheduler
from app import db

#from . import ticketNotifier

# Custom Jinja template functions
def lookup_priority_name(priority_number):
    priorities = config['development'].TICKET_PRIORITIES
    priDict = dict(priorities)

    try:
         return priDict[priority_number]
    except KeyError:
        return 'Unknown'
        

# Create appl immediately at module level so teardown_appcontext function can be registered
appl = Flask(__name__)
appl.config.from_object(config['development'])
appl.jinja_env.globals.update(lookup_priority_name=lookup_priority_name)

bootstrap = Bootstrap()
bootstrap.init_app(appl)

# Configure the Database

dburl = db.configure()
appl.config['SQLALCHEMY_DATABASE_URI'] = dburl
from app.db import session


@appl.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()





def run():
 
    global appl
   

    if config['development'].APNP_ENABLED:

        # Start the ticketNotifier based on a schedule
        scheduler = BackgroundScheduler()
        pollRate = config['development'].APNP_POLL_RATE
    
       # Check if running on Cloud Foundry

    if os.getenv('VCAP_APP_PORT',0) != 0:   
            # Use Cloud foundry env settings                                   
            pythonPort = os.getenv('VCAP_APP_PORT') # Assigned port for app in Cloud Foundry
            pythonHost = os.getenv('VCAP_APP_HOST', '0.0.0.0') # Assigned host in Cloud Foundry
            print('VCAP_APP_HOST=', pythonHost)
            print('VCAP_APP_PORT=', pythonPort)
    else:
            # Setup for local execution, Cloud Foundry may Override
            pythonPort = config['development'].PYTHON_PORT
            pythonHost = config['development'].PYTHON_HOST
        
   
 #   scheduler.add_job(ticketNotifier.main, 'interval', minutes=pollRate, id='my_job_id')
 #   scheduler.start()
 #   print(scheduler.print_jobs())
 #   print('Started Scheduler')

    db.init_db()

    print('Python listening on Host: ' + str(pythonHost))
    print('Python listening on Port: ' + str(pythonPort))
    print('Alchemy sql server url = ' + appl.config['SQLALCHEMY_DATABASE_URI'])

    appl.run(debug=config['development'].DEBUG, port=int(pythonPort), host=pythonHost,threaded=True)





