#import for gpio pins and time for sleep
#import curses for keyboard control and os to do linux commands with python code

from gpiozero import Robot
from time import sleep as s
import curses
import os
        
#these 4 numbers are corresponding to the gpio pinso on the raspberry pi
#they are then connected to the h bridge motor control
#motor control to ground, ground, power and dc motors. 
tank = Robot(left = (13, 6), right = (19, 26))

#make my window box
#this is nice b/c its clear the program is ok and waiting for button push
window = curses.initscr()
#do not display buttons pushed
curses.noecho()
#turn on instant (no waiting) key response
#cbreak disables line buffering allowing chars typed to be instantly avail to program
curses.cbreak()
#allows use of arrow keys
window.keypad(True)

try:
    while True:
        #key pushed gets new var button
        #from (curses.initscr) the window gets the character key clicked
        #getch() waits until a key is pressed
        button = window.getch()
        #all the ord... return the integer representing the unicode char in ("")
        if button == ord("t"):  #one char string, if lowercase t is pushed
            #terminate
            #python script runing linux command for shutdown now
            #sudo is for super user do
            #now or -0 is the same, could have used -p, -f or -h
            os.system ('sudo shutdown -h 0')
        #"sudo apt-get cmatrix" or "brew install cmatrix"  "or you have windows and good luck"
        """ Nobody can be told what the matrix is, you have to see it for yourself.    
                        If real is what you can feel, smell, taste and see.
            then 'real' is simply electrical signals interpreted by your brain.  #Morpheus"""
        if button == ord("m"):
            os.system ('cmatrix')  #favorite linux command is run by this python code
        #o is for on off button.
        #arrow keys are turned on for curses
        #but arrow is clicked and motion continues until changed typically by stop with enter key
        #these are not hold buttons for directions
        #if arrow up then use all 4 gpio pins to make both dc motors spin technically in opposite directions
        #but this will allow forward movement at full speed hence (1) is %100 unsure about 100+ ability
        #x is for exit. used to absolutely stop
        #i prefer to use break as my failsafe
        if button == ord("x"):
            break
        if button == ord("r"):
            os.system ('sudo reboot')
        elif button == curses.KEY_UP:
            tank.forward(1)
        #stop with enter use 10, 13 and KEY_ENTER (WIRELESS, MAC AND OTHER)
        #COULD RUN TESTS but best be sure for stop on all control source
        #key enter did not work, testing for 10
        elif button == 10:
            tank.stop()
        #same arrow key down for reverse/straight back at full speed
        elif button == curses.KEY_DOWN:
            tank.backward(1)
        #one back one forwards for turn right when right arrow key is pressed
        elif button == curses.KEY_RIGHT:
            #i imagine that 1 which is 100% is to fast
            #try 0.4-0.7 
            tank.right(.5) #adjust probably less
            #same for turn left with left arrow
            #left and right recent change to half speed for precission driving
        elif button == curses.KEY_LEFT:
            tank.left(.5)

finally:
    #restore curses back to normal
    #show key strokes on screen again
    #buttons are resotred to default
    curses.nocbreak()
    #put the keys back to how they were.  arrow keys are back to normal
    window.keypad(False)
    #show button press as usual once again
    curses.echo()
    #make sure to restore to normal operating mod    
    curses.endwin()
    
