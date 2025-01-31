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
    resp = requests.post(' http://asllearning.info/api/login.php', data=data)
    token = json.loads(resp.text)
    return token


def user_info():
    # User info 
    headers = {'x-token':get_token()}
    resp = requests.get(' http://asllearning.info/api/user.php',headers=headers)
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

    url=' http://asllearning.info/ai_model/trained_model.h5'
    resp = requests.get(url)
    with open ('models/trained_model.h5','wb') as f:
        f.write(resp.content)

def write_log(user_id, log_type, log_data, action, risk):
    data = json.dumps(log_data)
    dataset = {"user_id" : user_id,"lg_type" : log_type,"data" : data, "action" : action, "risk" : risk}
    headers = {'x-token':get_token()}
    requests.post(' http://asllearning.info/api/log.php', data=dataset, headers=headers)
    return True


