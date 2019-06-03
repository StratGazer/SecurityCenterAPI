import requests
import csv
import time
import sys

reload(sys)
sys.setdefaultencoding('utf8')
requests.packages.urllib3.disable_warnings();

myurl = 'https://security_center_api_endpoint'
r = requests.post(myurl + 'token', verify=False, json={'username': '', 'password': ''})
j = r.json()
t = j['response']['token']


def getRequest(method):  # plugin method call
    gr = requests.get(myurl + str(method), headers={'X-SecurityCenter': str(t)},
                      cookies=r.cookies, verify=False)
    return gr;


def getRequestID(method, id):  # plugin/id  method call
    gr = requests.get(myurl + str(method) + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                      cookies=r.cookies, verify=False)
    return gr;


line = []

with open("test.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, dialect='excel')
    for i in range(len(getRequest('user').json()['response'])):
        writer.writerow([getRequest('user').json()['response'][i]['username'] + ',' +
                         getRequest('user').json()['response'][i]['firstname'] + ' ' +
                         getRequest('user').json()['response'][i]['lastname'] + ',' +
                         getRequest('user').json()['response'][i]['group']['name'] + ',' +
                         getRequest('user').json()['response'][i]['role']['name'] + ',' +
                         time.strftime('%Y-%m-%d',
                                       time.localtime(float(getRequest('user').json()['response'][i]['lastLogin'])))])
