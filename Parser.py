import sys

globalFlag = True;
def main():
    #Tells user how to access commands for program
    sys.stdout.write("Welcome. Type 'help' for a full list of commands and correct syntax\n")
    #Flag to end program
    global globalFlag
    while globalFlag:
        getInput()

def getInput():
    sys.stdout.write(">>")
    processInput(input())

def processInput(userInput):
    userInput = userInput.strip()
    if userInput.lower() == "help":
        help()
    elif userInput.lower() == "exit" or userInput.lower() == "quit":
        sys.stdout.write("Goodbye!")
        global globalFlag
        globalFlag = False
    elif userInput.lower() =="load data":
        loadData()
    else :
        parse(userInput)


#Parse function will break user input into three valid pieces of data to pass to query function
#Will validate input and only let user enter valid data.
def parse(userInput):
    try:
        #Split input into three distinct pieces, place in list
        list = userInput.split()
        #Standardize column string
        column = list[0].lower()
        column = column.capitalize()
        #Adjust for Possible synonyms in column string
        if column == "Song" or column == "Track":
            column = "Title"
        #Standardize key string
        key = list[1].lower()
        key = key.capitalize()
        #Adjust for Possible synonyms in key string
        if key == "Song" or key == "Track":
            key = "Title"
        #Add all values after first two arguments to value string
        #This will handle possiblilty of multi-word song name
        value =""
        for i in range(2,len(list)):
            value += (list[i] + " ")
        value = value.strip()

        #Validate that first two columns are valid inputs, then query, if not prompt user to input again
        if(validate(column) and validate(key)):
            sys.stdout.write("\n")
        else:
            sys.stdout.write("Please enter a valid command. Type: help for a complete list of commands\n"
            "the syntax of your argument may have been wrong, or too few arguments may have been passed\n")
            getInput()
    except IndexError:
        sys.stdout.write("Please enter a valid command. Type: help for a complete list of commands\n"
        "the syntax of your argument may have been wrong, or too few arguments may have been passed\n")
        getInput()


#This Function is not a complete list, more keys will be added to valid array
def validate(str):
    validInput =  ["AvgValence","AvgDancability","Rank", "Title", "Artist", "Genre", "Danceability", "Valence"]
    for i in range(len(validInput)):
        if (validInput[i] == str):
            return True
    return False
def help():
    sys.stdout.write("exit : To exit program\n"
    "help : Full list of commands and correct syntax\n"
    "load data: Create database and load data from csv\n\n"
    "Proper Syntax for Querying: <column> <key> <value>\n"
    "Ex : Rank Title Randsom - will return the 'Rank' of the song 'Titled' 'Randsom'\n ")

def loadData():
    x=1

if __name__ == '__main__':
    main()
