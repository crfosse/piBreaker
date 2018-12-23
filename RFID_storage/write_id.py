from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

new_id = {'1','1'}

result = firebase.post('/items/',new_id)
print result
