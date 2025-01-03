#barebones task list
#list of tuples of tasks with start time
#Q - does tuple support datetime object - YES
#Takes in list with start time.
#When task is done it is written into the text file with the total time taken.
import datetime, time
import os
from progress.bar import ChargingBar
#import shelve # perhaps use later

def buildList():
    print("Building List")
    time.sleep(0.3)
    print("Enter stop when you are done.")
    time.sleep(0.3)
    taskList = []
    testTuple = ("",None)
    while testTuple[0].lower() != "stop":
        testTuple = (input("what task do you want to add?"),microSecSlicer(datetime.datetime.now()))
        if testTuple[0].lower() == "stop":
            continue
        else:
            taskList.append(testTuple)
            print(f"{testTuple[0]} is added to your tasks at {testTuple[1]}.")
    return taskList

def doList(taskList):
    print("Do tasks on list")
    print(f"""Here are your tasks. Enter the number of the task when you complete it:""")

    for task in taskList:
        print(f"{taskList.index(task) + 1}. {task[0]}")

    completedTasks = []
    os.chdir('c:\\Users\\tomas\\Desktop\\Anti-Procrastination')
    now = datetime.datetime.now()
    path = f'Todo list - quicklist - {now.year}-{now.month}-{now.day}.txt'
    todo = open(path, 'a')
    todo.write(f"\n\nThe date is {now.month} and you have {len(taskList)} tasks to finish!\n")
    #bar = ChargingBar('Status', max=len(taskList))
    print('\n')
    with ChargingBar(max=len(taskList)) as bar:
        for i in range(len(taskList)):
            update = int(input("Enter number of completed task: \n")) - 1
            now = microSecSlicer(datetime.datetime.now())
            timeTaken = now - taskList[update][1]
            todo.write(f"{taskList[update][0]} - TASK COMPLETE\nIt took you(hours:minutes:seconds): {timeTaken}\n")
            completedTasks.append(taskList[update])
            bar.next()
            print("\nRemaining tasks:")

            for task in taskList:
                if task not in completedTasks:
                    print(f"{taskList.index(task) + 1}. {task[0]}")
            
    if len(completedTasks) == len(taskList):
        print("all tasks completed")
    else:
        print("something went wrong, length of tasklist and length of completedTasks do not match")
    todo.close()
    print("closing file...")

def quickList(): # runs through parts 1 and 2 as a unit
    doList(buildList())

def microSecSlicer(datetimeObject):
    datetimeString = str(datetimeObject)
    datetimeString = datetimeString[0:datetimeString.find(".")]
    datetimeObject = datetime.datetime.strptime(datetimeString, "%Y-%m-%d %H:%M:%S")
    return datetimeObject


quickList()
