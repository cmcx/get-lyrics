
# Scrape all lyrics by an artist from songtextemania.com 

This is a simple script that downloads all lyrics off an artist page from the website songtextemania.com and optionally writes them to disk. The data is formatted as a list of dictionary, where each entry in the list represents a song, and where each song dictionary contains the song title, url and lyrics.


### Usage

~~~
get-lyrics --json filename artist-url
~~~



# todo

- option to download just one song
- option to download each song to a textfile in a corpus-directory, together with a metadata-file
- option to download just a song from a song-page
 
