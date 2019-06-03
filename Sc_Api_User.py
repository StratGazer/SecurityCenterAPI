import requests
import json
import sys
import re

requests.packages.urllib3.disable_warnings();

myurl = 'https://security_center_api_endpoint'
r = requests.post(myurl + 'token', verify=False, json={'username': '', 'password': ''})
j = r.json()
t = j['response']['token']


def getRequest(method):
    gr = requests.get(myurl + str(method), headers={'X-SecurityCenter': str(t)},
                      cookies=r.cookies, verify=False)
    return gr;


def getRequestID(method, id):
    gr = requests.get(myurl + str(method) + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                      cookies=r.cookies, verify=False)
    return gr;


def postRequest(method, data):
    pr = requests.post(myurl + str(method), data=data, verify=False, cookies=r.cookies,
                       headers={'X-SecurityCenter': str(t)})
    return pr


def postRequestID(method, id, data):
    pr = requests.post(myurl + str(method) + '/' + str(id), data=data, verify=False, cookies=r.cookies,
                       headers={'X-SecurityCenter': str(t)})
    return pr


def patchRequest(method, data):
    ptr = requests.patch(myurl + str(method), data, verify=False, cookies=r.cookies,
                         headers={'X-SecurityCenter': str(t)})
    return ptr


def patchRequestID(method, id, data):
    ptr = requests.patch(myurl + str(method) + '/' + str(id), data=data, verify=False, cookies=r.cookies,
                         headers={'X-SecurityCenter': str(t)})
    return ptr


def checkUser(user):
    for i in range(len(getRequest('user').json()['response'])):
        if user != getRequest('user').json()['response'][i]['username']:
            continue
        elif user == getRequest('user').json()['response'][i]['username']:
            return 1


def userList(index):
    js = []
    for i in range(len(getRequest('user').json()['response'])):
        matched = re.match(r'\Au[0-9]*', getRequest('user').json()['response'][i]['username'])
        if matched:
            js.insert(0, str(getRequest('user').json()['response'][i]['username']))
    return js[index]


def titleCheck(user):
    for i in range(len(getRequest('user').json()['response'])):
        if user != getRequest('user').json()['response'][i]['username']:
            continue
        elif user == getRequest('user').json()['response'][i]['username']:
            return getRequest('user').json()['response'][i]['title']


def users():
    js = []
    for i in range(len(getRequest('user').json()['response'])):
        matched = re.match(r'\Au[0-9]*', getRequest('user').json()['response'][i]['username'])
        if matched:
            js.insert(0, str(getRequest('user').json()['response'][i]['username']))
    return js


def titles():
    js = []
    for i in range(len(getRequest('user').json()['response'])):
        js.insert(0, getRequest('user').json()['response'][i]['title'])
    return js


def deleteUser(user):
    for i in range(len(getRequest('user').json()['response'])):
        if user == getRequest('user').json()['response'][i]['username']:
            requests.delete(myurl + 'user' + '/' + str(getRequest('user').json()['response'][i]['id']),
                            headers={'X-SecurityCenter': str(t)}, cookies=r.cookies, verify=False)
            return 1


def modifyUser(user, data):
    dt = {
        "title": data
    }
    for i in range(len(getRequest('user').json()['response'])):
        if user != getRequest('user').json()['response'][i]['username']:
            continue
        elif user == getRequest('user').json()['response'][i]['username']:
            patchRequestID('user', getRequest('user').json()['response'][i]['id'], data=json.dumps(dt))
            return 1


def createUser(user, title, gid):
    data = {
        "roleID": '1000001',
        "groupID": gid,
        "username": user,
        "title": title,
        "authType": "ldap",
        "ldap": {
            "id": user
        },
        "responsibleAssetID": "-1"
    }
    re = postRequest('user', json.dumps(data))
    if re.status_code == 200:
        return 1
    return re.status_code


if sys.argv[1] == "--help":
    print "1) --create (ldapName, title, groupID)\n" \
          "2) --delete (user)\n" \
          "3) --modify (user, data)\n" \
          "4) --check (user)\n" \
          "5) --titleCheck (user)\n" \
          "6) --users All users\n" \
          "7) --titles All titles\n" \
          "8) --userList (index)"

if sys.argv[1] == "--create":
    createUser(sys.argv[2], sys.argv[3], int(sys.argv[4]))
elif sys.argv[1] == "--delete":
    deleteUser(sys.argv[2])
elif sys.argv[1] == "--modify":
    modifyUser(sys.argv[2], sys.argv[3])
elif sys.argv[1] == "--check":
    checkUser(sys.argv[2])
elif sys.argv[1] == "--userList":
    userList(int(sys.argv[2]))
elif sys.argv[1] == "--titleCheck":
    titleCheck(sys.argv[2])
elif sys.argv[1] == "--users":
    users()
elif sys.argv[1] == "--titles":
    titles()
