import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BOARD) #Physical pin numbering
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

def button_insert2storage():
    print "CLICKED"

GPIO.add_event_detect(7, GPIO.RISING, callback=button_insert2storage)


message = input("Press enter to quit\n\n")

GPIO.cleanup()