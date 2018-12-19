# using libusb1: https://pypi.org/project/libusb1/#supported-oses

# using serial https://raspberrypi.stackexchange.com/questions/13930/capturing-serial-number-of-2-usb-rfid-reader-in-python-pi2-rfid-mifire-rfid?fbclid=IwAR3kyBryBN-X7jhMRq_aGlz3xqmFBOVZ7k6xKHkMUQuqNQA0sUdoKUDJIHo 



import serial
ser = serial.Serial('/dev/tty.usbmodem1411', 9600) # here you have to write your port. If you dont know how to find it just write ls -l /dev/tty.* in your terminal (i'm using mac)

while True:
    try:
        response = ser.readline()
        print response
    except KeyboardInterrupt:
        break

ser.close()