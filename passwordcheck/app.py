from flask import request, Flask
import json, socket

special_chars = {'[', '@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '\\', '|', '}', '{', '~', ':', ']'}
numerical_chars = {'0', '1', '2', '3', '4', '5', '6', '7' , '8', '9'}
capitals = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Z'}

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
# curl -d '{ "password" : "xxxxxxxx" }' -X POST http://localhost:9001/check  -H "Content-type: application/json"
#

@app.route("/check", methods=["POST"])
def compute():
    hostName = socket.gethostname()

    password = request.json['password']
    password_length = len(password)
    has_special = False
    has_num = False
    has_capital = False

    returnDictionary = {}
    returnDictionary["password"] = password
    returnDictionary["length"] = password_length
    returnDictionary["has_special"] = has_special
    returnDictionary["has_num"] = has_num
    returnDictionary["has_capital"] = has_capital
    returnDictionary["success"] = True

    if password_length < 5:
        returnDictionary["success"] = False
    for i in range(password_length):
    	if not has_special and password[i] in special_chars:
    		has_special = True
    	if not has_num and password[i] in numerical_chars:
    		has_num = True
    	if not has_capital and password[i] in capitals:
    		has_capital = True
    	if has_special and has_num and has_capital:
    		break
    
    returnDictionary["has_special"] = has_special
    returnDictionary["has_num"] = has_num
    returnDictionary["has_capital"] = has_capital
    
    if not has_special or not has_num or not has_capital:
    	returnDictionary["success"] = False
    
    return json.dumps(returnDictionary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9001)
