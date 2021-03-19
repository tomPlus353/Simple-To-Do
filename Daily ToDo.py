#Slightly more complex than "simple" version
#Simple version
##
#list of tuples of tasks with start time
#Q - does tuple support datetime object - YES(hours later - thank you ADHD-Sama!)
#Takes in list with start time.
#When task is done it is written into the text file with the total time taken.
#This can serve as function in more complex program.
##
#Current Version
#1. DONE - add menu.
#2. DONE - add dailies.
#3. DONE - add tomorrow's list (both Creation and Reading) 
#4. DONE - Add persistant datatypes (dailies(list of strings, no need for tuples yet), tomorrow's list(same), uncompleted tasks/leftover tasks)
#5. DONE -(see "Dolist") Allow for tasks not completed to be saved somehow and completed later.
#6. DONE - For both this version AND "SIMPLE" version - allow for aborting the loop if you can't complete all the tasks so you can at least update progress.
# -> Perhaps create a persistant list that can be reaccessed later in
# 7. DONE - For ALL versions, in "dolist" clean up that awful for loop(change to while?) and put in some imput validation.
# Also, consider a shrinking list. => actually this is easy... i = 0; then increment my one and print.
# 8. 
import datetime, time
import os
from calendar import month_name #list of 13 strings [0] = "", [1] = "January"

import shelve # For persistance: (dailies(list of strings, no need for tuples yet), tomorrow's list(same), uncompleted tasks/leftover tasks)

from progress.bar import ChargingBar
os.chdir('c:\\Users\\tomas\\Desktop\\Anti-Procrastination')


data = shelve.open('Persistant Data') #"dailies","tomorrowList","uncompleted","deadline"
if "dailies" not in list(data.keys()):
    data["dailies"] = []
dailies = data["dailies"]
if "tomorrowList" not in list(data.keys()):
    data["tomorrowList"] = []
tomorrowList = data["tomorrowList"]
if "uncompleted" not in list(data.keys()):
    data["uncompleted"] = []
uncompleted = data["uncompleted"]
if "deadline" not in list(data.keys()):
    data["deadline"] = []
deadline = data["deadline"]
print(dailies,tomorrowList, uncompleted,deadline)
data.close()

def menu(dailies,tomorrowList, uncompleted,deadline):
    menuList = ["Create new list.","Create list for tomorrow.","Load list made yesterday","Review current daily tasks","Add new daily tasks","See Uncompleted Tasks","Move Current Task to Long-Term Tasks","Create new tasks and add to Long-Term Task","Report completion of Long-Term Tasks","Exit"]
    choice = " "
    while choice:
        print("""Task List Creator:\n\nWhat would you like to do?\n""")
        print(f"You have {len(uncompleted)} regular tasks and {len(deadline)} Long-Term Tasks left.")
        for option in menuList:
            print(f"{menuList.index(option) + 1}. {option}")
        choice = input("Enter the number of your choice")
        isValid = False # user input must meet certain criteria to change this to True and escape the loop
        while isValid == False:
            if choice.isalpha() == False and choice.isdecimal() == True:
                if int(choice) in range(1,len(menuList)+1):
                    isValid = True
                    continue
                else:
                    print("Your number is out of range. Try again.")
            else:
                print("Not a positive number. Enter a number")
            choice = input("Enter the number of your choice")
        choice = menuList[int(choice)-1] #switch out index for string
        #actual selection. Careful when adding new menu options as we are using changable list indexes, not dictionary keys.
        if choice == menuList[0]:
            completedList, uncompleted, deadline = quickList(uncompleted)
            print(f"You have {len(uncompleted)} tasks left")
            syncUncompleted(uncompleted)
        elif choice == menuList[1]:
            tomorrowList = buildTomorrow(tomorrowList)
            #saves data to the shelve
            syncTomorrow(tomorrowList)
            print("List for tomorrow saved to database.")
        elif choice == menuList[2]:
            completedList, uncompleted = doList(tomorrowList,uncompleted) #tomorrow list becomes a regular "taskList" from this point on.
            syncUncompleted(uncompleted)
            print(f"You have {len(uncompleted)} tasks left")
            #Can we perhaps clean all this up? (12 lines is alot for a menu! let's try to get to less than 6!)
            tasksRemaining = [x for x in tomorrowList if x not in completedList]
            if len(tasksRemaining) == 0:
                print("Congrats. You completed all items on the the list")
            else:
                print(f"You completed {len(completedList)} and have {len(tasksRemaining)}.")
            answer = ""
            while answer != "y" or answer.lower() != "n":
                answer = input("Are you finished with this list? \nEnter [y] to delete this list.\nEnter [n] to return to the main menu.")
                if answer.lower() == "y":
                    tomorrowList.clear()
                    syncTomorrow(tomorrowList)
                    print("List deleted")
                    time.sleep(0.8)
                    break
                elif answer.lower() == "n":
                    break
        elif choice == menuList[3]:
            dailies = reviewDailies(dailies)
        elif choice == menuList[4]:
            dailies = addDailies(dailies)
        elif choice == menuList[5]:
            for task in uncompleted:
                print(f"{uncompleted.index(task) + 1}. {task[0]}")
            print(f"You have {len(uncompleted)} tasks left")
            time.sleep(2)
        elif choice == menuList[6]:
            deadline, uncompleted = moveToLongList(deadline, uncompleted)
        elif choice == menuList[7]:
            deadline = appendLongList(deadline)
        elif choice == menuList[8]:
            deadline = doLongList(deadline)
        elif choice == menuList[9]:
            print("Exiting program")
            break #exit has been pressed
        
    
