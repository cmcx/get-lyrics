# coding: utf-8

import argparse
from bs4 import BeautifulSoup
import requests
import json
import os

parser = argparse.ArgumentParser()

parser.add_argument('artist_url',
                    help = 'You need a URL for an artist page from songtextemania.com.')

parser.add_argument('--json',
                    help = 'Write output to specified file')

# parser.add_argument('-d', '--delete_doubles',
#                    action = 'store_true',
#                    help = 'Delete doubles, e.g. if the same song is on two different albums and is listed twice.')


args = parser.parse_args()


   
def get_songdata(url):
    '''
    downloads the songdata from a song-oriented sub-site of songtextmania.com and extracts the text
    '''
    
    html = requests.get(url)
    html = html.text
    soup = BeautifulSoup(html, 'lxml')
    songtext1 = soup.find_all(class_='lyrics-body')
    songtext2 = soup.find_all(class_='p402_premium')
    if songtext1 != [] and songtext2 != []:
        songtext = songtext1[0].text + songtext2[0].text
    elif songtext1 != [] and songtext2 == []:
        songtext = songtext1[0].text
    else:
        songtext = None
    return songtext

def check_filename(filename):
    '''
    checks if the filename given on the command line exists and if it does, a new filename can be input
    '''
    if os.path.exists(filename):
        filename = raw_input('File or directory exists. Please choose another filename.')
        check_filename(filename)
 

songs = []                                                      # initialize the list which will contain the songs, each song as a dictionary

html = requests.get('http://www.songtextemania.com/sohne_mannheims_songtexte.html') # get the page for the artist
html = html.text
soup = BeautifulSoup(html, 'lxml')                              # soupify
   
links = [link.get('href') for link in soup.find_all('a')]       # get all the links
links = [link for link in links if not 'songtexte' in link]     # filter out the links to the albums
links = [link for link in links if 'songtext' in link]          # only keep the links for the songs (and dump the rest)
base_url = 'http://www.songtextemania.com'                       # set the base url (because the links to the songtexts lack that base)
links = [base_url + link for link in links]

for link in links:
    songs.append({'title': ' '.join(link[30:-30].split('_')), 'url': link})  # split the songtitle into a list of words and then rejoin it to get 'song title' from 'song_title'

#if args.delete_doubles:
#    songs = list(set(songs))        # if we don't want redundant entries (e.g. same song on different albums), remove these

# get the songtext for each of the songs
for song in songs:
    song['text'] = get_songdata(song['url'])


if args.json:
    filename = args.json
    check_filename(filename)
    with open(filename, 'w') as f:
        f.write(json.dumps(songs))
    print('Songtexts have been written to ', filename)



