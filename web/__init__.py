import urllib
import urllib2
import re
from HTMLParser import HTMLParser


class HTMLTagFinder(object, HTMLParser):
    tag = ""
    css_class = ""
    data = []
    depth = 0

    whiteSpace = re.compile("\\s{2,}")
    leadingSpace = re.compile("^\\s+")

    def __init__(self, tag, css_class):
        HTMLParser.__init__(self)
        self.tag = tag
        self.css_class = css_class
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == self.tag:
            save = False
            link = ''
            for attr in attrs:
                if self.css_class == '' or (attr[0] == 'class' and attr[1] == self.css_class):
                    save = True
                if attr[0] == 'href' or attr[0] == 'src':
                    link = attr[1]
            if save:
                self.data.append(link)

    def feed(self, data):
        super(HTMLTagFinder, self).feed(data)
        return self.data


# gets the page html returns nothing if the page is unreachable
def get_page(url, headers={}, post_data=None):
    if post_data is not None:
        url = urllib2.Request(url, headers=headers, data=urllib.urlencode(post_data))
    else:
        url = urllib2.Request(url, headers=headers)
    response = is_page_reachable(url)
    if response is not None:
        return response.read()
    return


# gets the response object can be None
def get_page_raw(url, headers={}, post_data=None):
    if post_data is not None:
        url = urllib2.Request(url, headers=headers, data=urllib.urlencode(post_data))
    else:
        url = urllib2.Request(url, headers=headers)
    response = is_page_reachable(url)
    return response


# Returns None if it is unreachable and the response if it is
def is_page_reachable(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        return
    except urllib2.URLError as e:
        return


def get_element(page, tag, css_class):
    if page is not None:
        return HTMLTagFinder(tag, css_class).feed(page)


def download_page(url, filename):
    urllib.urlretrieve(url, filename)
