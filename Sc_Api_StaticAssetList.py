import requests
import csv
import sys

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
    gr = requests.post(myurl + str(method), data, verify=False, cookies=r.cookies,
                       headers={'X-SecurityCenter': str(t)})
    return gr


def postRequestID(method, id, data):
    gr = requests.post(myurl + str(method) + '/' + str(id), data, verify=False, cookies=r.cookies,
                       headers={'X-SecurityCenter': str(t)})
    return gr


def patchRequest(method, data):
    gr = requests.patch(myurl + str(method), data, verify=False, cookies=r.cookies,
                        headers={'X-SecurityCenter': str(t)})
    return gr


def patchRequestID(method, id, data):
    gr = requests.patch(myurl + str(method) + '/' + str(id), data=data, verify=False, cookies=r.cookies,
                        headers={'X-SecurityCenter': str(t)})
    return gr


if sys.argv[1] == '--static':
    with open("assets.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for i in range(len(getRequest('asset').json()['response']['usable'])):
            id = getRequest('asset').json()['response']['usable'][i]['id']
            if getRequestID('asset', id).json()['response']['type'] == 'static':
                writer.writerow([
                    (getRequestID('asset', id).json()['response']['name']).encode('utf-8') + ',' +
                    (getRequestID('asset', id).json()['response']['tags']).encode('utf-8')
                ])

if sys.argv[1] == '--combination':
    with open("assets.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for i in range(len(getRequest('asset').json()['response']['usable'])):
            id = getRequest('asset').json()['response']['usable'][i]['id']
            if getRequestID('asset', id).json()['response']['type'] == 'combination':
                writer.writerow([
                    (getRequestID('asset', id).json()['response']['name']).encode('utf-8') + ',' +
                    (getRequestID('asset', id).json()['response']['tags']).encode('utf-8')
                ])

if sys.argv[1] == '--dynamic':
    with open("assets.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for i in range(len(getRequest('asset').json()['response']['usable'])):
            id = getRequest('asset').json()['response']['usable'][i]['id']
            if getRequestID('asset', id).json()['response']['type'] == 'dynamic':
                writer.writerow([
                    (getRequestID('asset', id).json()['response']['name']).encode('utf-8') + ',' +
                    (getRequestID('asset', id).json()['response']['tags']).encode('utf-8')
                ])

if sys.argv[1] == '--all':
    with open("assets.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        for i in range(len(getRequest('asset').json()['response']['usable'])):
            id = getRequest('asset').json()['response']['usable'][i]['id']
            writer.writerow([
                (getRequestID('asset', id).json()['response']['name']).encode('utf-8') + ',' +
                (getRequestID('asset', id).json()['response']['tags']).encode('utf-8')
            ])
