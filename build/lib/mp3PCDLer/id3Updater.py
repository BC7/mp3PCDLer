import eyed3
import os

def updateID3(metadata):
	# Test File location:
	# /home/brizzy/CodeWork/python/yt-dl[Front-End]/Free.mp3


	# fPath = str(input("Please enter File path: \n"))

	# print(os.path.dirname(os.path.realpath(metadata["fileName"])))
	# cwd = os.getcwd()
	audiofile = eyed3.load(metadata["fileName"])
	# audiofile.initTag()

	audiofile.tag.title = metadata["title"]
	print("Title: " + metadata["title"])

	audiofile.tag.artist = metadata["artist"]
	print("Artist: " + metadata["artist"])

	audiofile.tag.album = metadata["album"]
	print("Album: " + metadata["album"])

	audiofile.tag.genre = metadata["genre"]
	print("Genre: " + metadata["genre"])
	# audiofile.tag.title = u"Hollow"
	# audiofile.tag.track_num = 2

	audiofile.tag.save()
