import requests

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


for i in range(len(getRequest('asset').json()['response']['manageable'])):
    id2 = getRequest('asset').json()['response']['manageable'][i]['id']
    if getRequestID('asset', id2).json()['response']['type'] == 'dynamic':
        print getRequestID('asset', id2).json()['response']['name']
        requests.delete(myurl + 'asset' + '/' + str(id2), headers={'X-SecurityCenter': str(t)},
                        cookies=r.cookies, verify=False)

for i in range(len(getRequest('asset').json()['response']['usable'])):
    id1 = getRequest('asset').json()['response']['usable'][i]['id']
    if getRequestID('asset', id1).json()['response']['type'] == 'dynamic':
        print getRequestID('asset', id1).json()['response']['name']
        requests.delete(myurl + 'asset' + '/' + str(id1), headers={'X-SecurityCenter': str(t)},
                        cookies=r.cookies, verify=False)
