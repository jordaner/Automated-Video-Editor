import os
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips

def makeVideo():
	cliplist = []
	for i in range(25):
		print("%d.mp4"%(i+1))
		cliplist.append(VideoFileClip("%d.mp4"%(i+1)))
	makeVideoFromClips(cliplist, "vincennes_1804_haute_cam")

def makeVideoFromClips(cliplist, videoname="output"):
	final_clip = concatenate_videoclips(cliplist)
	final_clip.write_videofile(videoname+".mp4")
	print("Video completed")

def makeClipsFromTimestamps(timestampList, videoFile):
	clipList = []

	print(type(videoFile))

	for timestamp in timestampList:
		print("Processing clip number %d" %(len(clipList) + 1))
		timeWindow = timestamp.split('-')
		print("Start time: %s" %(timeWindow[0]))
		print("End time: %s" %(timeWindow[1]))
		# TODO Make clip
		clip = videoFile.subclip(t_start=timeWindow[0], t_end=timeWindow[1])

		clipList.append(clip)
		print()

	return clipList

def makeTimestampsFromFile(file):
	return [x.translate(str.maketrans('','','\n')) for x in file]

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", dest="input_filename", type=str,help="Input video file")
	parser.add_argument("-t", "--timestamps", dest="timestamps_filename", type=str, default="timestamps.txt",
						help="Input timestamps file (timestamps.txt by default)")
	parser.add_argument("-o", "--output", dest="output_filename", type=str, default="output",
						help="Output filename (without .mp4 part)")
	args = parser.parse_args()

	scriptDirectory = os.path.dirname(os.path.abspath(__file__))

	absTimestampPath = scriptDirectory+"/"+args.timestamps_filename
	
	timestampLines = open(absTimestampPath, 'r').readlines()

	clipList = makeClipsFromTimestamps(makeTimestampsFromFile(timestampLines),
										VideoFileClip("%s.mp4"%(args.input_filename)))
	
	makeVideoFromClips(clipList, args.output_filename)
