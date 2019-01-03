#import time
import nfc
from multiprocessing import Pool

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)


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
def stepper_control(pos): 
	return True	

def rotate_storage():
	storage_position = firebase.get("rotation position",None)
	
	if(storage_position > 0 | storage_position < 5):
	    stepper_control(storage_position)

	return storage_position



#init:
clf = nfc.ContactlessFrontend()
assert clf.open('tty:AMA0:pn532') is True



#Async:
pool = Pool()
storage_pos = 0

#Error handling: https://jreese.sh/blog/python-multiprocessing-keyboardinterrupt 
try:
	pool.apply_async(tag_search)

	while(storage_pos != -1):
		
		rotation_result = pool.apply_async(rotate_storage)

		rotation_answer = rotation_result.get(timeout=10)

		print rotation_answer

	answer1 = result1.get(timeout=1) #Shutting down the tag_search in a super ugly way.
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
