import os
from threading import Thread

import re

import web

base_url = 'http://hubblesite.org/'
wallpaper_url = 'images/wallpaper/'
wallpaper_size = '1920x1200'
imgsrc = 'http://imgsrc.hubblesite.org'
dl_folder = 'downloads/wallpapers/'  # relative or absolute
count = 20

if not os.path.exists(dl_folder):
    os.makedirs(dl_folder)


class GetThread(Thread):
    wallpaper = ""
    output = {}

    def __init__(self, wallpaper, output):
        super(GetThread, self).__init__()
        self.wallpaper = wallpaper
        self.output = output

    def run(self):
        page_url = base_url + self.wallpaper
        if web.is_page_reachable(page_url):
            img_page = web.get_page(page_url)
            img_links = web.get_element(img_page, 'a', '')
            for img_link in img_links:
                if img_link.startswith(imgsrc) and wallpaper_size in img_link:
                    if img_link is not '':
                        self.output[self.wallpaper.split('/')[-2]] = img_link
                        print 'Added ' + self.wallpaper.split('/')[-2]


page = web.get_page(base_url + wallpaper_url)
links = web.get_element(page, 'a', '')
wallpapers = []
pattern = re.compile(r'/image/\d+/wallpaper')
for link in links:
    if pattern.match(link):
        wallpapers.append(link)

imgs = {}
threads = []

# Get all wallpaper urls
for wallpaper in wallpapers:
    thread = GetThread(wallpaper, imgs)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

# Download given count of new ones
for name, img in imgs.iteritems():
    dest = dl_folder + name + '.' + img.split('.')[-1]
    if (not os.path.isfile(dest)) and web.is_page_reachable(img):
        thread = web.download_page_threaded(img, dest)
        thread.start()
        threads.append(thread)
        count -= 1
        if count < 1:
            break
for thread in threads:
    thread.join()
