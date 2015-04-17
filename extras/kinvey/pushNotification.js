// Test in Kinvey test harness with body value of {"username": "bwebster", "customer": "JamesCo", "number": "34336"}
function onRequest(request, response, modules) {
	  var collectionAccess = modules.collectionAccess
, userCollection = collectionAccess.collection('user')
, utils = modules.utils
, push = modules.push
, template = '{{customer}}, ticket {{number}} has been modified!'
, pushedMessageCount = 0
, userCount;
// Find all users who's username matches the username in the request 
userCollection.find({"username": request.body.username}, function(err, userDocs){
// Total number of messages to send
userCount = userDocs.length;
// Each message is customized
userDocs.forEach(function(doc){
var values = {
name: doc.givenName,
customer: request.body.customer,
number: request.body.number
};
// Render the message to send
var message = utils.renderTemplate(template, values);
// Send the push
push.send(doc, message);
// Keep track of how many pushes we've sent
pushedMessageCount++;
// reduce the number of users left to push to
userCount--;
if (userCount <= 0){
// We've pushed to all users, complete the request
response.body = {"message": "Attempted to push " + pushedMessageCount + " messages."};
response.complete(200);
}
});
});
}

