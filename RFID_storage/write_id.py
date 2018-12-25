from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

new_id = '3'

result = firebase.post('/items/1', new_id)
print result