from flask import request, Flask
import json, socket

import sys
sys.path.insert(0,"..")

#import my_imports.top

printable_chars = {"!", "#", "$", "%", "&", "'", "*", "+", "-", "/", "=", "?", "^", "_", "`", "{", "|", "}", "~"}


app = Flask(__name__)

#
# curl http://localhost:9000
#
@app.route('/')
def echo():
    returnDictionary = {}
    returnDictionary["echo"] = str(socket.gethostname())
    return json.dumps(returnDictionary)

#
# curl -d '{ "email" : "foo@bar" }' -X POST http://localhost:9000/check  -H "Content-type: application/json"
#
@app.route("/check", methods=["POST"])
def compute():
    hostName = socket.gethostname()

    email = request.json['email']
    number_of_at_signs = email.count("@")

    returnDictionary = {}
    returnDictionary["email"] = email
    returnDictionary["at_signs"] = number_of_at_signs
    returnDictionary["success"] = True

    if number_of_at_signs == 1:
    	at_idx = email.find('@')
    	local = email[0:at_idx]
    	domain = email[at_idx + 1: len(email)]
    	# local part of email cannot start or end with period or hyphen
    	if local[0] == '.' or local[-1] == '.' or local[0] == '-' or local[-1] == '-':
    		returnDictionary["success"] = False
    	# local part cannot contain two periods back to back
    	for i in range(len(local) - 1):
    		if local[i] == '.' and local[i+1] == local[i]:
    	 		returnDictionary["success"] = False
    	 		break
    	# domain part of email cannot start or end with hypthn
    	if domain[0] == '-' or domain[-1] == '-':
    		returnDictionary["success"] = False
    else:
    	returnDictionary["success"] = False
    
    
    return json.dumps(returnDictionary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
