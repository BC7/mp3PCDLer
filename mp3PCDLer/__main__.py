# import mp3PCDLer
from __future__ import unicode_literals
import sys
import tkinter as tk
import youtube_dl
import os
import sys
import json
from mp3PCDLer import id3Updater
from tkinter import filedialog


def startDownload(urlString, metadata):

    global rootDir
    global fileName

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
        # fileName = info_dict.get('title', None) + '.mp3'
        ydl.download([urlString])

    print(fileName + ' downloaded successfully. \nUpdating ID3 information\n')
    id3Updater.updateID3(mp3Meta, fileName.replace('.webm', '.mp3'))
    os.chdir(rootDir)
    print("\n**Process Complete**")
    success = tk.Tk()
    success.resizable(0,0)
    success.title("SUCCESS!")
    m = tk.Message(success, text= "**Process Complete**\n\nTitle: " + mp3Meta['title'] + '\nArtist: ' + mp3Meta['artist'] + '\nAlbum: ' + mp3Meta['album'] + '\nGenre: ' + mp3Meta['genre'])
    m.config(anchor='center', font=('Helvetica', 16), pady=7, padx=8, width=500)
    m.pack()

def my_hook(d):
    global fileName

    if d['status'] == 'finished':
        # print(json.dumps(d))
        fileName = d['filename']
    else:
        sys.stdout.write('\rDownloading ' + d['filename'] + ' : ' + d['_percent_str'] + ' Complete ')
        sys.stdout.flush()

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

        self.relief = 'SUNKEN'
        with open(rootDir + "/pref.json", 'r+') as pref_data:
            d = json.load(pref_data)
            downloadDir = d['download_location']

        defaultBG= "#d3d3d3" #"#3399ff"
        
        self.pack(expand="true", fill="both")
        self.configure(bg=defaultBG)

        # Declare Labels
        urlString = tk.StringVar()
        urlLabel = tk.Label(self, padx=10, pady=10, width=12, anchor='center', font=('Helvetica', 20), bg=defaultBG, text="Youtube URL: ").grid(row=0,column=0, sticky="w")
        songTitleLabel = tk.Label(self, pady=10, width=12, anchor="e", font=('Helvetica', 20), bg=defaultBG, text="Title: ").grid(row=2,column=0, sticky="w")
        songArtistLabel = tk.Label(self, padx=10, width=12, pady=10, anchor="e", font=('Helvetica', 20), bg=defaultBG, text="Artist: ").grid(row=3,column=0, sticky="w")
        songAlbumLabel = tk.Label(self, padx=10, width=12, pady=10, anchor="e", font=('Helvetica', 20), bg=defaultBG, text="Album: ").grid(row=4,column=0, sticky="w")
        songGenreLabel = tk.Label(self, padx=10, width=12, pady=10, anchor="e", font=('Helvetica', 20), bg=defaultBG,text="Genre: ").grid(row=5,column=0, sticky="w")

        # Declare entry widgets
        self.urlEntry = tk.Entry(self, textvariable=urlString, font=('Helvetica', 18), width=40, selectborderwidth="2",justify="left")
        self.titleEntry = tk.Entry(self, font=('Helvetica', 18))
        self.artistEntry = tk.Entry(self, font=('Helvetica', 18))
        self.albumEntry = tk.Entry(self, font=('Helvetica', 18))
        self.genreEntry = tk.Entry(self, font=('Helvetica', 18))

        # Add Entry Widgets to Frame (separated for ease of readability and accessing entry values
        self.urlEntry.grid(row=1,column=0, columnspan=4, sticky="w")
        self.titleEntry.grid(row=2,column=1, sticky="w")
        self.artistEntry.grid(row=3,column=1, sticky="w")
        self.albumEntry.grid(row=4, column=1, sticky="w")
        self.genreEntry.grid(row=5,column=1, sticky="w")

        # sourceCheck = tk.StringVar().set("web")
        # formatCheck = tk.StringVar().set("mp3")

        # dlFormatCheck = tk.Checkbutton(self, variable=formatCheck,offvalue="mp3", onvalue="mp4", bg=defaultBG, text="Save as videos (.mp4)").grid(row=5, columnspan=3, column=0, sticky="w")
        # automatedDLCheck = tk.Checkbutton(self, variable=sourceCheck,offvalue="web", onvalue="local", bg=defaultBG, text="Download multiple from list (insert filepath in URL)").grid(row=6, columnspan=3, column=0, sticky="w")
        dlButton = tk.Button(self, command= lambda: self.dl_click(), bd=0, font=('Helvetica', 14), bg=defaultBG, text="Download").grid(row=7,column=1, sticky="se")
        # dlButton.config(highlightbackground=defaultBG)

        prefButton = tk.Button(self, command= lambda: self.find_directory(),bd=0, font=('Helvetica', 14), bg=defaultBG, text="Set Dowload Directory").grid(row=7,column=0, sticky="sw")
        # self.config(highlightbackground=defaultBG)
        # for i in range(0,3):
        #   self.grid_columnconfigure(i, weight=1, uniform="main")

    def find_directory(self):
        
        print('line 108 + ' + rootDir)
        with open(rootDir + "/pref.json", 'r+') as pref_data:
            d = json.load(pref_data)
            if len(d["download_location"]) > 0 :
                os.chdir(d["download_location"])
            else :
                os.chdir(d["install_location"])
            d["download_location"] = tk.filedialog.askdirectory()
            downloadDir = d['download_location']
            os.chdir(rootDir)
            updated = json.dumps(d,separators=(', ', ': ')).replace(', ', ', \n').replace('{', '{ \n').replace('}','\n}')
            pref_data.seek(0)
            pref_data.write(updated)

    def dl_click(self):
        # collect optional id3 tags
        global downloadDir
        
        mp3Meta["title"] = self.titleEntry.get()
        mp3Meta["artist"] = self.artistEntry.get()
        mp3Meta["album"] = self.albumEntry.get()
        mp3Meta["genre"] = self.genreEntry.get()
        
        os.chdir(downloadDir)
        startDownload(self.urlEntry.get(), mp3Meta)

