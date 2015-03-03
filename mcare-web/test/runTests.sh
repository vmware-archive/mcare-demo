
# Rest  tests may run against local http server or http server on Cloud Foundry
# For Jenkins build/test http location is returned by 'cf push' command and 
# use HTTP_API_URI environment variable to set uri of http server hosting rest services
export HTTP_API_URI='http://bwebster-mbpro:5000'
echo "Running Rest Service Tests"

python -m unittest discover -s ./rest
