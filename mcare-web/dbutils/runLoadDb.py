import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app import loadDb

def main():

    print('Loading data into customer_service database.');
    loadDb.main()

if __name__ == "__main__":
   # stuff to run when called by a command line vs import 
   main()
