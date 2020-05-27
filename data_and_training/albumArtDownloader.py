
import time
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import tensorflow as tf
# import keras
# import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd

# create credentials object
creds = SpotifyClientCredentials(client_id="YOUR_CLIENT_ID", client_secret="YOUR_SECRET_KEY")

# create spotify object
spotify = spotipy.Spotify(client_credentials_manager=creds)


# download and save image to albumart folder
def saveAlbumArt(albumName, linkToImage, path = 'albumartimages/'):
    albumName = albumName.replace(r'/',' ')
    fullPath = path + albumName + ".jpg"
    f = open(fullPath, 'wb')
    f.write(requests.get(linkToImage).content)
    f.close()

# given a  dictionary, go through each entry and get the links to the images and download them into the specified folder
def getAndSaveAlbumArts(dictionary, path = 'albumartimages/'):

    for link in dictionary:
        fileName = link + ".jpg"
        fileName = fileName.replace(r'/', ' ')
        url = dictionary[link]
        r = requests.get(url)
        fullPath = path + fileName
        with open(fullPath, 'wb') as f:
            f.write(r.content)
    print("done")

#given artist uri, return a dictionary with all their albums formatted {albumId: [albumName, artistName, artistID, imageLink, genre, releaseDate]}
def getAlbumInfoFromArtist(uri):
    id = "spotify:artist:"+ uri
    albums = spotify.artist_albums(uri)
    try:
        genre = spotify.artist(id)['genres'][0]
    except:
        genre = "unknown"
    finally:
        album_dict = {}
        for item in albums['items']:
            try:
                albumID = item['id']
                albumName = item['name']
                artistName = item['artists'][0]['name']
                artistID = item['artists'][0]['id']
                imageLink = item['images'][0]['url']
                releaseDate = item['release_date']
                album_dict[albumID] = [albumName, artistName, artistID, imageLink, genre, releaseDate]
            except:
                continue
        return album_dict

# returns a list of artists that are similar to the one you searched for.
# maxlevel specifies how deep you want it to search, or how many degrees of relation you want it to search
def recursiveSimilarArtistSearch(artistID, curLevel,maxLevel, listOfArtists = {}, listOfAlbums = {}):
    artists = spotify.artist_related_artists(artistID)['artists']
    for artist in artists:
        name = artist['name']
        name = name.replace(" (Deluxe Edition)", "")
        if name not in listOfArtists:
            uri = artist['uri']
            id = artist['id']
            genre = artist['genres'][0]
            listOfArtists[name] = id
            albums = spotify.artist_albums(uri)
            for item in albums['items']:
                albumName = item['name']
                if albumName not in listOfAlbums:
                    images = item['images'][0]['url']
                    listOfAlbums[albumName] = images
            #time.sleep(2)
            if(curLevel + 1 ) <= maxLevel:
                artistDict, albumDict = recursiveSimilarArtistSearch(id, curLevel+1, maxLevel, listOfArtists, listOfAlbums)
                listOfArtists.update(artistDict)
                listOfAlbums.update(albumDict)

    return listOfArtists, listOfAlbums

# returns a list of artists that are similar to the one you searched for and a dictionary of albumIds with all their info
# maxlevel specifies how deep you want it to search, or how many degrees of relation you want it to search
def recursiveAlbumSearch(artistID, curLevel,maxLevel, listOfArtists = {}, the_list = {}):
    artists = spotify.artist_related_artists(artistID)['artists']
    for artist in artists:
        name = artist['name']
        name = name.replace(" (Deluxe Edition)", "")
        if name not in listOfArtists:
            uri = artist['uri']
            id = artist['id']
            try:
                genre = artist['genres'][0]
            except:
                print(artist)
                genre = "unknown"
            finally:
                listOfArtists[name] = id
                albums = getAlbumInfoFromArtist(uri)
                for item in albums:
                    if item not in the_list:
                        the_list[item] = albums[item]
                if(curLevel + 1 ) <= maxLevel:
                    artistDict, albumDict = recursiveAlbumSearch(id, curLevel+1, maxLevel, listOfArtists, the_list)
                    listOfArtists.update(artistDict)
                    the_list.update(albumDict)
    return listOfArtists, the_list

# give an artist id, this opens the master csv file, creates a pandas dataframe,
# does a search of similar artists and their albums, then adds only new and unique
# album artwork to the dataframe, and saves it at the end
# format of dataframe is ['album_id', 'link_to_image', 'album_name', 'artist_name', 'artist_id', 'genre', 'year']
def AlbumSearchToCSV(artistID, maxLevel=0, fileName = "masterAlbumList.csv"):
    #define column names for dataframe
    col_names = ['album_id', 'link_to_image', 'album_name', 'artist_name', 'artist_id', 'genre', 'year']

    #read in master list from file, or create a new file
    print("loading existing dataset from csv")
    masterDF = pd.read_csv(fileName, header = None, names = col_names)

    # do search of new albums given the artist id, getting back a new pandas dataframe
    print("searching for new albums")
    new_search_ar, new_search_al = recursiveAlbumSearch(artistID, 0,maxLevel)
    result_message = "got " + str(len(new_search_al)) + " albums from " + str(len(new_search_ar)) + " artists"
    print(result_message)

    #go through the dictionaries it got back and see if theres anything new to add to the dataframe """
    newstuff = [{'album_id': album_id,'link_to_image': new_search_al[album_id][3],
                         'album_name': new_search_al[album_id][0] , 'artist_name':new_search_al[album_id][1] ,
                         'artist_id':new_search_al[album_id][2] , 'genre':new_search_al[album_id][4] ,
                         'year':new_search_al[album_id][5]} for album_id in new_search_al if album_id not in masterDF["album_id"].values]
    # save the master list to the file
    masterDF = masterDF.append(newstuff, ignore_index=True)
    #print(masterDF)
    masterDF.to_csv(fileName)



# citizen uri : spotify:artist:0znuUIjvP0LXEslfaq0Nor
#brand new uri: spotify:artist:168dgYui7ExaU612eooDF1
#julien baker uri: spotify:artist:12zbUHbPHL5DGuJtiUfsip
#tupac uri: spotify:artist:1ZwdS5xdxEREPySFridCfh
#eminem: spotify:artist:7dGJo4pcD2V6oG8kP0tJRR
#manchester orchestra: spotify:artist:5wFXmYsg3KFJ8BDsQudJ4f
#as i lay dying: spotify:artist:2vd2HnNh4pdYa9gDVHFjEu
#ABR: spotify:artist:5p9CTsn5ueGU4oScNX1axu
#my band felina: spotify:artist:2k17GhmZx1GS1dCGLP4rKh


"""
id  = "0znuUIjvP0LXEslfaq0Nor"
info = getAlbumInfoFromArtist(uri)
for id in info:
    print(info[id])
"""

"""
f =open("/Users/michaelmcdermott/PycharmProjects/untitled1/uri2",'r')
uriList = f.readlines()
for uri in uriList:
    id = uri.replace("spotify:artist:","").rstrip()
    AlbumSearchToCSV(id, maxLevel=2)
"""

#artists, albums = recursiveSimilarArtistSearch("0znuUIjvP0LXEslfaq0Nor", 1 ,0, {}, {})
#message = "Got {numartists} artists and {numalbums} albums".format(numartists = len(artists), numalbums = len(albums))
#print(message)
#getAndSaveAlbumArts(albums)

