import sys
import time
import random
from pythonosc import udp_client

# Settings
sendAddress = '0.0.0.0'
sendPort = 8000
stepTime = 1
maxRandomTurnMultiplier = 2
motorSpeed = 100
leftWheelPolarity = 1
rightWheelPolarity = 1

client = udp_client.SimpleUDPClient(sendAddress, sendPort)

def process_message(address, value=0):
    client.send_message(address, value)

def go_forward():
    print('goForward')
    process_message('/rightwheelspeed', motorSpeed * rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * leftWheelPolarity)

def turn_right():
    print('turnRight')
    process_message('/rightwheelspeed', motorSpeed * -rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * leftWheelPolarity)

def turn_left():
    print('turnLeft')
    process_message('/rightwheelspeed', motorSpeed * rightWheelPolarity)
    process_message('/leftwheelspeed', motorSpeed * -leftWheelPolarity)

def random_turn():
    print('randomTurn')
    if random.randint(0, 1) == 0:
        turn_right()
    else:
        turn_left()
    time.sleep(random.random() * maxRandomTurnMultiplier)

def stop():
    print('stop')
    process_message('/stop')

with open('/home/rabota/rabota/data.txt') as inf:
    for line in inf:
        line = line.strip()
        if line != '':
            print('line read: ' + line)
            if line == 'f':
                go_forward()
            elif line == 'r':
                turn_right()
            elif line == 'l':
                turn_left()
            elif line == 'm':
                random_turn()
            elif line == 's':
                stop()
            time.sleep(stepTime)

stop()
print('DONE')
