#!/apps/enthought/bin/python2.7

# generates a composite synoptic analysis for the uk, consisting of
# ukmo mslp, satellite ir and rainfall radar with a large timer in
# the corner

# usage:
# generate.py d1 d1 fout
#
# where d1 and d2 are the start and end dates respectively,
# format yyyymmddhhmm, and fout is the output filename.
#
# fout is an animated gif
#
# Aaron O'Leary Oct 2012

from sys import argv
from datetime import datetime, timedelta as td
import os

import Image, ImageDraw, ImageFont
import numpy as np

import images2gif

def date_range(start, end):
    """start end are yyyymmddhhmm"""
    d1 = datetime(int(start[:4]), int(start[4:6]), int(start[6:8]), int(start[8:10]), int(start[10:]))
    d2 = datetime(int(end[:4]), int(end[4:6]), int(end[6:8]), int(end[8:10]), int(end[10:]))
    diff = d2 - d1

    diffs = int(diff.total_seconds())
    D = [d1 + td(seconds=i) for i in xrange(0, diffs, 1800)]
    return D

def fname_sat(time):
    """loads a satellite image for the *hour* of the time given."""
    root = '/nfs/see-archive-10_a29/chatmosphere/'
    folder = 'metoffice_satellite/'
    ftime = time.strftime("eurir_sat_%Y%m%d%H00.jpg")
    fname = root + folder + ftime
    return fname

def fname_mslp(time):
    """mslp analysis filename for the *6 hourly* of the time given.
    i.e. 00, 06, 12, 18"""
    h6 = "%02d" % (time.hour // 6 * 6)
    ftime = time.strftime("%Y%m%d")
    root = '/nfs/see-archive-10_a29/chatmosphere/'
    folder = 'metoffice_charts/'
    fname = "{ftime}_{h}00_analysis.gif".format(ftime=ftime, h=h6)
    fpath = os.path.join(root, folder, fname)
    return fpath

def fname_radar(time):
    """loads a radar image filename for the *minute* of the time given."""
    root = '/nfs/see-archive-10_a29/chatmosphere/'
    folder = 'metoffice_rainfall_radar/'
    ftime = time.strftime("uk_britradar_%Y%m%d%H%M.gif")
    fname = root + folder + ftime
    return fname

def grab_image(form, time, size=None):
    """form is the type of image to load - mslp, radar or sat
    time is a datetime object
    size is the total size of the final image.
    returns an image object
    """
    if form == "mslp":
        fname = fname_mslp(time)
        print fname
    elif form == "sat":
        fname = fname_sat(time)
    elif form == "radar":
        fname = fname_radar(time)

    try:
        im = Image.open(fname)
    except IOError:
        im = Image.new('RGB', (size[0]/2,size[1]/2), color='white')

    if size:
        height = im.size[1]
        new_height = size[1] / 2
        new_width = im.size[0] * new_height // height
        re = im.resize((new_width, new_height))
        return re
    return im

def make_timer(time):
    """generate a timer image"""
    size = (565,450)
    im = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(im)

    text1 = time.strftime("%a")
    text2 = time.strftime("%H%M")
    text_pos1 = (100,75)
    text_pos2 = (100,225)

    fonts = '/usr/share/fonts/liberation/LiberationMono-Regular.ttf'
    font = ImageFont.truetype(fonts, 150)

    draw.text(text_pos1, text1, font=font, fill='black')
    draw.text(text_pos2, text2, font=font, fill='black')

    return im

def stitch(time, size=None):
    """append all the images together and return as image object"""
    size = (1200, 900)
    top_left = grab_image("mslp", time, size)
    top_right = grab_image("radar", time, size)
    bottom_left = grab_image("sat", time, size)
    bottom_right = make_timer(time)
    big_im = Image.new('RGB', size, color='white')
    big_im.paste(top_left, (0,0))
    big_im.paste(top_right, (635,0))
    big_im.paste(bottom_left, (0,size[1]/2))
    big_im.paste(bottom_right, (635,size[1]/2))
    return big_im

def main():
    dates = date_range(argv[1], argv[2])
    print dates[0].ctime()
    print dates[-1].ctime()
    images = [np.asarray(stitch(date)) for date in dates]
    outfile = argv[3]
    images2gif.writeGif(outfile, images, duration=0.1)

if __name__ == '__main__':
    main()
