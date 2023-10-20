                                                                           
## USSDBuy 

### DESCRIPTION 
It's a RESTful API for companyA for managing its USSDBuy service. Admins can use the resource to signup and manage user numbers. 

#### TECHNOLOGIES USES
* Python
* Flask
* SQLite for Data Storage
* bcrypt
* JWT for security ensurance.
#### CHALLENGES FACED 
* One major faced during the development of the service is the updating of a phone number. This is the case where I ensured that the number to be updated exists and the replacement number should be someone else's number. This is to ensure that unique of all numbers stored in the system.

#### WHAT AM PROUD OF
I am proud of being able to implement the updating of a number and also writing tests to cover this functionality.

### INSTALLATION GUIDE 
* Clone the project ```git clone _project url_```
* cd into the project root directory
* create a virtual environment using ```python -m venv <virtual_name>``` where <virtual_name> is your env name eg. If ```ussd-env``` is your venv name, then copy, paste and run ```python3 -m venv ussd-env```
* Activate virtual environment ```source <virtual_name>/bin/activate```. But you used ```ussd-env``` as your env then use this ```source <virtual_name>/bin/activate``` in your terminal far left of the console will appear as ```(ussd-env)``` which means env is activated where the word in the parenthesis is your environment name
* Installing dependencies from the ```requirements.txt```. Copy, paste and run this ```pip install -r requirements.txt```
* Running the server ```python app.py``` or ```python3 app.py``` depending on which version of python installed or if have multiple python versions on your computer, you should see ``` Running on http://127.0.0.1:5003```  ```Press CTRL+C ``` to quit
* Congratulations you have started server. If you have issues and need assistance contact me asap on LinkedIn

### HOW TO USE THE PROJECT 
The system has only one type of user which is the admin, to create or signup an admin you need to hit the signup endpoint with the email and password.

#### HOW TO USE THE RESOURCES 

##### NOTE THE FOLLOWING 

1. ALL APIs MUST START WITH THE BASE_URL = ```http://127.0.0.1:5003```
2. EXAMPLE SHOWN IN THE FIRST 2 RESOURCES, SIGNUP AND LOGIN
3. ANY NAME IN ANGLE BRACKET IS A PATH VARIABLE EG. ```{{BASE_URL}}/api/v1/<name>```
4. ALL APIs REQUIRE AUTHENTICATION AND OR AUTHORIZATION EXCEPT SIGNUP AND LOGIN

##### REGISTRATION OR SIGNUP =>  POST: ```{{BASE_URL}}/api/v1/signup```
 **sample signup request body**
{
    "email": "vida@bluespace.io",
    "password": "thanks",
}

##### LOGIN => POST: ```{{BASE_URL}}/api/v1/login```
NB: when login is successful, token is part of the response.
   **sample login request body**
   
{
    "email": "vida@bluespace.io",
    "password": "thanks"
}

NB: ONLY THE SIGNUP AND LOGIN APIs DO NOT REQUIRE AUTHENTICATION

### <u>API CONTRACT 
BASE_URL = ```http://127.0.0.1:5003/```
<br>NOTE: ONLY SIGNUP AND LOGIN ARE AUTHENTICATED RESOURCES 



| Description      |                           API                           |                                      REQUEST BODY |
|:-----------------|:-------------------------------------------------------:|--------------------------------------------------:|
| signup           |            ```{{BASE_URL}}/api/v1/signup```             |  {email: "admin@bluespace.com", password: "1234"} |
| login            |             ```{{BASE_URL}}/api/v1/login```             |  {email: "admin@bluespace.com", password: "1234"} |
| add_number       |           ```{{BASE_URL}}/api/v1/users/add```           |                       {phoneNumber: "0248887779"} |
| update_number    |      ```{{BASE_URL}}/api/v1/users/<phoneNumber>```      |                       {phoneNumber: "0248887779"} |
| delete_numer     |      ```{{BASE_URL}}/api/v1/users/<phoneNumber>```      |                                               N/A |
| blacklist_number | ```{{BASE_URL}}/api/v1/users/<phoneNumber>/blacklist``` |                                               N/A |
| whitelist_number | ```{{BASE_URL}}/api/v1/users/<phoneNumber>/whitelist``` |                                               N/A |
| get_all_numbers  |             ```{{BASE_URL}}/api/v1/users```             |                                               N/A |
