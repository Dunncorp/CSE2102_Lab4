from flask import request, Flask
import json, socket

import sys
sys.path.insert(0,"..")

import requests
import uuid

special_chars = {'[', '@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '\\', '|', '}', '{', '~', ':', ']'}
numerical_chars = {'0', '1', '2', '3', '4', '5', '6', '7' , '8', '9'}
capitals = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z'}



#import my_imports.top


app = Flask(__name__)

users = {}

#
# curl http://localhost:9003
#
@app.route('/')
def echo():
    returnDictionary = {}
    returnDictionary["echo"] = str(socket.gethostname())
    return json.dumps(returnDictionary)

#
# curl -d '{ "email": "user_email", "password" : "user_password" }' -X POST http://localhost:9003/adduser -H "Content-type: application/json"
#
@app.route("/adduser", methods=["POST"])
def adduser():
    user_email = request.json['email']
    user_pass = request.json['password']
    
    valid_email = True
    
    number_of_at_signs = user_email.count("@")

    if number_of_at_signs == 1:
    	at_idx = user_email.find('@')
    	local = user_email[0:at_idx]
    	domain = user_email[at_idx + 1: len(user_email)]
    	# local part of email cannot start or end with period or hyphen
    	if local[0] == '.' or local[-1] == '.' or local[0] == '-' or local[-1] == '-':
    		valid_email = False
    	# local part cannot contain two periods back to back
    	for i in range(len(local) - 1):
    		if local[i] == '.' and local[i+1] == local[i]:
    	 		valid_email = False
    	 		break
    	# domain part of email cannot start or end with hypthn
    	if domain[0] == '-' or domain[-1] == '-':
    		valid_email = False
    else:
    	valid_email = False
    
    
    valid_pass = True
    
    has_special = False
    has_num = False
    has_capital = False
    
    if len(user_pass) < 5:
        valid_pass = False
    for i in range(len(user_pass)):
    	if not has_special and user_pass[i] in special_chars:
    		has_special = True
    	if not has_num and user_pass[i] in numerical_chars:
    		has_num = True
    	if not has_capital and user_pass[i] in capitals:
    		has_capital = True
    	if has_special and has_num and has_capital:
    		break
    
    if not has_special or not has_num or not has_capital:
    	valid_pass = False
    
    
    
    
    #
    # I tried getting the services to communicate with each other but couldn't figure it out in time
    #
    #email_obj = {"email": user_email}    
    #emailrequest = requests.post('http://emailcheck:9000/check', json = email_obj)
    #emaildata = emailrequest.text
    
    #password_obj = {"password", user_pass}
    #passrequest = requests.post('http://passwordcheck:9001/check', json = password_obj)
    #passdata = passrequest.text
    
    if valid_email and valid_pass:
    	user_id = uuid.uuid1()
    	users[user_id.hex] = {"email": user_email, "password": user_pass}
    
    return json.dumps(users)
    
#
#curl -d '{ "id": "user_id"}' -X POST http://localhost:9002/removeuser -H "Content-type: application/json"
#
@app.route("/removeuser", methods=["POST"])
def removeuser():
    user_id = request.json['id']
    
    if user_id in users:
    	del users[user_id]
    
    return json.dumps(users)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9003)
