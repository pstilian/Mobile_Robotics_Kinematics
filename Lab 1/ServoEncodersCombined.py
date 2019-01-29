# This program demonstrates usage of the servos.
# Keep the robot in a safe location before running this program,
# as it will immediately begin moving.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.
# For full information on this project see the Git Repo at https://github.com/pstilian/Mobile_Robotics_Kinematics.git

import time
import Adafruit_PCA9685
import signal
import math
import RPi.GPIO as GPIO
import signal

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second.
LSERVO = 0
RSERVO = 1

#Used Values
lCount = 0
rCount = 0
TotalCount = (0,0)
lSpeed = 0
rSpeed = 0
lRevolutions = 0
rRevolutions = 0
startTime = time.time()
currentTime = 0

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library, 
# the value must be divided by 20 and multiplied by 4096.
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    global lCount, lRevolutions, lSpeed, currentTime
    lCount += 1
    lRevolutions = float(lCount / 32)
    currentTime = time.time() - startTime
    lSpeed = lRevolutions / currentTime

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    global rCount, rRevolutions, rSpeed, currentTime
    rCount += 1
    rRevolutions = float(rCount / 32)
    currentTime = time.time() -startTime
    lSpeed = rRevolutions / currentTime

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    print("Exiting")

    GPIO.cleanup()    
    # Write an initial value of 1.5, which keeps the servos stopped.
    # Due to how servos work, and the design of the Adafruit library, 
    # The value must be divided by 20 and multiplied by 4096.
    pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096));
    pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096));

    exit()

#Resets the tick count
def resetCounts():
    Lcounts = 0
    Rcounts = 0

#Returns the previous tick counts as a touple
def getCounts():
    return ( lCount, rCount)

#Returns instantious speeds for both left and right wheels as a touple
def getSpeeds():
    global lCount, rCount, currentTime, lSpeed, rSpeed
    currentTime = time.time() -startTime
    lSpeed = ( lCount / 32 ) / currentTime
    rSpeed = ( rCount / 32 ) / currentTime
    return ( lSpeed, rSpeed)

#Function that sets up and initializes the econders for the robot
def initEncoders():
    # Set the pin numbering scheme to the numbering shown on the robot itself.
    GPIO.setmode(GPIO.BCM)
    # Set encoder pins as input
    # Also enable pull-up resistors on the encoder pins
    # This ensures a clean 0V and 3.3V is always outputted from the encoders.
    GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Attach a rising edge interrupt to the encoder pins
    GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
    GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)

#This function changes the values from 1.5 - 1.7 to 1.5-1.3 basically outputting inverse pwm values 
def setDifference(speed):
    diff = speed - 1.5
    return 1.5 - diff

#This function creates a calibration map comparing the servo input to output based on microseconds
#Measures the speeds of each wheel based on different input values 
def calibrateSpeeds():

    #Initial start pwm value is at complete stop
    startVar = 1.5

    #Loop runs starting from full stop to full speed in the forward direction
    #LSERVO runs from 1.5 to 1.3 (with 1.3 being max forward pwm)
    #RSERVO runs from 1.5 to 1.7 (with 1.7 being max forward pwm)
    while startVar < 1.71: 
        pwm.set_pwm(LSERVO, 0, math.floor( setDifference(startVar) / 20 * 4096));
        pwm.set_pwm(RSERVO, 0, math.floor(startVar / 20 * 4096));
        time.sleep(1)

        #Print out speed corresponding to pwm values
        print (startVar, getSpeeds())
        time.sleep(1)

        #Increment loop
        startVar += 0.01

        #Reset counts for next loop!
        ENCODER.resetCounts()

# How do we get the above code to write into a map?? ***********************************

#Sets speed of motors in revolutions per second
def setSpeedsRPS(rpsLeft, rpsRight):
    # needs to convert from RPS to PWM values

#Sets speed of motors in Inches per econd
def setSpeedsIPS(ipsLeft, ipsRight):

#Function sets speed of robot to move over a linear speed with a set angular velocity
# v = inches per second         w = angular velocity
# positive w values spin counterclockwise       negative w values spin clockwise
def setSpeedsvw(v, w):


