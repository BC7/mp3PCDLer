# import mp3PCDLer
from __future__ import unicode_literals
import sys
import tkinter as tk
import youtube_dl
import os
import json
from mp3PCDLer import id3Updater


def startDownload(urlString, metadata):

    global cwd
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    'outtmpl': '%(title)s.%(ext)s',
	'noplaylist':'true',
	'logger': MyLogger(),
	'progress_hooks': [my_hook],}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(urlString)
        sdlTitle = info_dict.get('title', None)
        ydl.download([urlString])

    print(sdlTitle + ' downloaded successfully. \nUpdating ID3 information\n')
    metadata["fileName"] = sdlTitle + ".mp3"
    id3Updater.updateID3(mp3Meta)
    print("\n**Process Complete**")

def my_hook(d):
    global dlStartStatus
    global dlFinishStatus

    if d['status'] == 'downloading' and dlStartStatus == False:
        dlStartStatus = True
        print("Download started - " + d['filename'])
    elif d['status'] == 'finished' and dlFinishStatus == False:
        dlFinishStatus = True
        print('Done downloading file, now converting to mp3...')
        global mp3Meta

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


class Application(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)

		defaultBG="#3399ff"
		# self.parent = master
		self.pack(expand="true", fill="both")
		self.configure(bg=defaultBG)

		# Declare Labels
		urlString = tk.StringVar()
		urlLabel = tk.Label(self, pady=5, bg=defaultBG, text="Youtube URL: ").grid(row=0,column=0, sticky="w")
		songTitleLabel = tk.Label(self, pady=5, bg=defaultBG, text="Title: ").grid(row=1,column=0, sticky="w")
		songArtistLabel = tk.Label(self, pady=5, bg=defaultBG, text="Artist: ").grid(row=2,column=0, sticky="w")
		songAlbumLabel = tk.Label(self, pady=5, bg=defaultBG, text="Album: ").grid(row=3,column=0, sticky="w")
		songGenreLabel = tk.Label(self, pady=5, bg=defaultBG,text="Genre: ").grid(row=4,column=0, sticky="w")

		# Declare entry widgets
		self.urlEntry = tk.Entry(self, textvariable=urlString, selectborderwidth="2",justify="left")
		self.titleEntry = tk.Entry(self)
		self.artistEntry = tk.Entry(self)
		self.albumEntry = tk.Entry(self)
		self.genreEntry = tk.Entry(self)

		# Add Entry Widgets to Frame (separated for ease of readability and accessing entry values
		self.urlEntry.grid(row=0,column=1, columnspan=4, sticky="w")
		self.titleEntry.grid(row=1,column=1, sticky="w")
		self.artistEntry.grid(row=2,column=1, sticky="w")
		self.albumEntry.grid(row=3, column=1, sticky="w")
		self.genreEntry.grid(row=4,column=1, sticky="w")

		sourceCheck = tk.StringVar().set("web")
		formatCheck = tk.StringVar().set("mp3")

		dlFormatCheck = tk.Checkbutton(self, variable=formatCheck,offvalue="mp3", onvalue="mp4", bg=defaultBG, text="Save as videos (.mp4)").grid(row=5, columnspan=3, column=0, sticky="w")
		automatedDLCheck = tk.Checkbutton(self, variable=sourceCheck,offvalue="web", onvalue="local", bg=defaultBG, text="Download multiple from list (insert filepath in URL)").grid(row=6, columnspan=3, column=0, sticky="w")

		dlButton = tk.Button(self, command= lambda: self.dl_click(), bd=0, bg=defaultBG, text="Download").grid(row=7,column=0, sticky="sw")
		# dlButton.config(highlightbackground=defaultBG)

		prefButton = tk.Button(self, command= lambda: openPref(),bd=0, bg=defaultBG, text="Settings").grid(row=7,column=1, sticky="se")
		self.config(highlightbackground=defaultBG)
		# for i in range(0,3):
		# 	self.grid_columnconfigure(i, weight=1, uniform="main")

	def dl_click(self):
		# collect optional id3 tags
		global mp3Meta
		mp3Meta["title"] = self.titleEntry.get()
		mp3Meta["artist"] = self.artistEntry.get()
		mp3Meta["album"] = self.albumEntry.get()
		mp3Meta["genre"] = self.genreEntry.get()
		startDownload(self.urlEntry.get(), mp3Meta)



def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    global cwd
    global mp3Meta
    global dlStartStatus
    global dlFinishStatus

    # get install location
    cwd = os.path.dirname(os.path.realpath(__file__))

    # download movies to temp before moving elswhere
    with open("mp3PCDLer/pref.json") as pref_data:
        d = json.load(pref_data)
        cwd = d["download_location"]
        os.chdir(cwd)
        print("Working in : " + os.getcwd())

    dlStartStatus = False
    dlFinishStatus = False

    mp3Meta = {
    "title"  : "Unknown",
    "artist" : "Unknown",
    "album"  : "Unknown",
    "genre"  : "Unknown"}

    root = tk.Tk()
    # root.configure(width=350,height=110)
    # root.configure(background='#000000',width='360')
    #root.resizable(0,0)
    for i in range(0,1):
        root.grid_columnconfigure(i, weight=1, uniform="main")

    # root.minsize(555, 110)
    root.title("mp3DLer")
    root.resizable(0,0)
    app = Application()
    app.mainloop()
    # print("This is the main routine.")
    # print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.

if __name__ == "__main__":
    main()