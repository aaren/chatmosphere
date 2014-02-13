Basic script to automate creation of analysis charts for chatmosphere.

Download:

    git clone https://github.com/aaren/chatmosphere.git


Usage:

    ./generate_chatmosphere.py start stop output

start is the time to start plotting, format yyyymmddhhmm

stop is the time to stop plotting, format yyyymmddhhmm

output is a filename to write to. Output is an animated gif.


`images2gif.py` needs to be in the same directory as generate_chatmosphere.py, so
you can run it here or put both files somewhere in your $PATH.


