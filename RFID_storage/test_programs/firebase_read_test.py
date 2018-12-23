from firebase import firebase
firebase = firebase.FirebaseApplication('https://RFID-storage.firebaseio.com',None)
result = firebase.get('/items',None)
print result

