from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

result = firebase.post('/items/','carl er rar')
print result
