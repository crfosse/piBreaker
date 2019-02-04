import time
import nfc
from multiprocessing import Pool
import RPi.GPIO as GPIO #For button interrupt

from firebase import firebase
firebase = firebase.FirebaseApplication('https://rfid-storage.firebaseio.com',None)

import serial #For arduino communication

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


def tag_search_indefinitely():
	tag = True
	while (tag == True):
		print("tag_search")
		tag = tag_search()


def tag_search():
	tag = clf.connect(rdwr={
   	 'on-connect': lambda tag:  read_id(tag)
   	})
	return tag

#Stepper functions:
def rotate_storage():
	storage_position = firebase.get("rotation position",None)    

	return storage_position

#Button function: 
def button_insert2storage(pin_number):
	if (pin_number == 16): 
		global button_pressed
		button_pressed  = True
	
#init:

clf = nfc.ContactlessFrontend()
try:
	assert clf.open('tty:AMA0:pn532') is True, "Cannot connect to nfc reader"
except AssertionError:
	

ser = serial.Serial('/dev/ttyACM0',9600) #Arduino communication
global button_pressed
button_pressed = False


#Button interrupt:
GPIO.setmode(GPIO.BOARD) #Physical pin numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

GPIO.add_event_detect(16, GPIO.RISING, callback=button_insert2storage, bouncetime=3000)


#Async:
pool = Pool()
storage_pos = 0
old_rotation = 1

#Error handling: https://jreese.sh/blog/python-multiprocessing-keyboardinterrupt 
try:
	pool.apply_async(tag_search)

	while(storage_pos != -1):
		if(button_pressed == True):
			#global button_pressed
			button_pressed  = False
			stor_pos = old_rotation #firebase.get("rotation position", None)
			if(stor_pos == 4):
				result = firebase.put("/","rotation position",1)
			else: 
				result = firebase.put("/","rotation position",(stor_pos + 1))	
		
		rotation_result = pool.apply_async(rotate_storage)

		rotation_answer = rotation_result.get(timeout=10)
		if(old_rotation != rotation_answer):
			ser.write(str(rotation_answer))
			print rotation_answer
			old_rotation = rotation_answer
			#time.sleep(500)
			#print ser.readline()

	#answer1 = result1.get(timeout=1) #Shutting down the tag_search in a super ugly way.
except KeyboardInterrupt:
	print("Caught Keyboard interrupt")
	pool.terminate()
	pool.join()
	clf.close()
	ser.write('1')
	ser.close()	
	GPIO.cleanup()
else: 
	print "Quitting normaly"
	pool.close()
	pool.join()
	clf.close()
	ser.write('1')
	ser.close()
	GPIO.cleanup()
