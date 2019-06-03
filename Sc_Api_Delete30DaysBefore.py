import requests
import time
import datetime
from datetime import timedelta

requests.packages.urllib3.disable_warnings();

myurl = 'https://security_center_api_endpoint'
r = requests.post(myurl + 'token', verify=False, json={'username': '', 'password': ''})
j = r.json()
t = j['response']['token']


def getRequest(method):  # plugin method call
    gr = requests.get(myurl + str(method), headers={'X-SecurityCenter': str(t)}, cookies=r.cookies, verify=False)
    return gr;


def getRequestID(method, id):  # plugin/id  method call
    gr = requests.get(myurl + str(method) + '/' + str(id), headers={'X-SecurityCenter': str(t)}, cookies=r.cookies,
                      verify=False)
    return gr;


gr = getRequest("scanResult").json()
for i in range(len(gr['response']['usable'])):
    id = gr['response']['usable'][i]['id']
    finTime = time.strftime('%Y-%m-%d',
                            time.localtime(float(getRequestID("scanResult", id).json()['response']['finishTime'])))
    daysBefore = (datetime.datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    if daysBefore >= finTime:
        delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                                 cookies=r.cookies, verify=False)
