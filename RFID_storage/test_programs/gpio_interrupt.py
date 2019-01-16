import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) #Physical pin numbering
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
#GPIO.setup(port_or_pin, GPIO.IN)
def button_insert2storage(pin_number):
    print "CLICKED"

GPIO.add_event_detect(16, GPIO.RISING, callback=button_insert2storage)


message = input("Press enter to quit\n\n")

GPIO.cleanup()
