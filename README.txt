APCT
====

APCT - Anti Paranoya Copy Tool


Some time ago, I have wrote a small python script to move TV series episodes in the correct folder as Xbmc like. 

The code run correctly on Linux ( Ubuntu) and I hope on windows but I never tried it on this platform.

Command syntax :
apct.py -i <Input_Path> -o <Output_Path>
apct.py -i /home/user/download/ /home/xbmc/TvShows/


The script can be used within a cron job like that
  
  #sh

  #to avoid duplicate script
  pidof -x -o $$ $(basename "$0") && exit 1
  pidof -x -o $$ ncftpget && exit 1

  #ncftp to move data from other machines via ftp
  #ncftpget -DD -Z -u xbmc -p xbmc atom /home/user/Downloads /incoming/*

  /home/user/script/apct.py -i /home/user/Downloads -o /home/user/TV\ Shows/


I hope that this script can be useful to someone.

Know bug:
* JSON call works only on local host
* Not check available space before copy 
* Missing code path to support copy instead move