def autoAdd(d,u,t):
    #adds daily tasks and uncompleted tasks
    t = autoDailies(t,d)
    t = autoDeadline(t)
    counter = 0
    #for u, it's a bit different as tasks in u have a datetime stamp already
    print(f"You have {len(uncompleted)} uncompleted tasks left from last time")
    for task in u:
        if task[0] in [task2[0] for task2 in t]:
            t.append((task[0] + str(len([task[0] in t]) + 1),task[1]))
            print(f"{task[0]} is added to your new list.\n->It was originally added at {task[1]}.")
            counter += 1
            time.sleep(0.1)
        else:
            t.append((task))
            print(f"{task[0]} is added to your new list.\n->It was originally added at {task[1]}.")
            counter += 1
            time.sleep(0.1)
    print(f"{counter} previously uncompleted tasks added out of {len(u)}")
    return t

def autoDailies(t,d):
    counter = 0
    yesOrNo = input(f"Do you wish to add your {len(d)} dailies?")
    while yesOrNo.lower() not in ['yes','y','no','n']:
        yesOrNo = input(f"Do you wish to add your {len(d)} dailies?")
    if yesOrNo.lower() in ["yes","y"]:
        for task in d:
            t.append((task,microSecSlicer(datetime.datetime.now())))
            print(f"{task} is added to your tasks at {microSecSlicer(datetime.datetime.now())}.")
            counter += 1
            time.sleep(0.1)
    print(f"{counter} Dailies added out of {len(d)}")
    return t

def autoDeadline(t): #tasklist
    now = microSecSlicer(datetime.datetime.now())
    startingLength = len(t)
    global deadline
    d = deadline.copy()
    for task in deadline:
        if task[1] <= now:
            print(f'Your task {task[0]} is due.')
            print(f'This task was due {now-task[1]} ago. So let\'t do this one first. Moving to top of your list.')
            time.sleep(1)
            t.insert(0,task)
            d.remove(task)
            print('Added to the top of your list.')
            time.sleep(0.3)
    if len(t)-startingLength == len(deadline)-len(d): # ie the task added to t and removed from d should be the same
        deadline = d # change should affect global variable
        syncDeadline(deadline) # sync to database
        print('Deadlines removed from database. Remained deadlines: ', len(deadline))
    else:
        print(f"length of t: {len(t)}\nstarting length: {startingLength}\nlength of deadlines{len(deadline)}\nlength of d{len(d)}")
        raise ArithmeticError
    return t
    
# this code results in duplication when a list is saved for later
##def crossOffDeadline(task,deadline): #Reduces the deadlineList if task in said list
##    for eachTuple in deadline:
##        if task == eachTuple:
##            deadline.pop(deadline.index(eachTuple))
##            print(f"{task} moved from your list of deadlines.\nWell done!")
##            break 
##    syncDeadline(deadline)
##    return deadline
    

def buildList(uncompleted):
    print("Building List")
    time.sleep(0.3)
    taskList = []
    taskList = autoAdd(dailies,uncompleted,taskList)
    print("Add tasks. Enter \"stop\" when you are done.")
    time.sleep(0.3)
    testTuple = ("",None)
    while testTuple[0].lower() != "stop":
        testTuple = (input("what task do you want to add?"),microSecSlicer(datetime.datetime.now()))
        if testTuple[0].lower() == "stop":
            continue
        else:
            taskList.append(testTuple)
            print(f"{testTuple[0]} is added to your tasks at {testTuple[1]}.")
    return taskList

