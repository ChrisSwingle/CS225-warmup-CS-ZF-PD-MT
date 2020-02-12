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


#Parse function will break user input into seperate pieces of data to pass to query function:
#-If search lies within SongsTable, there should be 3 pieces of input:
#       Column(of song table), Key(specifier to narrow down search), Value(specifies row)
#-If search lies within ArtistsTable, there should be 4 pieces of input:
#       Column(of artist table), Foreign Key(artist), Foreign Key Value(artist name), Value(Song Title)

#Parser will first split on " " to obtain strings.
def parse(userInput):
    try:
        #Split on Quotes
        splitOnQuotes = userInput.split('"')
        #This logic will be for searches in the Songs Datatable
        if len(splitOnQuotes)==3:
            #Split on Spaces
            divList1 = splitOnQuotes[0].split()
            column = divList1[0]
            #divList1[1] is "of" which will be disguarded
            key = divList1[2]
            value = splitOnQuotes[1]
            #Standardize capitalization of column.
            column = column.lower()
            column = column.capitalize()
        #This logic will be for searches in the Artists Datatable
        elif len(splitOnQuotes) == 5:
            #Split on spaces
            divList1=splitOnQuotes[0].split()
            column = divList1[0]
            foreignKey = divList1[2]
            foreignVal = splitOnQuotes[1]
            divList2=splitOnQuotes[2].split()
            key = divList2[1]
            value = splitOnQuotes[3]
            #Standardize foreignKey
            foreignKey = foreignKey.lower()
            foreignKey = foreignKey.capitalize()
            #Adjust for Synonyms
            if foreignKey == "Singer" or foreignKey == "Artists" or foreignKey == "Author":
                foreignKey = "Artist"
        #Standardize capitalization among variables. The key will remain unchanged
        key = key.lower()
        key = key.capitalize()
        #Adjust for Possible synonyms in column string
        if column == "Song" or column == "Track":
            column = "Title"
        if column == "Singer" or column == "Artists" or column == "Author":
            column = "Artist"
        #Adjust for Possible synonyms in key string
        if key == "Song" or key == "Track":
            key = "Title"
        if key == "Singer" or key == "Artists" or key == "Author":
            key = "Artist"
        #Validate that first two columns are valid inputs, then query, if not prompt user to input again
        #This makes user of short circuit evaluation
        if((len(splitOnQuotes)==3 ) and ( validateCol(column) and validateKey(key))):
            sys.stdout.write("sqlQuery called with the following parameters:"+ column + "," + key +
            "," + value + "\n")
            sqlQuery(column, key, value)
        #Validate that inputs are valid
        #Only way to access Artist table is though foreign key, so this will require foreignKey to be "Artist"
        #and the value to be "Title"
        elif((len(splitOnQuotes)==5) and ((foreignKey == "Artist") and (key=="Title") and validateCol(column))):
            sys.stdout.write("sqlQuery called with following paramerters:" + column + "," + foreignKey +
            "," + foreignVal + "," + key + ","+ value+"\n\n")
            sqlQuery(column, foreignKey, foreignVal)

        #If this point is reached, Input is invalid
        else:
            sys.stdout.write("Please enter a valid command. Type: help for a complete list of commands\n"
            "the syntax of your argument may have been wrong, or too few arguments may have been passed\n")
            getInput()
    except IndexError or UnboundLocalError:
        sys.stdout.write("Please enter a valid command. Type: help for a complete list of commands\n"
        "the syntax of your argument may have been wrong, or too few arguments may have been passed\n")
        getInput()


#Functions to validate Column and Key as valid inputs
def validateCol(str):
    validInput =  ["AvgValence","AvgDancability","Rank", "Title", "Artist", "Genre", "Danceability", "Valence"]
    for i in range(len(validInput)):
        if (validInput[i] == str):
            return True
    return False
def validateKey(str):
    validInput =  ["Rank" , "Title"]
    for i in range(len(validInput)):
        if (validInput[i] == str):
            return True
    return False
#Help function to instruct user on operations and proper syntax
def help():
    sys.stdout.write("exit : To exit program\n"
    "help : Full list of commands and correct syntax\n"
    "load data: Create database and load data from csv\n\n"
    "Proper Syntax for Querying information about a Title: <column> of <key> <value>\n"
    "Ex : Rank of Title \"Randsom\" - will return the Rank of the song Titled Randsom\n\n "
    "Proper Syntax for Querying information about an Artist:\n"
    "<column> of <foreignKey> <foreignVal> from <key> <value>\n"
    "Ex : AvgValence of Artist\"Ed Sheeran\" from Title \"Shape of You\"- will the Average Valence of Ed Sheeran\n")
#Laod Data Function will go here
def loadData():
    x=1

if __name__ == '__main__':
    main()
