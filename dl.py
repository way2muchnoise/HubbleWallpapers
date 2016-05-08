import os

import web

base_url = 'http://hubblesite.org/'
wallpaper_size = '1920x1200'
wallpaper_suffix = '_wallpaper'
dl_folder = 'downloads/'  # relative or absolute
count = 5

if not os.path.exists(dl_folder):
    os.makedirs(dl_folder)

page = web.get_page(base_url + '/gallery/wallpaper/')
wallpapers = web.get_element(page, 'a', 'icon wallpaper')
imgs = []
for wallpaper in wallpapers:
    page_url = base_url + wallpaper + wallpaper_size + wallpaper_suffix
    if web.is_page_reachable(page_url):
        img_page = web.get_page(page_url)
        img = web.get_element(img_page, 'img', '')[1]
        if img is not '':
            imgs.append(img)
            print 'Added ' + img
            if len(imgs) > count-1:
                break
for img in imgs:
    if web.is_page_reachable(img):
        print 'Downloading ' + img
        dest = dl_folder + img.split('/')[-1]
        web.download_page(img, dest)
