import json
import requests 
import getpass
import pickledb

db = pickledb.load('asl.db', False) 

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        resp = requests.get(url, timeout=timeout)
        return resp.status_code

    except requests.ConnectionError:
        error = 'Please Check Your Internet Connection and Try Again !!!'
        return error


token = ""


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

def logout():
    #remove token from local storages
    return db.deldb()


def download_model(): 

    url='http://localhost:8888/asllearning/ai_model/trained_model_3.h5'
    resp = requests.get(url)
    with open ('models/trained_model.h5','wb') as f:
        f.write(resp.content)
    # return True

def write_log(user_id, log_type, log_data, action, risk):
    data = json.dumps(log_data)
    dataset = {"user_id" : user_id,"lg_type" : log_type,"data" : data, "action" : action, "risk" : risk}
    headers = {'x-token':get_token()}
    resp = requests.post('http://localhost:8888/asllearning/api/log.php', data=dataset, headers=headers)
    print (resp.text)
    # result = json.loads(resp.text)
    # return result


