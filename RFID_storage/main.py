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
def init_nfc_reading(): 
	clf = nfc.ContactlessFrontend()

	error_nfc_connection = "Cannot connect to the nfc reader, might be connected to the wrong port or the last connection was not terminated properly. If the last one happened you might have to restart the nfc reader, good old turn on and off"
	assert clf.open('tty:AMA0:pn532') is True, error_nfc_connection
	return clf

def init_arduino_communication(): 
	error_arduino_connection = "Cannot connect to Arduino, probably trying to connect trough the wrong port"
	ser = serial.Serial('/dev/ttyACM0',9600) #Arduino communication
	assert ser, error_arduino_connection

	return ser

def init_button_interrupt(): 
	GPIO.setmode(GPIO.BOARD) #Physical pin numbering
	GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

	GPIO.add_event_detect(16, GPIO.RISING, callback=button_insert2storage, bouncetime=3000)


def main():
	#Var
	storage_pos = 0
	old_rotation = 1
	global button_pressed
	button_pressed = False

	#Init
	init_button_interrupt()	
	ser = init_arduino_communication()
	clf = init_nfc_reading()

	#Async:
	pool = Pool()

	#Error handling: https://jreese.sh/blog/python-multiprocessing-keyboardinterrupt 
	try:
		pool.apply_async(tag_search_indefinitely)

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

			#Send rotation to the arduino:
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
		raise
	else: 
		print "Quitting normally"
		pool.close()
		pool.join()
		clf.close()
		ser.write('1')
		ser.close()
		GPIO.cleanup()
		raise
