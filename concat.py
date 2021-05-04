from argparse import ArgumentParser
from os import path, listdir
from re import match
from sys import exit
from moviepy.editor import VideoFileClip, concatenate_videoclips

# TIMESTAMPS

def makeTimestampsDictFromFileName(filename):
	timestampLines = makeTsListFromFileName(filename)
	timestamps = {}
	temp = {'currentVideo': "default", 'empty': 0, 'comments': 0}
	for rawLine in timestampLines:
		processLine(timestampLines.index(rawLine), rawLine, temp, timestamps)
	return timestamps

def makeTsListFromFileName(filename):
	if filename.split('.')[-1] != 'txt':
		print("Timestamps must be a .txt file"), exit()
	absFilePath = path.dirname(path.abspath(__file__)) + "/" + filename
	return open(absFilePath, 'r').readlines()

def processLine(index, rawline, temp, timestamps):
	line = processCommentsAndSpaces(rawline, temp)
	if not line:
		temp['empty'] += 1
	elif line [:2] == '>>':
		processNewVideoLine(line, temp, timestamps)
	else:
		timestamps[temp['currentVideo']].append(makeTimeWindowFromString(line, index))

def processCommentsAndSpaces(rawLine, temp):
	line = rawLine.replace(' ','').replace('\n','')
	if '#' in line:
		temp['comments'] += 1
		return line.split('#')[0]
	return line

def processNewVideoLine(line, temp, timestamps):
	if line[2:] + '.MP4' not in listdir():
		print("Video %s does not exist" % line[2:]), exit()
	temp['currentVideo'] = line[2:]
	timestamps[temp['currentVideo']] = []

def makeTimeWindowFromString(line, index):
	timeWindow = line.split('-')
	if len(timeWindow) != 2:
		print("Invalid timeWindow: not 2 stamps: %s at line %d" % (line, index)), exit()
	for stamp in timeWindow:
		if stamp and not match('(([0-9]:)?[0-5])?[0-9]:[0-5][0-9]$', stamp):
			print("Invalid timestamp: %s at line %d" % (stamp, index)), exit()
	return (timeWindow[0], timeWindow[1])

# VIDEO READING

def makeClipsFromTimestamps(timestampDict):
	clipList = []
	for inputName in timestampDict.keys():
		videoFile = VideoFileClip(inputName + '.MP4')
		for timeWindow in timestampDict[inputName]:
			clipList.append(videoFile.subclip(t_start=timeWindow[0], t_end=timeWindow[1]))
	return clipList

# VIDEO RENDERING

def makeVideoFromClips(cliplist, videoname="output"):
	final_clip = concatenate_videoclips(cliplist)
	final_clip.write_videofile(videoname+".mp4")
	print("Video completed")

# MAIN

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("-i", "--input", dest="input_filename", type=str,help="Input video file") # remov?
	parser.add_argument("-t", "--timestamps", dest="timestamps_filename", type=str, default="timestamps.txt",
						help="Input timestamps file (timestamps.txt by default)")
	parser.add_argument("-o", "--output", dest="output_filename", type=str, default="output",
						help="Output filename (without .mp4 part)")
	args = parser.parse_args()

	clipList = makeClipsFromTimestamps(makeTimestampsDictFromFileName(args.timestamps_filename))
	makeVideoFromClips(clipList, args.output_filename)
