import sys
import sqlite3
import csv

# GLOBALS
# Program continues to run
globalFlag = True

# Connects to database file
db = sqlite3.connect('SongsArtists.db')

# Creates database cursor object
c = db.cursor()


# Main function
def main():
    # Tells user how to access commands for program
    sys.stdout.write("Welcome. Type 'help' for a full list of commands and correct syntax.\n")

    # Flag to end program
    global globalFlag
    while globalFlag:
        getInput()
    db.close()


# Gets user input and passes to processInput()
def getInput():
    sys.stdout.write(">>")
    processInput(input())


# Processes user input and looks for preset commands before sending to parser
def processInput(userInput):
    userInput = userInput.strip()
    if userInput.lower() == "help":
        help()
    elif userInput.lower() == "exit" or userInput.lower() == "quit":
        sys.stdout.write("Goodbye!")
        global globalFlag
        globalFlag = False
    elif userInput.lower() == "load data":
        loadData()
    elif userInput.lower() == "join data":
        joinSql()
    else:
        parse(userInput)


# Parse function will break user input into seperate pieces of data to pass to query function:
# Parser will first split on " " to obtain strings.
def parse(userInput):
    try:
        # Split on Quotes
        splitOnQuotes = userInput.split('"')

        # Split on Spaces
        divList1 = splitOnQuotes[0].split()
        column = divList1[0]

        # divList1[1] is "of" which will be disguarded
        key = divList1[2]
        value = splitOnQuotes[1]

        # Standardize capitalization of column and key.
        column = column.lower()
        column = column.capitalize()
        key = key.lower()
        key = key.capitalize()

        # Adjust for Possible synonyms in column string
        if column == "Song" or column == "Track":
            column = "Title"
        if column == "Singer" or column == "Artists" or column == "Author":
            column = "Artist"
        if column == "Avgvalence" or column == "avgvalence":
            column = "AvgValence"
        if column == "Avgdanceability":
            column = "AvgDanceability"

        # Adjust for Possible synonyms in key string
        if key == "Song" or key == "Track":
            key = "Title"
        if key == "Singer" or key == "Artists" or key == "Author":
            key = "Artist"

        # Validate that first two columns are valid inputs, then query, if not prompt user to input again
        # This makes user of short circuit evaluation
        if ((len(splitOnQuotes)==3) and (validateCol(column) and validateKey(key))):
            sqlQuery(column, key, value)

        # If this point is reached, input is invalid
        else:
            sys.stdout.write("Please enter a valid command. Type \"help\" for a complete list of commands.\n"
                             "The syntax of your argument may have been wrong.\n")
            getInput()
    except IndexError or UnboundLocalError:
        sys.stdout.write("Please enter a valid command. Type \"help\" for a complete list of commands.\n"
                         "The syntax of your argument may have been wrong.\n")
        getInput()


# Function to validate Column as valid input
def validateCol(str):
    validInput =  ["AvgValence", "AvgDanceability", "Rank", "Title", "Artist", "Genre", "Danceability", "Valence"]
    for i in range(len(validInput)):
        if (validInput[i] == str):
            return True
    return False


# Function to validate Key as valid input
def validateKey(str):
    validInput =  ["Rank", "Title", "Artist"]
    for i in range(len(validInput)):
        if (validInput[i] == str):
            return True
    return False


# Help function to instruct user on operations and proper syntax
def help():
    print("Commands:")
    sys.stdout.write("exit: To exit program\n"
    "help: Full list of commands and correct syntax\n"
    "load data: Create database and load data from csv\n"
    "join data: Join data from the songs and artists table to view relevant information\n\n"
    "Syntax:\nProper Syntax for Querying information about a Title or Artist: <column> of <key> <value>\n"
    "Ex: Rank of Title \"Randsom\" - will return the Rank of the song Titled 'Randsom'\n"
    "Ex: AvgDanceability of Artist \"Ed Sheeran\" - will return the Average Danceability of Ed Sheeran's songs\n\n")


# loadData() function creates tables and then loads data from csv files into tables
def loadData():
    # Remove previously created tables if they exist
    try:
        c.execute('''DROP TABLE Songs''')
        c.execute('''DROP TABLE Artists''')
        db.commit()
    finally:
        # Creates tables
        c.execute('''CREATE TABLE  Songs
                      (Rank real PRIMARY KEY, Title text, Artist text, Genre text,
                       Danceability real, Valence real)''')
        c.execute('''CREATE TABLE Artists
                      (ArtistName text, AvgDanceability real, AvgValence real,
                      FOREIGN KEY(ArtistName) REFERENCES Songs(Artist))''')
        db.commit()

        # Inserts csv file data into tables
        with open('Songs.csv') as songsDataFile:
            songsReader = csv.reader(songsDataFile)
            for songsRow in songsReader:
                print(songsRow)
                c.execute('''INSERT INTO Songs(Rank, Title, Artist, Genre,
                                                Danceability, Valence)
                              VALUES(?,?,?,?,?,?)''', (songsRow[0], songsRow[1],
                                                       songsRow[2], songsRow[3],
                                                       songsRow[4], songsRow[5]))
            print("")
        with open('Artists.csv') as artistsDataFile:
            artistsReader = csv.reader(artistsDataFile)
            for artistsRow in artistsReader:
                print(artistsRow)
                c.execute('''INSERT INTO Artists(ArtistName, AvgDanceability,
                                                  AvgValence)
                              VALUES (?,?,?)''', (artistsRow[0], artistsRow[1],
                                                  artistsRow[2]))
            print("")
        db.commit()


# SQL functionality for joining the two tables, called by issuing "join data"
def joinSql():
    try:
        # Valid SQL statement to fetch correct information from database
        c.execute('''SELECT Songs.Rank, Songs.Artist, Songs.Title, Artists.AvgDanceability, 
                  Artists.AvgValence FROM Artists INNER JOIN Songs ON Artists.ArtistName=Songs.Artist ORDER BY Songs.Rank ASC''')

        # Stores and prints fetched results from query as list
        rows = c.fetchall()
        print("Joined data (Rank, Artist, Title, AvgDanceability of Artist, AvgValence of Artist)")
        for row in rows:
            print(row) 
        print("")
    except sqlite3.OperationalError as e:
        print("Please load data with the \"load data\" before issuing querys.")


# sqlQuery() function takes 3 arguements of user input, converts to a valid SQL statement, 
# and returns correct data
def sqlQuery(column, key, val):
    songCols = ['Rank', 'Title', 'Artist', 'Genre', 'Danceability', 'Valence']
    artistCols = ['Artist', 'AvgDanceability', 'AvgValence']

    # Determine correct table to search in given user input
    if key in songCols and column in songCols:
        table = "songs"
    elif key in artistCols and column in artistCols:
        table = "artists"
        if column == "Artist":
            column = "ArtistName"
        if key == "Artist":
            key = "ArtistName"

    try:
        # Convert to valid SQL statement to fetch correct information from database
        c.execute("SELECT "+column+" FROM "+table+" WHERE upper("+key+") = upper(\'"+val+"\')")

        # Stores and prints fetched results from query as list
        rows = c.fetchall()
        for row in rows:
            print(row[0])
        print("")
        if len(rows) == 0:
            print("Query returned no results, please try a different query.")

    except sqlite3.OperationalError:
        print("Please load data with the \"load data\" before issuing querys.")
    except Exception:
        print("Please select valid column. Type 'help' for a full list of commands.")


if __name__ == '__main__':
    main()
