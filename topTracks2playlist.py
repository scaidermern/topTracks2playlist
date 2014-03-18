#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Alexander Heinlein <alexander.heinlein@web.de>
#
# topTracks2playlist: generate playlist from most famous artist tracks
# This script retrieves for each given artist the top tracks, according to
# last.fm. Then it either prints them, or uses 'mpc' to generate a playlist
# usable with 'mpd'.
#
# Note: the lastfm module requires the decorator and elementtree modules
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

import getopt
import lastfm
import shlex
import subprocess
import sys


# default settings
# max. number of tracks per artist
defaultNumTracks = 10
# playlist file name
defaultOutPlaylist = "topTracks.m3u"


api_key = 'a2e8a2657131322ef68d4c473cda4aac'
api = lastfm.Api(api_key)

# colored output
red, yellow, reset = range(3)
colors = { red    : "\033[1;31m",
           yellow : "\033[1;33m",
           reset  : "\033[1;m" }
def printCol(text, color):
    print colors[color] + text + colors[reset]

# ask last.fm for top tracks of the given artist
def getLastfmTopTracks(artist):
    #print "retrieving top %s tracks for '%s' from last.fm" % (numTracks, artist)
    try:
        info = api.get_artist(artist.decode('utf-8'))
        topTracks = info.top_tracks
        
        tracks = list()
        for track in topTracks[:numTracks]:
            tracks.append(track.name)
            
        if len(tracks) == 0:
            printCol('warning: no result from lastfm for artist "%s"' % (artist), yellow)
        
        return tracks
    except Exception as e:
        printCol("error for " + artist + ": " + str(e), red)
        return list()

# ask mpc for the path(s) of the given song
def getMPDPaths(artist, track):
    cmd = 'mpc search artist "%s" title "%s"' % (artist.decode("utf-8"), track)
    args = shlex.split(cmd.encode("utf-8"))
    output = subprocess.check_output(args)
    if len(output) == 0:
        printCol('warning: no result from mpc for artist "%s" title "%s"' % (artist, track), yellow)
    return output

# print usage information
def printUsage(name):
    print "usage:", name, "[OPTIONS] artist(s)"
    print "  generate playlist from most famous artist tracks"
    print "  -n      , --num    number of tracks per artist (default: %s)" % numTracks
    print "  -o <arg>, --out    output file name for the generated playlist (default: %s)" % outPlaylist
    print "  -p      , --print  just print the top tracks for the given artists"
    print "                     instead of generating a playlist"
    print "  -h      , --help   print this help and exit"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        printUsage(sys.argv[0])
        sys.exit(0)
    

    
    try:
        # get command line arguments
        opts, args = getopt.getopt(sys.argv[1:], 'n:o:ph', ["num=", "out=", "print", "help"])
    except getopt.GetoptError:
        usage(sys.argv[0])
        raise RuntimeError, 'invalid argument specified'
    
    numTracks   = defaultNumTracks
    outPlaylist = defaultOutPlaylist
    printOnly   = False
    for opt, arg in opts:
        if   opt in ("-n", "--num"):
            numTracks = int(arg)
        elif opt in ("-o", "--out"):
            outPlaylist = arg
        elif opt in ("-p", "--print"):
            printOnly = True
        elif opt in ("-h", "--help"):
            printUsage(sys.argv[0])
            sys.exit(0)
        else: assert(False)
    
    # 'args' now contains all remaining non-option arguments
    if len(args) == 0:
        printUsage(sys.argv[0])
        sys.exit(0)
    
    playlist = None
    if not printOnly:
        playlist = open(outPlaylist, "w")
    
    for artist in args:
        if printOnly:
            print "%s:" % (artist)
        
        topTracks = getLastfmTopTracks(artist)
        for track in topTracks:
            if printOnly:
                print "  %s" % (track)
            else:
                paths = getMPDPaths(artist, track)
                playlist.write(paths)
    
    if not printOnly:
        playlist.close()
