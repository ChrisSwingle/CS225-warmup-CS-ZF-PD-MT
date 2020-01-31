# This program connects to a SQLite database, creates tables for
# Songs and Artists, and then loops through csv files to insert
# the data into the the appropriate table.

import sqlite3
import csv

# Connects to database file
db = sqlite3.connect('SongsArtists.db')

# Creates database cursor object
c = db.cursor()


# Creates tables and then loads data from csv files into tables
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
        return


loadData()
db.close()
