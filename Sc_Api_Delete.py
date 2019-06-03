import requests
import time
requests.packages.urllib3.disable_warnings();

myurl = 'https://security_center_api_endpoint'
r=requests.post(myurl+'token', verify=False, json={'username':'','password':''})
j=r.json()
t=j['response']['token']

def getRequest(method):  # plugin method call
    gr = requests.get(myurl + str(method), headers={'X-SecurityCenter': str(t)}, cookies=r.cookies, verify=False)
    return gr;

def getRequestID(method, id):  # plugin/id  method call
    gr = requests.get(myurl + str(method) + '/' + str(id), headers={'X-SecurityCenter': str(t)}, cookies=r.cookies,
                      verify=False)
    return gr;

def deleteScanResult(id):  # delete the scan result with ID
    if getRequestID("scanResult", id).json()['error_code'] != 0:
        print "ID that you are trying to delete is not available or already deleted!"
        return
    delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                           cookies=r.cookies, verify=False)

def deleteScanResults(id1, id2):  # delete the given range of IDs' results
    if getRequestID("scanResult", id1).json()['error_code'] != 0 and getRequestID("scanResult", id2).json()['error_code'] != 0:
        print "ID that you are trying to delete is not available or already deleted!"
        return
    for i in range(id1, id2):
        if getRequestID("scanResult", i)['error_code'] != 0:  # continue if the checking scan result object is not available
            continue;
        delete = requests.delete(myurl + 'scanResult' + '/' + str(i), headers={'X-SecurityCenter': str(t)},
                               cookies=r.cookies, verify=False)

def deleteAll(): #delete ALL scan results
    user_input = raw_input("Do you want to delete ALL scan results? (Y/N)")
    if user_input is 'Y':
     for i in range(getRequest("scanResult").json()):  # all scan results
         if getRequestID("scanResult", i)['error_code'] != 0:  # continue if the checking scan result object is not available
             continue;
         delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                              cookies=r.cookies, verify=False)
    elif user_input is 'N':
        print "Process canceled"
        return

def deleteScanResultErrors(): #delete the results that the status is error
    gr=getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        if str(gr['response']['usable'][i]['status']) == "Error":
            delete = requests.delete(myurl + 'scanResult' + '/' + str(gr['response']['usable'][i]['id']),
                                     headers={'X-SecurityCenter': str(t)}, cookies=r.cookies, verify=False)

def deleteByFinishTime(date): #date formmat ("%Y-%m-%d")
    gr = getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        id = gr['response']['usable'][i]['id']
        finTime = time.strftime('%Y-%m-%d', time.localtime(float(getRequestID("scanResult", id).json()['response']['finishTime'])))
        if finTime < date:
            delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                             cookies=r.cookies, verify=False)

def deleteByOwner(owner): #delete the scans belong to given user
    gr = getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        id = gr['response']['usable'][i]['id']
        if owner is getRequestID("scanResult", id).json()['response']['owner']['username']:
            delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                                     cookies=r.cookies, verify=False)

def deleteByPolicy(policy): #delete the scans belong to given policy
    gr = getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        id = gr['response']['usable'][i]['id']
        if policy == str(getRequestID("scanResult", id).json()['response']['details']): #get policies
            delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                                     cookies=r.cookies, verify=False)

def deleteByGroup(group): #delete the scans belong to given group
    gr = getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        id = gr['response']['usable'][i]['id']
        if group == str(getRequestID("scanResult", id).json()['response']['ownerGroup']['name']):
            delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                                     cookies=r.cookies, verify=False)

def deleteByString(string): #delete the scans belong to given group
    gr = getRequest("scanResult").json()
    for i in range(len(gr['response']['usable'])):
        id = gr['response']['usable'][i]['id']
        if string in getRequestID("scanResult", id).json()['response']['name']:
            delete = requests.delete(myurl + 'scanResult' + '/' + str(id), headers={'X-SecurityCenter': str(t)},
                                     cookies=r.cookies, verify=False)

print "1 - Delete the given range of IDs' scan results (ID)\n" \
      "2 - Delete the scan result with ID (ID1-ID2)\n" \
      "3 - Delete ALL scan results\n" \
      "4 - Delete the results that the status is error\n" \
      "5 - Delete the scan results before given date time (Y-M-D)\n" \
      "6 - Delete the scans belong to given user (uXXXXX)\n" \
      "7 - Delete the scans belong to given policy (policyName)\n" \
      "8 - Delete the scans belong to given group (groupName)\n" \
      "9 - Delete the scan if it contains string (string)\n" \
      "10 - Exit"

input=0

while input != 9:
    input = raw_input("Select an option\n")
    if input == "1":
        param = raw_input("Give parameter (ID)")
        deleteScanResult(param)
    elif input == "2":
        param1=raw_input("Give 1st parameter (ID1)")
        param2=raw_input("Give 2nd parameter (ID2)")
        deleteScanResults(param1, param2)
    elif input == "3":
        deleteAll()
    elif input == "4":
        deleteScanResultErrors()
    elif input == "5":
        param = raw_input("Give parameter (Y-M-D)")
        deleteByFinishTime(param)
    elif input == "6":
        param = raw_input("Give user (uXXXXX)")
        deleteByOwner(param)
    elif input == "7":
        param = raw_input("Give parameter (policyName)")
        deleteByPolicy(param)
    elif input == "8":
        param = raw_input("Give parameter (groupName)")
        deleteByGroup(param)
    elif input == "9":
        param = raw_input("Give parameter (string)")
        deleteByString(param)
    elif input == "10":
        break