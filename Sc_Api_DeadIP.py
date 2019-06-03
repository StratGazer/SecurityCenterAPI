import requests
import time
from datetime import timedelta
import datetime
import csv

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


def allDeadIPs():
    with open("deadIPAll.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect = 'excel')
        for i in range(len(getRequest('scanResult').json()['response']['usable'])):
            for j in range(len(getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['progress']['scanners'])):
                if getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['progress']['scanners'][j]['deadHostIPs'] != "":
                    temp = getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['progress']['scanners'][j]['deadHostIPs']
                    temp1 = [e.encode('utf-8') for e in temp.strip('[]').split(',')]
                    for l in range(len(temp1)):
                        writer.writerow([temp1[l]])


def lastWeekDeadIPs():
    with open("deadIP.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for i in range(len(getRequest('scanResult').json()['response']['usable'])):
            for j in range(len(getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['progress']['scanners'])):
                if getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['progress']['scanners'][j]['deadHostIPs'] != "":
                    scannedTime = time.strftime('%Y-%m-%d', time.localtime(float(getRequestID('scanResult', getRequest('scanResult').json()['response']['usable'][i]['id']).json()['response']['finishTime'])))
                    today = datetime.datetime.now()
                    for k in range(0, 7):  # check last 7 days
                        t1 = today - timedelta(days=k)
                        t1 = t1.strftime('%Y-%m-%d')
                        if scannedTime == t1:  # if hosts in the range of last week
                            temp = getRequestID('scanResult',getRequest('scanResult').json()['response']['usable'][i]['id']).json()[+'response']['progress']['scanners'][j]['deadHostIPs']
                            temp1 = [e.encode('utf-8') for e in temp.strip('[]').split(',')]
                            for l in range(len(temp1)):
                                writer.writerow([temp1[l]])


input = raw_input("1 for last week Dead IPsn\n"
                  "2 for all Dead IPs\n")
if input == '1':
    lastWeekDeadIPs()
elif input == '2':
    allDeadIPs()
