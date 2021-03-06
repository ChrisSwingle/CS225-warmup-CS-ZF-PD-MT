# This program connects to a SQLite database, creates tables for
# Songs and Artists, and then loops through csv files to insert
# the data into the the appropriate table.

import sqlite3
import csv

# Connects to database file
db = sqlite3.connect('SongsArtists.db')

# Creates database cursor object
c = db.cursor()


# loadData() function creates tables and then loads data from csv files into tables
def loadData():
    # Remove previously created tables if they exist
    try:
        c.execute('''DROP TABLE Songs''')
        c.execute('''DROP TABLE Artists''')
    finally:
        db.commit()

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
        with open('Artists.csv') as artistsDataFile:
            artistsReader = csv.reader(artistsDataFile)
            for artistsRow in artistsReader:
                print(artistsRow)
                c.execute('''INSERT INTO Artists(ArtistName, AvgDanceability,
                                                  AvgValence)
                              VALUES (?,?,?)''', (artistsRow[0], artistsRow[1],
                                                  artistsRow[2]))
        db.commit()


# sqlQuery() function takes user input, converts to a valid SQL statement, and returns correct
# data
def sqlQuery(column, key, val):
    songCols = ['Rank', 'Title', 'Artist', 'Genre', 'Danceability', 'Valence']
    artistCols = ['ArtistName', 'AvgDanceability', 'AvgValence']

    # Determine correct table to search in given user input
    if key in songCols and column in songCols:
        table = "songs"
        print("determined table songs")
    elif key in artistCols and column in artistCols:
        table = "artist"
        print("determined table artist")

    # Convert to valid SQL statement to fetch correct information from database
    f = c.execute("SELECT "+column+" FROM "+table+" WHERE upper("+key+") = upper(\'"+val+"\')")

    # Stores and prints fetched results from query as list
    rows = c.fetchall()
    for row in rows:
        print(row[0])

loadData()
db.close()
