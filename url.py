# Wrapper around urllib to properly handle country code top-level domains
# Fetches data from Mozilla's Public Suffix List
import tldextract

# Used for the url parsing
from urllib.parse import urljoin, urlparse

from urllib.request import Request, urlopen

import urllib

from urllib.error import URLError, HTTPError

from logger import warn, info, debug, error

# Required for local cache
import os

# For proper error logging
import traceback

tld = tldextract.TLDExtract(
    # Use local cache of suffix to avoid call to Mozilla
    suffix_list_urls=["file://{}/public_suffix_list.dat".format(os.getcwd())],
    # Keep local cache of suffixes
    cache_file='{}/cache.tmp'.format(os.getcwd()))

class Url:
    def __init__(self, original_url, domain=None, protocol="http"):

        if protocol:
            self.protocol = protocol
        else:
            self.protocol = "http"

        self.original_url = original_url
        self.original_domain = domain
        self.full_url = None


    def url(self):
        """Returns the full URL by expanding the protocol and relative paths.
        """

        # Empty href fields
        if self.original_url == None:
            return ""

        # Avoid processing the URL multiple times
        if self.full_url:
            return self.full_url
        
        t = tld(self.original_url)
        domain = t.domain
        suffix = t.suffix
        scheme = urlparse(self.original_url).scheme

         # Handle relative paths (e.g. href=abc or href=/abc)
        if self.original_domain and self.protocol and (domain == '' or suffix == ''):
            self.full_url = urljoin('{}://{}'.format(self.protocol, self.original_domain), self.original_url)
        elif domain == '':
            # Ocasionally we get phone numbers on the href fields
            error('Relative paths require a protocol and domain to be specified: {}'.format(self.original_url))
            self.full_url = self.original_url
        elif scheme == '':
            # Handle missing protocol (e.g., //apple.com)
            self.full_url = urlparse('{}://{}'.format(self.protocol, self.original_url)).geturl()
        else:
            # Other cases return the original url
            self.full_url = self.original_url

        return self.full_url
    
    def netloc(self):
        """Returns the url with protocol and path parameters removed.
        """
        url = self.url()

        return urlparse(url).netloc

    def path(self):
        """Returns the url path parameters.
        """
        url = self.url()

        return urlparse(url).path

    def domain(self):
        """Returns the url domain.
        """

        url = self.url()

        if tld(url).domain != '':
            return tld(url).domain
        else:
            # Ocasionally we get phone numbers of the href fields
            error('URL without domain {}'.format(url))
        
        return ''

    def subdomain(self):
        """Returns the url subdomain.
        """

        url = self.url()

        return tld(url).subdomain

    def suffix(self):
        """Returns the url suffix.
        """

        url = self.url()

        return tld(url).suffix

    def proto(self):
        """Returns the url protocol.
        """
        url = self.url()

        return urlparse(url, scheme=self.protocol).scheme

    def content(self):
        """Returns the url content.
        """
        url = self.url()

        if url != '':

            # Using a common user agent to avoid getting blocked by webservers.
            # Note that different user agents might be served different versions
            # of the pages.
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            try:
                return urlopen(req)
            except HTTPError as e:
                error('HTTPError = ' + str(e.code))
            except URLError as e:
                error('URLError = ' + str(e.reason))
            except Exception:
                # TODO: catch lower level Exceptions first
                error('Exception: ' + traceback.format_exc())

            return None
