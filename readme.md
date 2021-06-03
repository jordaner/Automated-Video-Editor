# Automated Video Editor

A python script that takes one or more mp4 video files, edits together a set of clips from those files and renders them into a new video.

## How to

Before running the script you should ensure that the following files can be found in the same directory as the script file: 
- All source .mp4 videos 
- A timestamps.txt file defining the clips to cut 

### The timestamps.txt file

The timestamps.txt file defines the video files and the time windows to be used to make the final video.
The syntax of the timestamps file is as follows:
 - Each filename should be preceded by >> and should not include the .mp4 extension e.g. `>>myvideo`
 - The desired time windows from each file should come under the filename
 - The format for the time windows is starttime-endtime
 - A time is defined as hour:minute:second
 - Comments can be added using '#', anything to the right of this symbol will not be interpreted
 - If a starttime or an endtime are not defined the start/end of the file in question is taken e.g. -0:30 goes from the beginning of the file to the 30th second, 0:30- makes a clip from the 30th second to the end of the video.

### Launching the script

The script can be launched using the following command:
```
python3 ave.py
```
With the optional arguments `--timestamps` and `--output` (or `-t` and `-o`) which can be used to define the name of the timestamps file (timestamps.txt by default) and the name of the output file (output by default).

## Dependencies

The AVE script uses the moviepy library for the editing and rendering of the clips.