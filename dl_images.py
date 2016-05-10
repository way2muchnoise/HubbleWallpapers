import os
from threading import Thread

import web

base_url = 'http://hubblesite.org/'
album_url = '/gallery/album/entire/npp/all/'
dl_folder = 'downloads/images/'  # relative or absolute
file_type = '-print.jpg'
count = 10  # new download
latest = 50  # only check latest x amount of pictures

if not os.path.exists(dl_folder):
    os.makedirs(dl_folder)


class GetThread(Thread):
    picture = ""
    output = {}

    def __init__(self, picture, output):
        super(GetThread, self).__init__()
        self.picture = picture
        self.output = output

    def run(self):
        page_url = base_url + self.picture
        if web.is_page_reachable(page_url):
            img_page = web.get_page(page_url)
            _imgs = filter((lambda s: s.endswith(file_type)), (link for link in web.get_element(img_page, 'a', '')))
            img = next(_imgs.__iter__(), '')
            if img is not '':
                name = img.split('/')[-1].split(file_type)[0]
                self.output[name] = img
                print 'Added ' + name


page = web.get_page(base_url + album_url)
wallpapers = web.get_element(page, 'a', 'icon')

imgs = {}
threads = []

# Get all wallpaper urls
for wallpaper in wallpapers:
    latest -= 1
    if latest < 1:
        break
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
