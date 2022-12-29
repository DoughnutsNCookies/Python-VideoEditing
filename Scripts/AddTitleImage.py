from moviepy.editor import *
import threading
import os

# Finds files in the directory and stores them into a list
# Loop through each file and appends each file name with the directory name into a list to return
def getFiles(directory):
	files = []


	rawFiles = os.listdir(directory)
	for file in rawFiles:
		root, ext = os.path.splitext(file)
		if  root not in files:
			files.append(root)
	return files

# Final video = Image + Original Video
# Finds the file of the image and video. Sets the duration of the image video to 2 seconds and resize to Original Video's size
# Resize either image of video clip based on which is bigger in resolution
# Appends the image video and orginal video to the final video list to be concatenated
# Writes out the final video with its desired output name
def edit(directory, file):
	finalVideo = []

	video = VideoFileClip(directory + file + ".mp4")
	image = ImageClip(directory + file + ".png").set_duration(2)
	
	if (video.size[0] > image.size[0]):
		image = image.fx(vfx.resize, width=video.size[0], height=video.size[1])
	else:
		video = video.fx(vfx.resize, width=image.size[0], height=image.size[1])
	
	finalVideo.append(image)
	finalVideo.append(video)
	videoClip = concatenate_videoclips(finalVideo, method='compose')
	videoClip.write_videofile(file + ".mp4", fps=30, remove_temp=True, codec="libx264", audio_codec="aac")

# Gets all file names from the "Files" directory
# Creates a thread for each file
# Waits for all the threads to join before terminating the program
def main():
	directory = "ToEdit/"
	fileNames = getFiles(directory)

	threads = []
	for file in fileNames:
		thread = threading.Thread(target=edit, args=(directory, file,))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

# Ensures this script is being run directly
if __name__ == "__main__":
	main()
