import xml.etree.ElementTree as ET
import sqlite3

# cearting a connection to Track_DB then controling it by cursor
conn=sqlite3.connect("./Track_DB.sqlite")
cur=conn.cursor()

# SQL Queries
cur.executescript("""
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Album_id INTEGER,
    title TEXT UNIQUE,
    length INTEGER, rating INTEGER, views INTEGER
);
""")

# opening the data file
f=open("./Tracks.xml")
stuff=ET.parse(f)

# lookup function that search for a word inside the entry (e)
def lookup(e,word):
    found=False
    for  element in e:
        if found : return element.text
        if element.tag == 'key' and element.text == word:
            found=True
    return None

# get all the tracks inside the xml file
all=stuff.findall("dict/dict/dict")

# get the values from xml file to be used in the database using lookup()
for entry in all:
    if (lookup(entry,"Track ID") is None) : continue
    artist=lookup(entry,"Artist")
    album=lookup(entry,"Album")
    track=lookup(entry,"Name")
    length=lookup(entry,"Total Time")
    rating=lookup(entry,"Rating")
    views=lookup(entry,"Play Count")

    if artist is None or album is None or track is None : continue

    # inserting values in Artist table
    cur.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)",(artist,))
    cur.execute("SELECT id FROM Artist WHERE name = ?",(artist,))
    artist_id=cur.fetchone()[0] #to get the foreign key

    #insrting values in Album table
    cur.execute("INSERT OR IGNORE INTO Album (title,artist_id) VALUES (?,?)",(album,artist_id))
    cur.execute("SELECT id FROM Album WHERE title = ?",(album,))
    album_id=cur.fetchone()[0] #to get the foreign key

    #inserting balues in Track table
    cur.execute("INSERT OR IGNORE INTO Track (Album_id,title,length,rating,views) VALUES(?,?,?,?,?)",(album_id,track,length,rating,views))

    # to save changes
    conn.commit()

# print the final JOIN table rows
cur.execute("SELECT Track.title,Album.title,Artist.name FROM Track JOIN Album JOIN Artist ON Track.album_id=Album.id AND Album.artist_id=Artist.id ")
x=cur.fetchall()
for i in x:
    print(i)

