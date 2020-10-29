import RPi.GPIO as g
from time import sleep as s
import curses
import os
import time
g.setwarnings(False)

#start the setmode to name the pins we want to use on rpi
#pins are in board mode, NOT BCM LABELED
g.setmode(g.BOARD)
#setup the gpio pins with setup
#make pin3 output the pulse width modulation(pwm)
#type of digital signal to control direction of servo
g.setup(3, g.OUT)
#set hz to 50 on pin3 which is a digital signal and call it new var pulse
pulse = g.PWM(3, 50)
#make duty cycle start at 0
pulse.start(0)

#make my window box
#this is nice b/c its clear the program is ok and waiting for button push
stdscr = curses.initscr()
#do not display buttons pushed
curses.noecho()
#turn on instant (no waiting) key response
#cbreak disables line buffering allowing chars typed to be instantly avail to program
curses.cbreak()
#allows use of arrow keys
stdscr.keypad(True)


#myFunc for open/close = oc
def oc(direction):
    #calculation for duty%
    #the duty cycle is the percentage of time the signal is on compared to off
    #info @ learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
    #num regulates voltage or some type of power to the servo
    #desired direction given will produce value in acceptable range for servo sensitivity
    num = direction / 18 + 2
    #enable pin3 for output
    g.output(3, True)
    #use that num with changedutycycle from rpi.gpio to do exactly that
    pulse.ChangeDutyCycle(num)
    s(1) #sleep 1 sec. #time to make the move
    g.output(3, False) #pin3 no longer an output
    pulse.ChangeDutyCycle(0)
    #no more pulse
     
    
try:
    while True:
        #key pushed gets new var button
        button = screen.getch() 
        #projector must be switched on.  this servo controls the shutter
        #f is for the "f" in off
        #135 / 18 + 2 is 9.5 which is the strength of the pulse required to move to the angle 135.
        #which should be the off position but budget servos sometimes need help. so i and d with inc/dec (from below) 
        if button == ord("f"):
            oc(120) #use my func
        #n is for the "n" in on
        #48 moves the shutter to a position i like and does not obstruct laser.
        elif button == ord("n"):
            oc(48) #use my func
        elif button == ord("x"):
            break
        
finally:
    #restore curses back to normal
    #show key strokes on screen again
    #buttons are resotred to default
    curses.nocbreak()
    #put the keys back to how they were.  arrow keys are back to normal
    stdscr.keypad(False)
    #show button press as usual once again
    curses.echo()
    #make sure to restore to normal operating mode
    curses.endwin()    
    #ensure there are not still pulses/digital signals being output
    pulse.stop()
    #ensure there are not still pulses/digital signals being output
    #reset gpio status across all 40 pins(strictly from rpi.gpio assigned pins)
    g.cleanup()
    