def buildTomorrow(tomorrowList):
    print("Building List for Tomorrow")
    time.sleep(0.3)
    if len(tomorrowList) > 0:
        print("You already have a list for tomorrow")
        print(f"Here are your {len(tomorrowList)} tasks.")
        for task in tomorrowList:
            print(f"{tomorrowList.index(task) + 1}. {task[0]}")
        answer = ""
        while answer.lower() != "y" or "n":
            answer = input("Do you want to delete and start over? \nEnter [y] to delete this list and build a new one.\nEnter [n] to return to the main menu.")
            if answer.lower() == "y":
                tomorrowList.clear()
                print("List deleted")
                buildTomorrow(tomorrowList)
            #no need for else statement, the program will revert back to while loop in menu if the answer is "n"
    else:
        tomorrowList = autoAdd(dailies, uncompleted, tomorrowList)
        print("Add tasks. Enter \"stop\" when you are done.")
        time.sleep(0.3)
        testTuple = ("",None)
        while testTuple[0].lower() != "stop":
            testTuple = (input("what task do you want to add?"),microSecSlicer(datetime.datetime.now()))
            if testTuple[0].lower() == "stop":
                continue
            else:
                tomorrowList.append(testTuple)
                print(f"{testTuple[0]} is added to your tasks at {testTuple[1]}.")
        if len(tomorrowList) > 0:
            return tomorrowList
        else:
            print("No items added to your list for tomorrow")

def doList(taskList, uncompleted):
    ###NOTE - ADAPT this code to return UNCOMPLETED tasks - DONE
    global deadline
    if len(taskList) == 0:
        taskList.append(('Take it easy and finish a to-do list with no tasks!',microSecSlicer(datetime.datetime.now())))
    print("Do tasks on list")
    print(f"""Here are your tasks. Enter the number of the task when you complete it:""")

    for task in taskList:
        print(f"{taskList.index(task) + 1}. {task[0]}")

    completedTasks = []

    with ChargingBar(max=len(taskList)) as bar:   #the actual loop where user completes tasks
        while len(taskList) != len(completedTasks):
            update = input("\nEnter number of completed task: \n")
            if update.lower() == "stop":
                add2Uncompleted = [task for task in taskList if task not in completedTasks]
                if len(add2Uncompleted) == len(taskList) - len(completedTasks):
                    uncompleted = add2Uncompleted
                    syncUncompleted(uncompleted)
                    print("The following uncompleted tasks will been added to your database. They will be loaded next time you create a list.")
                    counter = 0 # this allows for a shrinking list of remaining tasks, which is better for motivation.
                    for task in uncompleted:
                        counter += 1
                        print(f"{counter}. {task[0]}")
                    return completedTasks, uncompleted, deadline
                else:
                    input("Something went wrong. Save your uncompleted tasks into a text file manually.\nPress enter when you are done.")
                    raise ArithmeticError
            elif update.lower() == 'focus':
                light = 'green'
                while light == 'green':
                    update2 = input('Select the task to focus on with timer')
                    if update2.isdecimal() == True:
                        if int(update) in range(len([task for task in taskList if task not in completedTasks])):
                            light = 'red'
                timer([task for task in taskList if task not in completedTasks][int(update2)])
                continue #user will still have to knock off the main task by themselves when they are done with the timer
            elif update.lower() == 'sublist':
                light = 'green'
                while light == 'green':
                    update2 = input('Select the task to focus on with a sublist')
                    if update2.isdecimal() == True:
                        if int(update) in range(len([task for task in taskList if task not in completedTasks])):
                            light = 'red'
                subList([task for task in taskList if task not in completedTasks][int(update2)])
                continue
            elif update.isdecimal() == True:
                #essentially we are accessing the phantom list: "tasks in taskList but not in completedTasks"
                update = int(update) - 1 # recieves reference to the phantom list
                taskToUpdate = [task for task in taskList if task not in completedTasks][update] # needs to be assigned before we alter the phantomlist in next line
                completedTasks.append(taskToUpdate) #NOTE, THIS MODIFIES THE PHANTOM LIST
                updateLog(taskToUpdate) #updates log once task has been logged to the system
                checkAllDailies(dailies,completedTasks)
                counter = 0 #provides reference to the phantom list
                print("Remaining tasks:")
                for task in taskList:
                    if task not in completedTasks:
                        counter += 1
                        print(f"{counter}. {task[0]}")
                bar.next()
                print('\n')

            else:
                continue
    if len(completedTasks) == len(taskList):
        print("All tasks completed")
        uncompleted.clear()
        bar.finish()
        syncUncompleted(uncompleted)
        print(f"You have {len(uncompleted)} tasks left")
    elif len(completedTasks) > len(taskList):
        print("Something went wrong, length of length of completed Tasks is higher than the actual task list!")
        print(f"You have {len(uncompleted)} tasks left")
    elif len(completedTasks) < len(taskList):
        print("not all tasks completed")
        print(f"You have {len(uncompleted)} tasks left")
    return completedTasks, uncompleted, deadline

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

