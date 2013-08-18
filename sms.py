#!/usr/bin/python
# Original API by Abhishek Anand, June 12, 2010, abhishek@bitproxy.co.cc, http://proxyspeaks.blogspot.com
# Updated by Master Yoda
# Modified by Rishav Thakker for smss. Thanks for both of them for making this - RishavT :)s

import urllib
import httplib2
import random

def login(username,password):
    # These are some of the CNAMES or roughly servers you are directed
    #  (to balance load i guess)
    serverList = ['site1','site2','site3','site4','site5','site6']
    # Get a random server from list
    server = serverList[random.randint(0,len(serverList)-1)]
    # Make a authentication request and get the cookie
    http = httplib2.Http()
    url = 'http://' + server + '.way2sms.com:80/auth.cl'
    body = {'username': username, 'password': password,'login': 'Login'}
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'}
    try:
        response, content = http.request(url,
                                     'POST',
                                     headers=headers,
                                     body=urllib.urlencode(body))
    except:
        print("Authenticaiton post failed")
        return False
    newurl = "http://"+ server +".way2sms.com/FirstServletsms?custid="
    return (response,newurl,http)
def send(mobileNo, message,xq):
    response=xq[0]
    newurl=xq[1]
    http=xq[2]
    # Set the cookie we got for future requests
    headers = {'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                                                   'Cookie': response['set-cookie']}
    if len(mobileNo) <> 10 or len(message) > 140:
        return False
    #Check validity of MobileNumber and length of message ( should be less than 160)
    newBody = {'custid': 'undefined',
               'HiddenAction': 'instantsms',
               'Action':'sa65sdf656fdfd',
               'login': '',
               'pass': '',
               'MobNo': mobileNo,
               'textArea': message}
    # Send message with the cookie we got
    try:
        response, content = http.request(newurl,
                                     'POST',
                                     headers=headers,
                                     body=urllib.urlencode(newBody))
    except:
        print("sms sending failed")
        return False
    # If the returned text contains word successfully, your message is sent
    if content.find("successfully") <> -1:
        print("sent")
        return True
    else:
        print("Failed")
        return False
