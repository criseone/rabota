import sys
import threading
import OSC
import time
import random

# Settings
sendAdress = '0.0.0.0', 8000
stepTime = 1
maxRandomTurnMultiplier = 2
motorSpeed = 100
leftWheelPolarity = 1
rightWheelPolarity = 1



def process_message(address, value=0):
    message = OSC.OSCMessage()
    message.setAddress(address)
    message.append(value)
    client.send(message)


def goForward():
    print 'goForward'
    process_message('/rightwheelspeed', motorSpeed * rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * leftWheelPolarity)


def turnRight():
    print 'turnRight'
    process_message('/rightwheelspeed', motorSpeed * -rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * leftWheelPolarity)

def turnLeft():
    print 'turnLeft'
    process_message('/rightwheelspeed', motorSpeed * rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * -leftWheelPolarity)

def randomTurn():
    print 'randomTurn'
    if (random.randint(0,1) == 0):
        turnRight()
    else: 
        turnLeft()

    time.sleep(random.random() * maxRandomTurnMultiplier);

def stop():
    print 'stop'
    process_message('/stop')


# Init OSC client
client = OSC.OSCClient()
client.connect(sendAdress)



with open('data.txt') as inf:
    for line in inf:
        line = line.strip()
	if (line != ''):
	    print 'line read: ' + line
            if line == 'f':
                goForward()
            elif line == 'r':
                turnRight()
            elif line == 'l':
                turnLeft()
            elif line == 'm':
                randomTurn()
            elif line == 's':
                stop()
    	    time.sleep(stepTime)

stop()
print 'DONE'

