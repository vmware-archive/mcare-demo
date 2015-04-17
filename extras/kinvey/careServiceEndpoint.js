//Test in harness with body value of {"location":"CLOUD"}
function onRequest(request, response, modules) {
  if (request.body.location == "CLOUD")
   	response.body = {url: "http://customer-service.23.92.225.219.xip.io/api/"};
  else
         response.body = {url: "http://192.168.0.9:5000/api/"};
    
	response.complete(201);
}

