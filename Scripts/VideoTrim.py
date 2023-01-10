from moviepy.editor import VideoFileClip
import threading
import os

# Finds files in the directory and gets its timestamps from user input
# Put them together into a list -> Eg: (Folder/file.mp4, file.mp4, 1:00, 2:00)
# Combines all of those list into one big list to return
def getFileTimestamps(directory):
	files = os.listdir(directory)
	toEditList = []
	for file in files:
		confirmed = False
		while confirmed == False:
			print("Input time for " + file)
			timeStamps = (str(input("Start (00:00:00): ")), str(input("End (00:00:00): ")))
			print(f"\nTimestamp for {file} is ({timeStamps[0]}, {timeStamps[1]})")
			confirmed = [False, True][int(input("Confirm? (1 for yes / 0 for no): "))]
			print()
		
		toEditList.append([directory + file, file, timeStamps[0], timeStamps[1]])
	return toEditList

# Trims the video by its path name using the timestamps, and outputs them into their original names
def trim(pathName, outputName, start, end):
	video = VideoFileClip(pathName)

	print(pathName, outputName, start, end)
	subClip = video.subclip(t_start=start, t_end=end)
	subClip.write_videofile(outputName)

# Gets all files from the directory
# Creates a thread for each file to trim each video simultaneously
def main():
	trimDir = "ToTrim/"
	if ([True, False][int(input('Ensure that the ' + trimDir + ' folder only contains video and image files that are of THE SAME NAME\nPress 1 to continue, 0 to exit: '))]):
		exit(0)
	files = getFileTimestamps(trimDir)

	threads = []
	for file in files:
		thread = threading.Thread(target=trim, args=file)
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

# Ensures this script is being run directly
if __name__ == "__main__":
	main()