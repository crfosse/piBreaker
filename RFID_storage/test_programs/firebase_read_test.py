#Simple read from firebase and print to console test. Exchange the *********** for your firebase address. 
from firebase import firebase
firebase = firebase.FirebaseApplication('https://***********.firebaseio.com',None)
path = '/items'
result = firebase.get(path,None)
print result