def subList(task):
    subTasks = []
    entry = ""
    while entry.lower() != "stop":
        entry = (input("what task do you want to add?"))
        if entry.lower() == "stop":
            continue
        else:
            subTasks.append(entry)
            print(f"{entry} is added to your sublist for {task[0]}.")
    update = None
    with ChargingBar(max=len(taskList)) as bar:
        while len(subTasks) > 0:
            for subTask in subTasks:
                print(f"{subTask.index(subTask) + 1}.{subT}")
            update = input('Enter the number of sub-task completed.')
            if update.isnum() == True:
                if int(update) in range(1,len(subTasks)+1):
                    subTasks.remove()


def doLongList(deadline):
    taskNum = ""
    while len(deadline) > 0:
        for task in deadline:
            print(f"{deadline.index(task)+1}. {task[0]}\nDate Due: {task[1]}")
        taskNum = input("Enter the number of the task you have completed. Enter /stop/(lower case) to return to main menu.")
        if taskNum == 'stop':
            return deadline
        valid = False
        while valid == False:
            if taskNum.isdecimal() == True:
                if int(taskNum) in range(1,len(deadline)+1):
                    taskNum = int(taskNum) - 1
                    valid = True #breaks loop if input is number and in range of the length of deadline
                    continue
            taskNum = input("Enter the number of the task you have completed. Enter /stop/(lower case) to return to main menu.")
        updateLog(deadline[taskNum])
        deadline.pop(taskNum)
        syncDeadline(deadline)
    return deadline
        

#three syncing methods for making any change to these variables persistant and keeping the database closed when not necessary
def syncTomorrow(tomorrowList):
    data = shelve.open('Persistant Data')
    data['tomorrowList'] = tomorrowList
    data.close()
    print('List for tomorrow synced to database')
def syncDailies(dailies):
    data = shelve.open('Persistant Data')
    data['dailies'] = dailies
    data.close()
    print('Dailies synced to database')
def syncUncompleted(uncompleted):
    data = shelve.open('Persistant Data')
    data['uncompleted'] = uncompleted
    data.close()
    print('Uncompleted tasks synced to database')
def syncDeadline(deadline):
    data = shelve.open('Persistant Data')
    data['deadline'] = deadline
    data.close()
    print('Deadlines synced to database')

#functions relating to CRUD for dailies below
def reviewDailies(dailies): #read and delete individual elements
    answer = ''
    while answer != "stop":
        print("Current dailies")
        for task in dailies:
            print(f"{dailies.index(task) + 1}. {task}")
            if len(dailies) == 0:
                print("Sorry, no dailies found")
        answer = input("Enter \"stop\" to exit. Or enter the number of a daily to DELETE.")
        if answer.lower() == "stop":
            continue
        elif int(answer) -1  in range(0,len(dailies)): #Bug fix, etch int(answer) -1 in range(ZERO,len(dailies)) NO INCREMENT into your skin
            dailies.pop(int(answer) - 1)
    syncDailies(dailies)
    return dailies

def addDailies(dailies):
    newTask = ""
    while newTask.lower() != "stop":
        newTask = input("What task do you want to add?(enter \"stop\" to return to main menu.)")
        if newTask.lower() == "stop":
            continue
        else:
            dailies.append(newTask)
            print(f"{newTask} is added to your daily tasks.")
    syncDailies(dailies)
    print("Dailies synced to database")
    return dailies

#adds tasks with a specific deadline
def moveToLongList(deadline, uncompleted): #moves items from uncompleted to longlist
    answer = ''
    while answer != "stop":
        print("Current uncompleted tasks.")
        for task in uncompleted:
            print(f"{uncompleted.index(task) + 1}. {task[0]}: Date Added: {task[1]}")
            if len(uncompleted) == 0:
                print("Sorry, no tasks found")
        answer = input("Enter \"stop\" to exit. Or enter the number of the task you wish to move to long list.")
        if answer.lower() == "stop":
            continue
        elif int(answer) - 1 in range(len(uncompleted)):
            taskNoDeadline = uncompleted[int(answer)-1][0]
            user_deadline = getDeadline()
            taskWithDeadline = (taskNoDeadline,user_deadline)
            deadline.append(taskWithDeadline)
            uncompleted.pop(int(answer) - 1)
            print(f"{taskWithDeadline[0]} added to long term tasks. Your deadline is {taskWithDeadline[1]}\n")
    syncDeadline(deadline)
    syncUncompleted(uncompleted)
    return deadline, uncompleted

