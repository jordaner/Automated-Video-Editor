from argparse import ArgumentParser
from os import path, listdir
from re import match
from sys import exit
from moviepy.editor import VideoFileClip, TextClip, concatenate_videoclips

from clipdetails import ClipDetails

clipDetailsList = []
clipDetailsDict = {}

# TIMESTAMPS

def makeTimestampsDictFromFileName(filename):
	timestampLines = makeTsListFromFileName(filename)
	timestamps = {}
	temp = {'currentVideo': "default", 'empty': 0, 'comments': 0}
	for rawLine in timestampLines:
		processLine(timestampLines.index(rawLine), rawLine, temp)

def makeTsListFromFileName(filename):
	if filename.split('.')[-1] != 'txt':
		print("Timestamps must be a .txt file"), exit()
	absFilePath = path.dirname(path.abspath(__file__)) + "/" + filename
	return open(absFilePath, 'r').readlines()

def processLine(index, rawline, temp):
	line = processCommentsAndSpaces(rawline, temp)
	if not line:
		temp['empty'] += 1
	elif line [:2] == '>>':
		processNewVideoLine(line, temp)
	elif line [:1] == '$':
		# text clip
		textClip = TextClip(line[1:], bg_color= 'black', fontsize=75, color = 'white')
		textDetails = ClipDetails("", 0, 2, line[1:])
		textDetails.clip = textClip.set_duration(2)
		clipDetailsList.append(textDetails)
	else:
		if validTimeWindow(line, index):
			details = ClipDetails(temp['currentVideo'], line.split('-')[0], line.split('-')[1], "")
			clipDetailsDict[temp['currentVideo']].append(details)
			clipDetailsList.append(details)

def processCommentsAndSpaces(rawLine, temp):
	line = rawLine.replace('\n','')
	if '#' in line:
		temp['comments'] += 1
		return line.split('#')[0] # What happens if there are multiple #'s ?
	return line

def processNewVideoLine(line, temp):
	if line[2:] + '.MP4' not in listdir():
		print("Video %s does not exist" % line[2:]), exit()
	temp['currentVideo'] = line[2:]
	if temp['currentVideo'] not in clipDetailsDict:
		clipDetailsDict[temp['currentVideo']] = []

def makeTimeWindowFromString(line, index):
	timeWindow = line.split('-')
	if len(timeWindow) != 2:
		print("Invalid timeWindow: not 2 stamps: %s at line %d" % (line, index)), exit()
	for stamp in timeWindow:
		if stamp and not match('(([0-9]:)?[0-5])?[0-9]:[0-5][0-9]$', stamp):
			print("Invalid timestamp: %s at line %d" % (stamp, index)), exit()
	return timeWindow

def validTimeWindow(line, index):
	timeWindow = line.split('-')
	if len(timeWindow) != 2:
		print("Invalid timeWindow: not 2 stamps: %s at line %d" % (line, index)), exit() # This triggers on returns
		return False
	for stamp in timeWindow:
		if stamp and not match('(([0-9]:)?[0-5])?[0-9]:[0-5][0-9]$', stamp):
			print("Invalid timestamp: %s at line %d" % (stamp, index)), exit()
			return False
	return True

# VIDEO READING

def makeClipsFromTimestamps(timestampDict):
	clipList = []
	for inputName in timestampDict.keys():
		videoFile = VideoFileClip(inputName + '.MP4')
		for timeWindow in timestampDict[inputName]:
			if not timeWindow[0]:
				timeWindow[0] = "0:00"
			if not timeWindow[1]:
				timeWindow[1] = videoFile.end
			clipList.append(videoFile.subclip(t_start=timeWindow[0], t_end=timeWindow[1]))
	return clipList

def makeVideoClipsFromDetails():
	for inputName in clipDetailsDict.keys():
		videoFile = VideoFileClip(inputName + '.MP4')
		for videoClipDetails in clipDetailsDict[inputName]:
			if not videoClipDetails.start:
				videoClipDetails.start = "0:00"
			if not videoClipDetails.end:
				videoClipDetails.end = videoFile.end
			videoClipDetails.clip = videoFile.subclip(t_start=videoClipDetails.start, t_end=videoClipDetails.end)

# VIDEO RENDERING

def makeVideoFromClips(cliplist, videoname="output", singleOutput=True):
	if singleOutput:
		final_clip = concatenate_videoclips(cliplist)
		final_clip.write_videofile(videoname+".mp4")
	else:
		for index in range(len(cliplist)):
			cliplist[index].write_videofile(videoname + str(index+1) + ".mp4")

def makeVideoFromClipDetails(videoname="output", singleOutput=True):
	clipList = []
	for clipDetails in clipDetailsList:
		clipList.append(clipDetails.clip)
	final_clip = concatenate_videoclips(clipList, method="compose")
	final_clip.write_videofile(videoname+".mp4")

# MAIN

if __name__ == "__main__":
	parser = ArgumentParser()
	parser.add_argument("-t", "--timestamps", dest="timestamps_filename", type=str, default="timestamps.txt",
						help="Input timestamps file (timestamps.txt by default)")
	parser.add_argument("-o", "--output", dest="output_filename", type=str, default="output",
						help="Output filename (without .mp4 part)")
	args = parser.parse_args()

	makeTimestampsDictFromFileName(args.timestamps_filename)	
	makeVideoClipsFromDetails()
	makeVideoFromClipDetails()