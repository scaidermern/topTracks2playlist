# topTracks2playlist

*topTracks2playlist* is a little script to retrieve for each given artist the top tracks (most listened tracks) according to [last.fm](http://www.last.fm) with the help of [python-lastfm](https://code.google.com/p/python-lastfm/).  Then it either prints them, or uses [mpc](http://www.musicpd.org/clients/mpc/) to generate a playlist usable with [mpd](http://www.musicpd.org/). Adding support for other players offering a command line interface should be fairly easy.

## Usage

*topTracks2playlist* has a few command line arguments:

    -n      , --num    number of tracks per artist (default: 10)
    -o <arg>, --out    output file name for the generated playlist (default: topTracks.m3u)
    -p      , --print  just print the top tracks for the given artists
                       instead of generating a playlist
    -h      , --help   print this help and exit

## Examples

`topTracks2playlist.py -p -n 2 "Radio Head" "Running Wild" "ColdPlay"` would print:

    Radio Head:
      Creep
      Street Spirit
    Running Wild:
      Riding the Storm
      Under Jolly Roger
    ColdPlay:
      Paradise
      The Scientist

`topTracks2playlist.py -n 2 "Radio Head" "Running Wild" "ColdPlay"` could generate the following playlist:

    Albums/Running Wild/Running Wild - 1989 - Death Or Glory/Running Wild - 01 - Riding The Storm.mp3
    Albums/Running Wild/Running Wild - 2002 - Live/Running Wild - 2002 - Live - CD1/Running Wild - 05 - Riding the Storm.mp3
    Albums/Running Wild/Running Wild - 2011 - The Final Jolly Roger/Running Wild - 2011 - The Final Jolly Roger - CD1/Running Wild - 04 - Riding The Storm.mp3
    Albums/Running Wild/Running Wild - 1987 - Under Jolly Roger/Running Wild - 01 - Under Jolly Roger.mp3
    Albums/Running Wild/Running Wild - 1988 - Ready For Boarding/Running Wild - 02 - Under Jolly Roger.mp3
    Albums/Running Wild/Running Wild - 2002 - Live/Running Wild - 2002 - Live - CD2/Running Wild - 10 - Under Jolly Roger.mp3
    Albums/Running Wild/Running Wild - 2011 - The Final Jolly Roger/Running Wild - 2011 - The Final Jolly Roger - CD2/Running Wild - 05 - Under Jolly Roger.mp3

(because I don't own any songs from Radio Head or ColdPlay ;))



# License   
[GPL v3](http://www.gnu.org/licenses/gpl.html)
(c) [Alexander Heinlein](http://choerbaert.org)
