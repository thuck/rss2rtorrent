import feedparser
import ConfigParser
import os
import os.path
import sys
import re
import socket
import urllib2
import base64

def save_magnetic_links(directory, series):

    for serie in series:
        name = 'meta-%s.torrent' % (serie['infohash'])
        filename = os.path.join(directory, name)

        #As this problably will run in a crontab, it's better to check if the file exists
        if not os.path.exists(filename):
            with open(filename, 'w') as magnet_file:
                magnet_file.write('d10:magnet-uri%s:%se' % (len(serie['magneturi']), serie['magneturi']))

def save_torrent_files(directory, series):

    for serie in series:
        name = '%s.torrent' % (base64.urlsafe_b64encode(serie['title'].encode('utf8')))
        filename = os.path.join(directory, name)

        if not os.path.exists(filename):
            with open(filename, 'w') as torrent_file:
                #TODO: Need to catch the expection in case of network problem
                torrent_file.write(urllib2.urlopen(serie['links'][1]['href']).read())

def get_series(series, rss):

    series_list = []
    #TODO: include network verification to not crash the program
    feed = feedparser.parse(rss)

    for item in feed['items']:
        series_list.extend(item for serie in series.split(',') 
              if re.search(serie.strip(), item.title, re.IGNORECASE))

    return series_list

def get_lock():
    #Avoid two scrips to run at the same time
    #Got this example from: http://stackoverflow.com/a/7758075
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + 'rss2rtorrent')

    except socket.error:
        #This error should be logged
        sys.exit(1)


if __name__ == '__main__':

    get_lock()
    config = ConfigParser.RawConfigParser({'series':'.*', 'type':'torrent'})
    config.read(os.path.expanduser('~/.config/rss2rtorrent/feed.cfg'))
    watch_directory = os.path.expanduser(config.get('torrent', 'watch_directory'))
  
    #rtorrent section is a special section
    for section in config.sections():
        if section == 'torrent':
            continue

        series = config.get(section, 'series')
        rss = config.get(section, 'rss')
        download_type = config.get(section, 'type')

        if download_type == 'magnet_link':
            save_magnetic_links(watch_directory, get_series(series, rss))

        elif download_type == 'torrent':
            save_torrent_files(watch_directory, get_series(series, rss))

        else:
            #TODO: Log error for invalid configuration
            pass

    sys.exit(0)
