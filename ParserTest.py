import sys

globalFlag = True;
def main():
    #Let users know correct syntax to use and command to get full of commands
    printCommands()
    #Flag to end program. Set When user types 'exit'
    global globalFlag
    while globalFlag:
        sys.stdout.write(">>")
        userInput = input()
        determineInput(userInput)


def determineInput(userInput):
    if userInput == "help":
        help()
    elif userInput == "exit" :
        global globalFlag
        globalFlag = False
    elif userInput =="load data":
        loadData()
    else :
        parse(userInput)

def parse(userInput):
    #This function will break up user input into seperate pieces
    #of data that will be used to query from the database
    list = userInput.split()
    print(list)

def loadData():
    x=1
def printCommands():
    sys.stdout.write("Type 'help' for a full list of commands and correct syntax\n")

def help():
    sys.stdout.write("exit : To exit program\n"
    "help : Full list of commands and correct syntax\n"
    "load data: Create database and load data from csv\n")

if __name__ == '__main__':
    main()
