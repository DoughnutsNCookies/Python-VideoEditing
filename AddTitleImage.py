from moviepy.editor import *
import threading
import os

def getFiles(directory):
	files = []

	# Finds files in the directory and stores them into a list
	rawFiles = os.listdir(directory)
	for file in rawFiles:
		# Loop through each file and appends each file name with the directory name into a list to return
		root, ext = os.path.splitext(file)
		if  root not in files:
			files.append(root)
	return files

def edit(directory, file):
	# Final video = Image + Original Video
	finalVideo = []

	# Finds the file of the image and video. Sets the duration of the image video to 2 seconds and resize to Original Video's size
	video = VideoFileClip(directory + file + ".mp4")
	image = ImageClip(directory + file + ".png").set_duration(2)

	# Resize either image of video clip based on which is bigger in resolution
	if (video.size[0] > image.size[0]):
		image = image.fx(vfx.resize, width=video.size[0], height=video.size[1])
	else:
		video = video.fx(vfx.resize, width=image.size[0], height=image.size[1])

	# Appends the image video and orginal video to the final video list to be concatenated
	finalVideo.append(image)
	finalVideo.append(video)
	videoClip = concatenate_videoclips(finalVideo, method='compose')

	# Writes out the final video with its desired output name
	videoClip.write_videofile(file + ".mp4", fps=30, remove_temp=True, codec="libx264", audio_codec="aac")

def main():
	# Gets all file names from the "Files" directory
	editDir = "ToEdit/"
	if ([True, False][int(input('Ensure that the ' + editDir + ' folder contains ONLY video files\nPress 1 to continue, 0 to exit: '))]):
		exit(0)
	fileNames = getFiles(editDir)

	# Creates a thread for each file
	threads = []
	for file in fileNames:
		thread = threading.Thread(target=edit, args=("Files/", file,))
		threads.append(thread)
		thread.start()

	# Waits for all the threads to join before terminating the program
	for thread in threads:
		thread.join()

# Ensures this script is being run directly
if __name__ == "__main__":
	main()