import time

import nfc

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

from multiprocessing import Pool

#Firebase functions:
def store_item(uid):

	storage_position = firebase.get("rotation position",None)

	path  = '/items/' + str(uid)

	result = firebase.put(path,"storage position",storage_position)
	return result

#NFC functions:
def read_id(tag):
    
    tag_id = str(tag)[12:]
    print(tag_id)
    result = store_item(tag_id)
    print result
	
    return True  #Returns to the connect function and keeps listening for new cards. This doesn't seem to work however 

def tag_search():
	print("tag_search")
	tag = clf.connect(rdwr={
   	 'on-connect': lambda tag:  read_id(tag)
   	 #lambda tag: False #Simple function that stops the process after the card has been found
   	})
	if(tag == True):
		tag_search()

#Stepper functions:
def stepper_control(pos): 
	return True	

def rotate_storage():
	storage_position = firebase.get("rotation position",None)
	
	if(storage_position != -1):
	     stepper_control(storage_position)

	return storage_position


#init:
clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True

#Async:
pool = Pool()
answer2 = 0

try:
	pool.apply_async(tag_search)

	while(answer2 != -1):
		#result1 = pool.apply_async(tag_search)
		result2 = pool.apply_async(rotate_storage)

		#answer1 = result1.get(timeout=10)
		answer2 = result2.get(timeout=10)

		#print answer1
		print answer2
except KeyboardInterrupt:
	print("Caught Keyboard interrupt")
	pool.terminate()
	pool.join()
	clf.close()	
else: 
	print "Quitting normaly"
	pool.close()
	pool.join()
	clf.close()
