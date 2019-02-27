import time
import nfc
from multiprocessing import Pool
import RPi.GPIO as GPIO #For button interrupt
from firebase import firebase
import serial #For arduino communication
import atexit

""" firebase structure:
'rotation position': (possible values: 1, 2, 3, 4),
'items/<id>' (where <id> is an 8 char hex-string)
	'storage position': (possible values: 1, 2, 3, 4)
"""
firebase = firebase.FirebaseApplication(dsn='https://rfid-storage.firebaseio.com', authentication=None)
button_pressed = False
atexit.register(on_exit)

#Firebase functions:
def store_item_by_nfc_tag(nfc_tag):
	item_uid = str(nfc_tag)[12:]
	position_of_new_item = firebase.get('rotation position', name=None, connection=None)
	return firebase.put('/items/'+str(item_uid), 'storage position', data=position_of_new_item, connection=None)

def nfc_tag_listener(clf):
	while True: clf.connect(rdwr={ 'on-connect': store_item_by_nfc_tag })

#Button function: 
def button_insert2storage(pin_number):
	if (pin_number == 16): 
		global button_pressed
		button_pressed  = True
	
def main():
	clf = nfc.ContactlessFrontend()
	assert clf.open('tty:AMA0:pn532') is True
	ser = serial.Serial('/dev/ttyACM0',9600) #Arduino communication
	
	#Button interrupt:
	GPIO.setmode(GPIO.BOARD) #Physical pin numbering
	GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
	GPIO.add_event_detect(16, GPIO.RISING, callback=button_insert2storage, bouncetime=3000)

	#Async:
	pool = Pool()
	current_position = 0
	previous_position = 1

	pool.apply_async(lambda: nfc_tag_listener(clf))
	while True:
		if button_pressed:
			button_pressed = False
			new_position = (current_position % 4) + 1  # (1->2), (2->3), (3->4), (4->1)
			firebase.put('/', 'rotation position', new_position, connection=None)
		
		firebase_rotation_position = firebase.get('rotation position', name=None, connection=None)
		if (previous_position != firebase_rotation_position):
			ser.write(str(firebase_rotation_position))
			previous_position = firebase_rotation_position


if __name__ == '__main__'
	main()
