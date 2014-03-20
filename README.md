Basic script to automate creation of analysis charts for chatmosphere.

### Download

    git clone https://github.com/aaren/chatmosphere.git


### Usage

    ./generate_chatmosphere.py start stop output

start is the time to start plotting, format yyyymmddhhmm

stop is the time to stop plotting, format yyyymmddhhmm

output is a filename to write to. Output is an animated gif.


### I still don't know what you mean

Do this to get an animated gif called 'animation.gif' from 1200 10th
Jan 2014 to 1800 12th Jan 2014:

    git clone https://github.com/aaren/chatmosphere.git
    cd chatmosphere
    ./generate_chatmosphere.py 201401101200 201401121800 animation.gif


### Dependencies

You need to be on a linux machine on the SEE network.

`images2gif.py` needs to be in the same directory as
generate_chatmosphere.py (as it is here) so you can run it from this
folder or put both files somewhere in your $PYTHONPATH.
