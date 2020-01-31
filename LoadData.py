# This program connects to two SQLite databases, one for songs and one
# for artists, creates tables for each database, and then loops through
# csv files to insert the data into the the appropriate table.

import sqlite3
import csv

# Connect to database files
dbSongs = sqlite3.connect('Songs.db')
dbArtists = sqlite3.connect('Artists.db')

# Create database cursor objects
cS = dbSongs.cursor()
cA = dbArtists.cursor()


# Creates tables and then loads data from csv files into tables
def loadData():
    # Remove previously created tables
    cS.execute('''DROP TABLE Songs''')
    cA.execute('''DROP TABLE Artists''')
    dbSongs.commit()
    dbArtists.commit()

    # Create tables
    cS.execute('''CREATE TABLE  Songs
                  (Rank real PRIMARY KEY, Title text, Artist text, Genre text,
                   Danceability real, Valence real)''')
    cA.execute('''CREATE TABLE Artists
                  (ArtistName text, AvgDanceability real, AvgValence real, 
                  FOREIGN KEY(ArtistName) REFERENCES Songs(Artist))''')
    dbSongs.commit()
    dbArtists.commit()

    # Insert csv file data into tables
    with open('Songs.csv') as songsDataFile:
        songsReader = csv.reader(songsDataFile)
        for songsRow in songsReader:
            cS.execute('''INSERT INTO Songs(Rank, Title, Artist, Genre, 
                                            Danceability, Valence) 
                          VALUES(?,?,?,?,?,?)''', (songsRow[0], songsRow[1],
                                                   songsRow[2], songsRow[3],
                                                   songsRow[4], songsRow[5]))
    with open('Artists.csv') as artistsDataFile:
        artistsReader = csv.reader(artistsDataFile)
        for artistsRow in artistsReader:
            cA.execute('''INSERT INTO Artists(ArtistName, AvgDanceability, 
                                              AvgValence) 
                          VALUES (?,?,?)''', (artistsRow[0], artistsRow[1],
                                              artistsRow[2]))
    dbSongs.commit()
    dbArtists.commit()
    return


loadData()
dbSongs.close()
dbArtists.close()
