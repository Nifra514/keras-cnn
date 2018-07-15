import json
import requests 
import getpass
import pickledb

db = pickledb.load('example.db', False) 

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code

    except requests.ConnectionError:
        error = 'Please Check Your Internet Connection and Try Again !!!'
        return error


token = ""
# Login
# data = {"uname": "qweqwe","password":"asd456"}
# resp = requests.post('http://localhost:8888/asllearning/api/login.php', data=data)
# print (resp.text)
# token = resp.text

def make_login(uname, password):
    data = {"uname": uname,"password":password}
    resp = requests.post('http://localhost:8888/asllearning/api/login.php', data=data)
    # print (resp.text)
    token = json.loads(resp.text)
    return token


def user_info():
    # User info 
    print('- GET USER FROM TOKEN')
    headers = {'x-token':get_token()}
    resp = requests.get('http://localhost:8888/asllearning/api/user.php',headers=headers)
    return json.loads(resp.text)


def set_token(token):
    #save token to local storages
    db.set("token",token)

def get_token():
    #get token from local storage
    return db.get("token")



