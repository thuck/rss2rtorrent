import feedparser
import ConfigParser
import os
import os.path
import sys
import re
import collections

def save_magnetic_links(directory, series):

    for serie in series:
        name = 'meta-%s.torrent' % (serie['infohash'])
        filename = os.path.join(directory, name)

        #As this problably will run in a crontab, it's better to check if the file exists
        if os.path.exists(filename):
            with open(filename, 'w') as magnet_file:
                magnet_file.write('d10:magnet-uri%s:%se' % (len(serie['magneturi']), serie['magneturi']))

def get_series(series, rss):

    series_list = []
    #TODO: include network verification to not crash the program
    feed = feedparser.parse(rss)

    for item in feed['items']:
        series_list.extend(item for serie in series.split(',') 
              if re.search(serie.strip(), item.title, re.IGNORECASE))

    return series_list

if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    config.read(os.path.expanduser('~/.config/rss2rtorrent/feed.cfg'))
    watch_directory = config.get('rtorrent', 'watch_directory')
  
    #rtorrent section is a special section
    for section in config.sections():
        if section == 'rtorrent':
            continue

        series = config.get(section, 'series')
        rss = config.get(section, 'rss')
        save_magnetic_links(watch_directory, get_series(series, rss))




