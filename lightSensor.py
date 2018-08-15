#NOTES: 2 light sensors. One points towards light source and the other points towards
#motion path. Then if light sensor for light detects light, run motion light sensor
#code. That would start the counter and it would see if there is no motion by the time
#the counter reaches its set limit, send the notification and reset counter. If motion
#is present during the counting period, it would reset the counter.


import RPi.GPIO as GPIO
import time
import httplib, urllib

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit

pin_to_circuit = 7
pin_to_circuit2 = 11
count = 0
counterX1 = 0
blob = "blob"

def rc_time (pin_to_circuit): #BLACK AND WHITE = MOTION PIN 7
    count = 0
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT) 
    #GPIO.output(pin_to_circuit, GPIO.LOW) #setup actually outputs #'s
    time.sleep(0.1) #running in millisecond. 1.0 = 1 second
    #then send notification and set counterX back to 0 and repeat
    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
    return count

def rc_time2 (pin_to_circuit2): # GRAY AND PURPLE = LIGHT SOURCE PIN 11
    count = 0
    #Output on the pin for 
    GPIO.setup(pin_to_circuit2, GPIO.OUT) 
    GPIO.output(pin_to_circuit2, GPIO.LOW) #setup actually outputs #'s
    time.sleep(0.1) #running in millisecond. 1.0 = 1 second
    #then send notification and set counterX back to 0 and repeat
    #Change the pin back to input
    GPIO.setup(pin_to_circuit2, GPIO.IN)
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit2) == GPIO.LOW):
        count += 1

    return count

def MotionDetect(detection):
    detect = detection
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
         "token": "ap9paw74acp52pycn5yvwyvcuquaza",
         "user": "uhkqoh7bnvhr6w1qrz94v9u2d23i2q",
         "message": "motion message sent to phone",
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
    detect = False
    
'''def counterX(counter):
    
    counterX = counter
    counterX = 0
    counterX = counterX + 1
    print(counterX)
    
    if counterX == 30:
        MotionDetect(True)
    return counterX'''        

#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while True:
        print rc_time2(pin_to_circuit2)
	x = rc_time2(pin_to_circuit2)
	y = rc_time(pin_to_circuit)
	counterX1 = 0
	while 300 < x < 400:   
            x = rc_time2(pin_to_circuit2)
            y = rc_time(pin_to_circuit)
	    counterX1 = counterX1 + 1
	    print(counterX1)
	    if counterX1 == 30: 
                MotionDetect(True)
	    rc_time(pin_to_circuit)
	    print rc_time(pin_to_circuit)
	    if y > 2100:
                counterX1 == 0    
	    		
except KeyboardInterrupt:
    GPIO.cleanup() 
                