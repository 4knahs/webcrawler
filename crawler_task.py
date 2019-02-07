from url import Url

# Parser for xml/html, handles unicode/utf-8 encoding otherwise managed when fetching the website via urllib
from bs4 import BeautifulSoup

import urllib

from logger import warn, info, debug, error

class CrawlerTask:

    def __init__(self, url, domain=None, protocol=None):

        self.crawl_url = Url(url, domain=domain, protocol=protocol)
        
    def urls_from_content(self, content):
        """Retrieves the URLs from a request content.
    
        Keyword arguments:
        content -- page content, as retrieved via urllib urlopen or compatible with lxml.
        """
        if content:
            bs = BeautifulSoup(content, 'lxml')
            urls = []
        
            for u in bs.findAll('a'):
                new_url = Url(u.get('href'), domain = self.crawl_url.netloc(), protocol=self.crawl_url.proto())
                if new_url == None or new_url == '':
                    error("Failed to process {}".format(u.get('href')))
                else:
                    urls.append(new_url)

            return urls
        else:
            return []

    def url(self):
        """Retrieves the crawler's URL.
        """
        return self.crawl_url

    def crawl(self):
        """Retrieves the urls present in the crawler's URL.
        """
        return {
            'urls': self.urls_from_content(self.crawl_url.content()),
            'parent': self.crawl_url.url()
        }

    def __call__(self):
        return self.crawl()

    def __str__(self):
        return self.crawl_url.url()