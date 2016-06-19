import json
import urllib
import urllib2
import cStringIO
from ttk import Frame, Label, Labelframe
from Tkinter import Tk, Y, Listbox, StringVar, END, LEFT, SUNKEN, NONE, W, Button
from PIL import Image, ImageTk
from Queue import Queue
from threading import Thread

main_url = "https://danbooru.donmai.us/"
query_args = {"page":1}

data = urllib.urlencode(query_args)
posts = urllib2.urlopen("%sposts.json?%s" % (main_url, data))

posts = json.loads(posts.read())

def get_image_from_internet_binary(url):
    return cStringIO.StringIO(urllib2.urlopen(url).read())

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.current_image = posts[0]

    def initUI(self):
        self.parent.title("Booru")
        self.pack(fill=Y, expand=1, side=LEFT)
        lb = Listbox(self)
        for i in posts:
            lb.insert(END, i["id"])
        lb.bind("<<ListboxSelect>>", self.onSelect)
        lb.pack(pady=15, fill=Y, expand=0, side=LEFT)
        image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, posts[0][u"preview_file_url"])))
        photo = ImageTk.PhotoImage(image)
        self.label = Label(self, image=photo)
        self.label.image = photo
        self.label.pack(fill=Y, expand=0, side=LEFT)

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
        def download_image_current():
            def download():
                urllib.urlretrieve("%s%s" % (main_url, self.current_image[u"file_url"]), "%s_%s.%s" % (self.current_image[u"id"], self.current_image[u"md5"], self.current_image[u"file_ext"]))
            t1 = Thread(target=download, args=())
            t1.start()
        self.download_button = Button(self, text="Download", command=download_image_current)
        self.download_button.pack()


    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        self.current_image = posts[idx[0]]
        """
        image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, posts[idx[0]][u"preview_file_url"])))
        photo = ImageTk.PhotoImage(image)
        self.label.configure(image=photo)
        self.label.image = photo
        """
        try:
            self.artist_v.set(u"Artist:\t%s" % posts[idx[0]][u"tag_string_artist"])
        except KeyError:
            self.artist_v.set(u"Artist:\t")
        try:
            self.md5_v.set(u"MD5:\t%s" % posts[idx[0]][u"md5"])
        except KeyError:
            self.md5_v.set(u"MD5:\t")
        try:
            self.source_v.set(u"Source:\t%s" % posts[idx[0]][u"source"])
        except KeyError:
            self.source_v.set(u"Source:\t")
        try:
            self.wxh_v.set(u"Size:\t%sx%s" % (posts[idx[0]][u"image_width"], posts[idx[0]][u"image_height"]))
        except KeyError:
            self.wxh_v.set(u"Size:\t")
        try:
            self.tags_v.set(u"Tags:\t%s" % posts[idx[0]][u"tag_string"])
        except KeyError:
            self.tags_v.set(u"Tags:\t")
        try:
            self.uploader_v.set(u"Uploader:\t%s" % posts[idx[0]][u"uploader_name"])
        except KeyError:
            self.uploader_v.set(u"Uploader:\t")
        def get_image_and_cover_it(self):
            image = Image.open(get_image_from_internet_binary(u"%s%s" % (main_url, posts[idx[0]][u"preview_file_url"])))
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