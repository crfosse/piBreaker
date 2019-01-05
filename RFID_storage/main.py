import time
import nfc
from multiprocessing import Pool

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

import serial

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
   	})
	if(tag == True):
		tag_search() #Not exactly a pretty solution...

#Stepper functions:
def rotate_storage():
	storage_position = firebase.get("rotation position",None)    

	return storage_position


#init:
clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True

ser = serial.Serial('/dev/ttyACM0',9600) #Arduino communication


#Async:
pool = Pool()
storage_pos = 0
old_rotation = 1

#Error handling: https://jreese.sh/blog/python-multiprocessing-keyboardinterrupt 
try:
	pool.apply_async(tag_search)

	while(storage_pos != -1):
		
		rotation_result = pool.apply_async(rotate_storage)

		rotation_answer = rotation_result.get(timeout=10)
		if(old_rotation != rotation_answer):
			ser.write(str(rotation_answer))
			print rotation_answer
			old_rotation = rotation_answer
			#time.sleep(500)
			#print ser.readline()

	answer1 = result1.get(timeout=1) #Shutting down the tag_search in a super ugly way.
except KeyboardInterrupt:
	print("Caught Keyboard interrupt")
	pool.terminate()
	pool.join()
	clf.close()
	ser.write('1')
	ser.close()	
else: 
	print "Quitting normaly"
	pool.close()
	pool.join()
	clf.close()
	ser.write('1')
	ser.close()
