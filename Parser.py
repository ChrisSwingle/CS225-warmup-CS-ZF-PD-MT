import sys

globalFlag = True;
def main():
    #Let users know correct syntax to use and command to get full of commands
    sys.stdout.write("Type 'help' for a full list of commands and correct syntax\n")
    #Flag to end program. Set When user types 'exit'
    global globalFlag
    while globalFlag:
        getInput()

def getInput():
    sys.stdout.write(">>")
    userInput = input()
    processInput(userInput)

def processInput(userInput):
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

    #will validate data to and adjust for synonyms such as song --> title
    list = userInput.split()
    column = list[0].lower()
    column = column.capitalize()
    key = list[1].lower()
    key = key.capitalize()
    value = list[2]

    if(validateCol(column) and validateKey(key)):
        sys.stdout.write(value)

#This Function is not a complete list, more keys will be added to validKey array
def validateCol(str):
    validCols =  ["AvgValence","AvgDancability", "Rating","Rank", "Title", "Artist", "Genre", "Danceability", "Valence"]
    for i in range(len(validCols)):
        if (validCols[i] == str):
            return True
    return False

#This Function is not a complete list, more keys will be added to validKey array
def validateKey(str):
    validKeys = ["Title", "Artist"]
    for i in range(len(validKeys)):
        if (validKeys[i] == str):
            return True
    return False

def help():
    sys.stdout.write("exit : To exit program\n"
    "help : Full list of commands and correct syntax\n"
    "load data: Create database and load data from csv\n")

def loadData():
    x=1

if __name__ == '__main__':
    main()
