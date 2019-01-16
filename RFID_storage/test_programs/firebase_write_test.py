#Simple firebase write test. Exchange the *********** for your firebase address.
from firebase import firebase
firebase = firebase.FirebaseApplication('https://***********.firebaseio.com',None)

path = '/items/'
value = 'Write test'
result = firebase.post(path,value)
print result

