#test timer
import time, datetime
def timer(task): #input 
    print(f"Ok! Let's focus on your task: '{task[0]}'!")
    print("First, let's set a timer.")
    minutes = int(input('How many minutes?'))
    seconds = int(input('How many seconds?'))
    print(f"You have {minutes} minutes and {seconds} left to complete the task:'{task[0]}'!")
    timeRemaining = minutes * 60 + seconds
    while timeRemaining > -1:
            minutes, seconds = divmod(timeRemaining,60)
            print('Time remaining: {:2d}:{:2d}'.format(minutes,seconds),end="\r")
            time.sleep(1)
            timeRemaining -= 1
    print('Times up!')
task = ('Do the dishes',datetime.datetime.now())
timer(task)
