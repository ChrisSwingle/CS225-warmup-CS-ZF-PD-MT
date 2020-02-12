# This program connects to two SQLite databases, one for songs and one
# for artists, creates tables for each database, reads in data from csv
# files into arrays, and then inserts the data stored in the arrays into
# the appropriate table.

import sqlite3
import csv

# Connect to database files
dbSongs = sqlite3.connect('Songs.db')
dbArtists = sqlite3.connect('Artists.db')

# Create database cursor objects
cS = dbSongs.cursor()
cA = dbArtists.cursor()

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

    # Read in csv file data into arrays
    songsArray = []
    with open('SongsClean.csv') as songsDataFile:
        songsReader = csv.reader(songsDataFile)
        for row in songsReader:
            print(row)
            songsArray.append(row)
    print()
    artistsArray = []
    with open('ArtistsClean.csv') as artistsDataFile:
        artistsReader = csv.reader(artistsDataFile)
        for row in artistsReader:
            print(row)
            artistsArray.append(row)

    # Insert data into tables
    for songRow in songsArray:
        cS.execute('''INSERT INTO Songs(Rank, Title, Artist, Genre, Danceability,
                      Valence) VALUES(?,?,?,?,?,?)''', (songRow[0], songRow[1],
                                                        songRow[2], songRow[3],
                                                        songRow[4], songRow[5]))
    for artistsRow in artistsArray:
        cA.execute('''INSERT INTO Artists(ArtistName, AvgDanceability, AvgValence)
                      VALUES (?,?,?)''', (artistsRow[0], artistsRow[1],
                                          artistsRow[2]))
    dbSongs.commit()
    dbArtists.commit()
    return


loadData()
dbSongs.close()
dbArtists.close()