# ToDo - Complete prefence windo
# class Preferences(tk.Frame):
#     def __init__(self, master = None):
#         tk.Frame.__init__(self, master)

#         directoryString = tk.StringVar()
#         window = tk.Toplevel(self)

#         defaultBG="#3399ff"
#         # self.parent = master
#         self.pack(expand="true", fill="both")
#         self.configure(bg=defaultBG)

#         # Declare Labels
#         urlString = tk.StringVar()
#         urlLabel = tk.Label(window, pady=5, bg=defaultBG, text="Download Directory: ").grid(row=0,column=0, sticky="w")

#         self.directoryEntry = tk.Entry(window, textvariable=directoryString, selectborderwidth="2",justify="left")
#         self.directoryEntry.grid(row=0, column=1, sticky="w",columnspan=2)
#         directorySelectButton = tk.Button(window, command= lambda: self.find_directory(), bd=0, bg=defaultBG, text="Choose Directory").grid(row=0,column=3, sticky="sw")
    
        
#ToDo implement preferences
# def pref():
    # prefWindow = Preferences()
    # prefWindow.mainloop()

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    global downloadDir
    global rootDir
    global cwd
    global mp3Meta
    global dlStartStatus
    global dlFinishStatus

    # get install location
    rootDir = os.path.dirname(os.path.realpath(__file__))
    
    with open(rootDir + "/pref.json", 'r+') as pref_data:
        d = json.load(pref_data)
        d["install_location"] = rootDir
        if len(d["download_location"]) > 0 :
            downloadDir = d["download_location"]
        else :
            downloadDir = d["install_location"]
        updated = json.dumps(d,separators=(', ', ': ')).replace(', ', ', \n').replace('{', '{ \n').replace('}','\n}')
        pref_data.seek(0)
        pref_data.write(updated)

    dlStartStatus = False
    dlFinishStatus = False

    mp3Meta = {
    "title"  : "Unknown",
    "artist" : "Unknown",
    "album"  : "Unknown",
    "genre"  : "Unknown"}

    root = tk.Tk()
    root.configure(width=3550,height=110)
    for i in range(0,1):
        root.grid_columnconfigure(i, weight=1, uniform="main")

    # ToDo - create a toplevel menu
    # menubar = tk.Menu(root)
    # menubar.add_command(label="Preferences", command=pref)
    # display the menu
    # root.config(menu=menubar)

    root.title("mp3PCDLer")
    root.resizable(0,0)
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()