from time import sleep as s
import curses
import os
import RPi.GPIO as g
#import for gpio pins and time to sleep
from picamera import PiCamera, Color
g.setwarnings(False)
cam = PiCamera()

#start the setmode to name the pins we want to use on rpi
#pins are in board mode, NOT BCM LABELED
g.setmode(g.BOARD)
#make pin3 output the Pulse Width Modulation(pwm)
#type of digital signal to control direction of servo
g.setup(3, g.OUT)
g.setup(11, g.OUT)
#I set my hz to 55; 50 is reccomended.
#tested values from 40 - 60
#value set to pin3
#make variable pulse for this pin with this value in Hz
p3 = g.PWM(3, 55)
p11 = g.PWM(11, 45)
#make duty cycle start at 0, only once function is called
p3.start(0)
p11.start(0) #make duty cycle start at 0

#myFunc Look with argument direction
def Look3(direction):   
    #calulation for duty% make variable for it called num
    #the duty cycle is the percentage of time the signal is on compared to off
    #info @ learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
    num = direction / 18 + 2
    #enable pin3 for output
    g.output(3, True)
    #use ChangeDutyCycle from rpio.gpio to change duty cycle to num 
    p3.ChangeDutyCycle(num)
    #sleep for time to turn
    s(1)
    #un-enable pin 3 as output
    #is that a word? i i think it describes what i mean 
    g.output(3, False)
    #put it back to zero
    p3.ChangeDutyCycle(0)

def Look11(direction):
    #only once function is called
    #calulation for duty% make variable for it called num
    #the duty cycle is the percentage of time the signal is on compared to off
    #info @ learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
    num = direction / 18 + 2
    #enable pin3 for output
    g.output(11, True)
    #use ChangeDutyCycle from rpio.gpio to change duty cycle to num 
    p11.ChangeDutyCycle(num)
    #sleep for time to turn
    s(1)
    #un-enable pin 11 as output
    #is that a word? i i think it describes what i mean 
    g.output(11, False)
    #put it back to zero
    p11.ChangeDutyCycle(0)

def position(horz, vert, flip, val):
    cam.resolution = (1280, 720)
    style = ["negative", "colorswap", "washedout", "solarize", "deinterlace2", "watercolor", "negative"]
    msg = ["Any A.I.", "Smart enough", "To pass", "a Turing test", "is Smart enough", "to know", "to Fail it!"]
    #quote from "Ian McDonald"
    Look3(horz)
    s(.2)
    Look11(vert)
    cam.rotation = (flip)
    cam.start_preview()
    cam.image_effect = style[(val)]
    cam.annotate_text_size = 90   #adjust number
    cam.annotate_text = msg[(val)]
    s(6)
    cam.capture("/home/pi/Desktop/{}{}.jpg".format((val),style[(val)]))
    cam.stop_preview()
    s(1)

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

        #x is for exit. used to absolutely stop
        #i prefer to use break as my failsafe
        if button == ord("x"):
            break
        #all the ord... return the integer representing the unicode char in ("")
        if button == ord("t"):  #one char string, if lowercase t is pushed
            #terminate
            #python script runing linux command for shutdown now
            #sudo is for super user do
            #now or -0 is the same, could have used -p, -f or -h
            os.system ('sudo shutdown -h 0')

        elif button == ord("a"):            #name
            position(45, 25, 270, 0)    #position(45, 25, 270, 1)
            position(100, 45, 270, 1)   #position(45, 25, 270, 2)
            position(180, 160, 90, 2)   #position(45, 25, 270, 3)
            position(50, 45, 270, 3)    #position(45, 25, 270, 1)
            position(20, 155, 90, 4)    #position(45, 25, 270, 5)
            position(160, 60, 270, 5)    #position(45, 25, 270, 1)
            position(35, 40, 270, 6)    #position(45, 25, 270, 7)

        elif button == ord("0"):
            position(45, 25, 270, 0)    #position(45, 25, 270, 1)

        elif button == ord("1"):
            position(100, 45, 270, 1)   #position(45, 25, 270, 2)

        elif button == ord("2"):        
            position(150, 150, 90, 2)   #position(45, 25, 270, 3)

        elif button == ord("3"):
            position(50, 45, 270, 3)    #position(45, 25, 270, 1)

        elif button == ord("4"):
            position(40, 155, 90, 4)    #position(45, 25, 270, 5)

        elif button == ord("5"):
            position(70, 60, 270, 5)    #position(45, 25, 270, 1)

        elif button == ord("6"):
            position(40, 40, 270, 6)    #position(45, 25, 270, 7)
            
        #Nobody can be told what the matrix is, you have to see it for yourself.
        #If real is what you can feel, smell, taste and see.
        #then 'real' is simply electrical signals interpreted by your brain.  Morpheus
        elif button == ord("m"):
            os.system('cmatrix')  #favorite linux command is run by this python code
        #for linux.. "sudo apt-get install cmatrix"   or
        #mac users...   "brew install cmatrix"
        #homebrew for your mac with:            
        #/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" """
        elif button == ord("c"):
            cam.capture('/home/pi/Desktop/image.jpg')
            
finally:
    #restore curses back to normal
    #show key strokes on screen again
    #buttons are resotred to default
    curses.nocbreak()
    #put the keys back to how they were.  arrow keys are back to normal
    window.keypad(False)
    #show button press as usual once again
    curses.echo()
    #make sure to restore to normal operating mode
    curses.endwin()    
    
    cam.close()
    #saftey for my pi
    #ensure to not send anymore pulses
    p3.stop()
    p11.stop()
    #undo any changes to gpio
    g.cleanup()


