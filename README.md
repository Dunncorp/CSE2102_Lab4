# CSE2102_Lab4
Using microservices to have a working login page

Once the repo is cloned, you should open a terminal and navigate into the new folder called CSE2102_Lab4 with the command:

cd CSE2102_Lab4

and then enter the command:

docker-compose up --build

this should take a few moments while it gets any required libraries and boots up the microservices. After the microservices finish getting created, open a new terminal. in the new terminal enter the curl commands listed below to test.


Microservice 1, first command is a valid email and the second has an incorrect syntax.
curl -d '{ "email" : "matthew.j.dunn@uconn.edu" }' -X POST http://localhost:9000/check  -H "Content-type: application/json"

curl -d '{ "email" : "matthew..dunn@uconn.edu" }' -X POST http://localhost:9000/check  -H "Content-type: application/json"


Microservice 2, first command is a valid password with a capital letter, a number and a special character. The seccond command is missing the different characters and should then return false for success.
curl -d '{ "password" : "P@ssw0rd" }' -X POST http://localhost:9001/check  -H "Content-type: application/json"

curl -d '{ "password" : "password" }' -X POST http://localhost:9001/check  -H "Content-type: application/json"


Microservice 3, first command is adding superuser role to matthew.j.dunn@uconn.edu email, second command adds admin role to same email. Third command adds a different user's role. Fourth command removed the given role from the email specified.
curl -d '{ "email": "matthew.j.dunn@uconn.edu", "newRole" : "superuser" }' -X POST http://localhost:9002/addrole -H "Content-type: application/json"

curl -d '{ "email": "matthew.j.dunn@uconn.edu", "newRole" : "admin" }' -X POST http://localhost:9002/addrole -H "Content-type: application/json"

curl -d '{ "email": "turing@gmail.com", "newRole" : "superuser" }' -X POST http://localhost:9002/addrole -H "Content-type: application/json"

curl -d '{ "email": "matthew.j.dunn@uconn.edu", "remove_role" : "superuser" }' -X POST http://localhost:9002/removerole -H "Content-type: application/json"


Microservice 4, first command gives valid email and password, this creates a unique user ID. Second command uses an invalid email, and so it should not create a new userid. Command 3 creates another user ID for another person, and the fourth command removes a user's account given the user ID.
curl -d '{ "email": "matthew.j.dunn@uconn.edu", "password" : "P@ssw0rd" }' -X POST http://localhost:9003/adduser -H "Content-type: application/json"

curl -d '{ "email": ".dunn@uconn.edu", "password" : "P@ssw0rd" }' -X POST http://localhost:9003/adduser -H "Content-type: application/json"

curl -d '{ "email": "turing@gmail.com", "password" : "Tc0mp!ete" }' -X POST http://localhost:9003/adduser -H "Content-type: application/json"

curl -d '{ "id": "user_id"}' -X POST http://localhost:9003/removeuser -H "Content-type: application/json"
