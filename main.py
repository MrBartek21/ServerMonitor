#!/usr/bin/env python3
 
import time
#from rpi_ws281x import *
import RPi.GPIO as GPIO

import smbus
from time import sleep
#import w1thermsensor
 
# LED strip configuration:
LED_COUNT = 16
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0 # set to '1' for GPIOs 13, 19, 41, 45 or 53
 
 
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


# Pin Definitons:
Relay1 = 23 # Broadcom pin 18 (P1 pin 12)
Relay2 = 24 # Broadcom pin 23 (P1 pin 16)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(Relay1, GPIO.OUT) # LED pin set as output
GPIO.setup(Relay2, GPIO.OUT) # PWM pin set as output



 
# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
 
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
 
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
 
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


def MPU_Init():
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	bus.write_byte_data(Device_Address, CONFIG, 0)
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    value = ((high << 8) | low)
    
    if(value > 32768):
            value = value - 65536
    return value





def reset():
	for i in range(strip.numPixels()):
		strip.setPixelColor(i,Color(0,0,0))

def colour(temp):
	if temp < 18:
		reset()
		l = int((temp/18)*4)
		for i in range(0,l):
			# Cyan colour for low temperatures
			strip.setPixelColor(i,Color(0,255,255))
			strip.show()
	elif temp < 26:
		reset()
		l = int(temp - 14)
		for i in range(0,l):
			# Green colour for medium temperatures
			strip.setPixelColor(i,Color(50,205,50))
			strip.setBrightness(25)
			strip.show()
	elif temp < 35:
		reset()
		l = int(((3/10.0)*temp) + 1.5)
		for i in range(0,l):
			# Red colour for high temperatures
			strip.setPixelColor(i,Color(255,0,0))
			strip.show()




if __name__ == '__main__':
    #strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    #strip.begin()
    #colorWipe(strip, Color(0, 255, 0))

    print("dsf")
    GPIO.output(Relay1, GPIO.LOW)
    GPIO.output(Relay2, GPIO.LOW)
    time.sleep(2)
    GPIO.output(Relay1, GPIO.HIGH)
    GPIO.output(Relay2, GPIO.HIGH)
    time.sleep(2)
    print("dsf")



    bus = smbus.SMBus(1)
    Device_Address = 0x68
    MPU_Init()

    #sensor = w1thermsensor.W1ThermSensor()
 
    print('Press Ctrl-C to quit.')

    try:
        while True:
            #Read Accelerometer raw value
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_YOUT_H)
            acc_z = read_raw_data(ACCEL_ZOUT_H)
            
            #Read Gyroscope raw value
            gyro_x = read_raw_data(GYRO_XOUT_H)
            gyro_y = read_raw_data(GYRO_YOUT_H)
            gyro_z = read_raw_data(GYRO_ZOUT_H)
            
            #Full scale range +/- 250 degree/C as per sensitivity scale factor
            Ax = acc_x/16384.0
            Ay = acc_y/16384.0
            Az = acc_z/16384.0
            
            Gx = gyro_x/131.0
            Gy = gyro_y/131.0
            Gz = gyro_z/131.0
            #print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	

            #if Gx>=-1 or Gx>=1:
            #if Gx<-1.0:
            #    theaterChase(strip, Color(255, 0, 0))

            #if Gy<-1:
            #    theaterChase(strip, Color(255, 0, 0))

            #if Gz<-1:
            #    theaterChase(strip, Color(255, 0, 0))
            

            #temp = sensor.get_temperature()
            #print(temp)
            #reset()
            #colour(temp)
            
            #colorWipe(strip, Color(0, 0, 255), 5)



            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print ('Theater chase animations.')
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print ('Rainbow animations.')
            #rainbow(strip)
            #theaterChaseRainbow(strip)
 
    except KeyboardInterrupt:
        #colorWipe(strip, Color(0,0,0), 10)
        GPIO.cleanup() # cleanup all GPIO