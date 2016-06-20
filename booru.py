import json
import urllib
import urllib as urllib2
import cStringIO
import glob
import os
from ttk import Frame, Label, Labelframe
from Tkinter import Tk, Y, Listbox, StringVar, END, LEFT, SUNKEN, NONE, W, Button, Toplevel, BOTTOM, RIGHT, BOTH, TOP, Menubutton, RAISED, Menu
from PIL import Image, ImageTk
from Queue import Queue
from threading import Thread

#TODO Add diffrent boorus
#TODO Store image informations
#TODO Sync database and HDD
#TODO Database view

main_url = "https://danbooru.donmai.us/"

def get_posts(file, query_dict):
    data = urllib.urlencode(query_dict)
    posts = urllib2.urlopen("%s%s?%s" % (main_url, file, data))
    posts = json.loads(posts.read())
    return posts

query_args = {"page":1}
posts = get_posts("posts.json", query_args)

def get_image_from_internet_binary(url):
    return cStringIO.StringIO(urllib2.urlopen(url).read())

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.current_image = posts[0]
        self.posts = posts
        self.initUI()
        self.current_booru = None

    def initUI(self):
        self.parent.title("Booru")
        self.pack(fill=Y, expand=0, side=LEFT)
        self.current_booru_var = StringVar()
        self.mb =  Menubutton(self, textvariable=self.current_booru_var, relief=RAISED)
        self.mb.pack(side=TOP)
        self.mb.menu = Menu(self.mb, tearoff = 0)
        self.mb["menu"] = self.mb.menu 
        self.current_booru_var.set("Danbooru")

        def change_booru(booru):
            self.current_booru = booru
            if self.current_booru == 0:
                self.current_booru_var.set("Danbooru")
            if self.current_booru == 1:
                self.current_booru_var.set("Safebooru")
            if self.current_booru == 1:
                self.current_booru_var.set("Gelbooru")
            #print(self.current_booru)
            
        self.mb.menu.add_command(label="Danbooru", command=lambda : change_booru(0))
        self.mb.menu.add_command(label="Safebooru", command=lambda : change_booru(1))
        self.mb.menu.add_command(label="Gelbooru", command=lambda : change_booru(2))

        self.mb.pack()

        image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, self.posts[0][u"preview_file_url"])))
        photo = ImageTk.PhotoImage(image)
        self.label = Label(self, image=photo)
        self.label.image = photo
        self.label.pack(fill=Y, expand=0, side=LEFT)

        self.lb = Listbox(self)
        for i in self.posts:
            self.lb.insert(END, i["id"])
        self.lb.bind("<<ListboxSelect>>", self.onSelect)
        self.lb.pack(pady=15, fill=Y, expand=0, side=LEFT)

        self.description = Labelframe(self, text="Description")
        self.description.pack(pady=15, fill=Y)
        #artist
        self.artist_v = StringVar()
        self.artist = Label(self.description, textvariable=self.artist_v, justify=LEFT, wraplength=500, anchor=W)
        self.artist.pack()
        #md5
        self.md5_v = StringVar()
        self.md5 = Label(self.description, textvariable=self.md5_v, justify=LEFT, wraplength=500, anchor=W)
        self.md5.pack()
        #source
        self.source_v = StringVar()
        self.source = Label(self.description, textvariable=self.source_v, justify=LEFT, wraplength=500, anchor=W)
        self.source.pack()
        #wxh
        self.wxh_v = StringVar()
        self.wxh = Label(self.description, textvariable=self.wxh_v, justify=LEFT, wraplength=500, anchor=W)
        self.wxh.pack()
        #tags (for now all)
        self.tags_v = StringVar()
        self.tags = Label(self.description, textvariable=self.tags_v, justify=LEFT, wraplength=500, anchor=W)
        self.tags.pack()
        #uploader
        self.uploader_v = StringVar()
        self.uploader = Label(self.description, textvariable=self.uploader_v, justify=LEFT, wraplength=500, anchor=W)
        self.uploader.pack()
        idx = (0,0)
        try:
            self.artist_v.set(u"Artist:\t%s" % self.posts[idx[0]][u"tag_string_artist"])
        except KeyError:
            self.artist_v.set(u"Artist:\t")
        try:
            self.md5_v.set(u"MD5:\t%s" % self.posts[idx[0]][u"md5"])
        except KeyError:
            self.md5_v.set(u"MD5:\t")
        try:
            self.source_v.set(u"Source:\t%s" % self.posts[idx[0]][u"source"])
        except KeyError:
            self.source_v.set(u"Source:\t")
        try:
            self.wxh_v.set(u"Size:\t%sx%s" % (self.posts[idx[0]][u"image_width"], self.posts[idx[0]][u"image_height"]))
        except KeyError:
            self.wxh_v.set(u"Size:\t")
        try:
            self.tags_v.set(u"Tags:\t%s" % self.posts[idx[0]][u"tag_string"])
        except KeyError:
            self.tags_v.set(u"Tags:\t")
        try:
            self.uploader_v.set(u"Uploader:\t%s" % self.posts[idx[0]][u"uploader_name"])
        except KeyError:
            self.uploader_v.set(u"Uploader:\t")

        self.button_frame = Frame(self.description)
        self.button_frame.pack(fill=Y, expand=0, side=LEFT)

        def download_image_current():
            def download():
                urllib.urlretrieve("%s%s" % (main_url, self.current_image[u"file_url"]), "%s_%s.%s" % (self.current_image[u"id"], self.current_image[u"md5"], self.current_image[u"file_ext"]))
            t1 = Thread(target=download, args=())
            t1.start()
        self.download_button = Button(self.button_frame, text="Download", command=download_image_current)
        self.download_button.pack(side=LEFT)
        def bigger_preview():
            self.bigpreview = Toplevel(self)
            image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, self.current_image[u"file_url"])))
            photo = ImageTk.PhotoImage(image)
            labelu = Label(self.bigpreview, image=photo)
            labelu.image = photo
            labelu.pack(fill=Y, expand=0, side=LEFT)
        self.preview_button = Button(self.button_frame, text="Preview", command=bigger_preview)
        self.preview_button.pack(side=RIGHT)
        def onRefresh():
            def method():
                self.posts = get_posts("posts.json", query_args)
                self.lb.delete(0, END)
                for i in self.posts:
                    self.lb.insert(END, i["id"])
            t1 = Thread(target=method, args=())
            t1.start()
        self.refresh = Button(self.button_frame, text="Refresh posts", command=onRefresh)
        self.refresh.pack(side=LEFT)
        """self.file_browser = Listbox(self)
        files_in_download = glob.glob(os.path.join("download", "*.jpg"))
        files_in_download += glob.glob(os.path.join("download", "*.png"))
        files_in_download += glob.glob(os.path.join("download", "*.gif"))
        if files_in_download == [[], []]:
            files_in_download = []
        for i in files_in_download:
            self.file_browser.insert(END, i)
        self.file_browser.bind("<<ListboxSelect>>", self.onSelectFileBrowser)
        self.file_browser.pack(fill=Y, expand=0, side=BOTTOM)"""


    def onSelectFileBrowser(self, val):
        sender = val.widget
        idx = sender.curselection()
        def get_image_and_cover_it(self):
            with open(sender.get(idx), "r") as fre:
                image = Image.open(fre.read())
                photo = ImageTk.PhotoImage(image)
                self.label.configure(image=photo)
                self.label.image = photo
        t1 = Thread(target=get_image_and_cover_it, args=(self,))
        t1.start()

    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        self.current_image = self.posts[idx[0]]
        """
        image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, posts[idx[0]][u"preview_file_url"])))
        photo = ImageTk.PhotoImage(image)
        self.label.configure(image=photo)
        self.label.image = photo
        """
        try:
            self.artist_v.set(u"Artist:\t%s" % self.posts[idx[0]][u"tag_string_artist"])
        except KeyError:
            self.artist_v.set(u"Artist:\t")
        try:
            self.md5_v.set(u"MD5:\t%s" % self.posts[idx[0]][u"md5"])
        except KeyError:
            self.md5_v.set(u"MD5:\t")
        try:
            self.source_v.set(u"Source:\t%s" % self.posts[idx[0]][u"source"])
        except KeyError:
            self.source_v.set(u"Source:\t")
        try:
            self.wxh_v.set(u"Size:\t%sx%s" % (self.posts[idx[0]][u"image_width"], self.posts[idx[0]][u"image_height"]))
        except KeyError:
            self.wxh_v.set(u"Size:\t")
        try:
            self.tags_v.set(u"Tags:\t%s" % self.posts[idx[0]][u"tag_string"])
        except KeyError:
            self.tags_v.set(u"Tags:\t")
        try:
            self.uploader_v.set(u"Uploader:\t%s" % self.posts[idx[0]][u"uploader_name"])
        except KeyError:
            self.uploader_v.set(u"Uploader:\t")
        def get_image_and_cover_it(self):
            image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, self.posts[idx[0]][u"preview_file_url"])))
            photo = ImageTk.PhotoImage(image)
            self.label.configure(image=photo)
            self.label.image = photo
        t1 = Thread(target=get_image_and_cover_it, args=(self,))
        t1.start()

def main():
    root = Tk()
    wMain = Main(root)
    root.geometry()
    root.mainloop()

if __name__ == '__main__':
    main()