def appendLongList(deadline):
    print("Current Deadlines")
    for task in deadline:
            print(f"{deadline.index(task) + 1}. {task[0]}: Deadline: {task[1]}")
    newTask = ""
    while newTask.lower() != "stop":
        newTask = input("What task do you want to add?(enter \"stop\" to return to main menu.)")
        if newTask.lower() == "stop":
            continue
        else:
            user_deadline = getDeadline()
            taskWithDeadline = (newTask,user_deadline)
            deadline.append(taskWithDeadline)
            print(f"{taskWithDeadline[0]} added to long term tasks. Your deadline is {taskWithDeadline[1]}\n")
    syncDeadline(deadline)
    print("Deadlines synced to database")
    return deadline

def getDeadline():
    print("Choose your deadline")
    now = microSecSlicer(datetime.datetime.now())
    possDeadlines = {"year": datetime.timedelta(days=365), "month": datetime.timedelta(days=31), "week": datetime.timedelta(weeks=1), "day": datetime.timedelta(days=1)}
    userInput = input("Choose how long you need to do the task.\n/year/\n/month/\n/week/\n/day/\n/other/")
    if userInput.lower() not in list(possDeadlines.keys()) + ['other']:
        print('Incorrect input')
        date1 = getDeadline()
        return date1
    elif userInput.lower() == 'other':    
        light = 'green'
        while light == 'green':
            try:
                print("Setting deadline...")
                time.sleep(0.3)
                year = int(input('Enter a year'))
                month = int(input('Enter a month(no.1-12)'))
                day = int(input('Enter a day'))
                hour = int(input('Enter an hour(0-23)'))
            except ValueError:
                print("Incorrect input")
                continue
            else:
                conditions = [False if month == 2 and day not in range(1,29) else True, month in range(1,13), day in range(1,32), day in range(1,31) if month in [4,6,9,11] else True]
                if all(conditions):
                    date1 = datetime.datetime(year, month, day, hour)
                    if isinstance(date1, datetime.datetime):
                        light = 'red'
                        return date1
                else:
                    print("Not in specified range!")
    else:
        date1 = now + possDeadlines[userInput]
        return date1
            
        

def updateLog(task):
    #4 parts open file corresponding to today - DONE write to file - DONE check if all dailies are completed - DONE(moved to separate function) close file DONE
    #no need to return anything
    description = input(f'Enter your description of the following task: \"{task[0]}\"\n')
    now = microSecSlicer(datetime.datetime.now())
    timeTaken = now - task[1]
    title = f'Todo list - quicklist - {now.year}-{now.month}-{now.day}.txt'
    todo = open(title, 'a')
    todo.write(f"{task[0]} - TASK COMPLETE\nIt took you(d, h:m:s): {timeTaken}\n=>Task desciption: {description}\n")
    todo.close()
    print("Closed text log.")
    

def checkAllDailies(dailies,completed):
    #if completed tasks(including this task are in dailies: print(affirmation that you did well)
    #-> How do I get this logic? - convert completed to a list of strings, add current task, then create a list of completed dailies, if len = len(dailies) then print your message
    #note: will compare length because order matters:
    """ >>> ab = ['a','b']
        >>> ba = ['b','a']
        >>> ab == ba
        False
    """
    #note2: will use set() to remove potential duplicates
    completedList = []
    for t in completed:
        completedList.append(t[0])
    completedDailies = set([t for t in completedList if t in dailies])
    if len(completedDailies) == len(dailies):
        print('Well Done, you completed all daily tasks!')
        now = microSecSlicer(datetime.datetime.now())
        todo = open(f'Todo list - quicklist - {now.year}-{now.month}-{now.day}.txt', 'a')
        todo.write(f'Well Done! You completed all {len(dailies)} daily tasks')
        print(f'Well Done! You completed all {len(dailies)} daily tasks')
        todo.close()
        print("Closed text log.")


def quickList(uncompleted): # builds list from scratch and then completes it by combining two functions.
    completedList, uncompleted, deadline = doList(buildList(uncompleted), uncompleted)
    print(f"You have {len(uncompleted)} tasks left")
    return completedList, uncompleted, deadline

def microSecSlicer(datetimeObject):
    datetimeString = str(datetimeObject)
    datetimeString = datetimeString[0:datetimeString.find(".")]
    datetimeObject = datetime.datetime.strptime(datetimeString, "%Y-%m-%d %H:%M:%S")
    return datetimeObject

menu(dailies,tomorrowList,uncompleted,deadline)
