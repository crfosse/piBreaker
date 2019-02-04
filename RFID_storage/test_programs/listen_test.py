#A test of a really unpractical way of infinitely listening to firebase. Exchange *********** with the relevant firebase address. 
from firebase import firebase
import json

firebase = firebase.FirebaseApplication('https://***********.firebaseio.com',None)

result_old = 0
while 1: 
    result = firebase.get('/items',None)
    
    if result != result_old: 
        print result

    result_old = result


    
