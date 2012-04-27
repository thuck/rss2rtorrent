# rss2rtorrent

This project will allow to use the rss to automatically add torrents to rtorrent.  
The current focus is The Piratebay, but this should be extended in the future.  

## Configuration File

The configuration file should be placed on the path:  
*~/.config/rss2rtorrent/feed.cfg*  

## Sections

### [torrent]  
Global configuration.

#### Valid parameters:  
* watch\_directory - Directory that rtorrent watch to start automatically the torrents. 

#### Example:
   [torrent]  
   watch\_directory=~/rtorrent/watch

### [feed]
This section has no special name, and as many as you want can be used.  
You'll need as many sections as you will have feeds

#### Valid parameters:
* series - This parameter is used to filter the series.  
You can include any regex that you want, and separate it using commas.  
This an optional parameter, and if not present a wildcard (.\*) will be used.
* rss - This parameter should be a valid feed.

#### Example:
  [eztv]  
  series=House, Silent Witness, conan  
  rss=http://rss.thepiratebay.se/user/d17c6a45441ce0bc0c057f19057f95e1

  [e-books]  
  rss=http://rss.thepiratebay.se/301

## Crontab
This software is not a daemon, and it should run in a cron-like software.  
There is no need to configure the cron using some kind of "just in case"  
configuration to avoid the start of many process of rss2rtorrent, it will  
automatically detect that another rss2rtorrent is running and will exit.

