from firebase import firebase

firebase = firebase.FirebaseApplication('https://RFID-storage.firebaseio.com',None)

result_old = 0
while true: 
    result = firebase.get('/items',None)
    
    if result != result_old: 
        print result
    result_old = result
    
