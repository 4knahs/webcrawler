import unittest
from crawler_task import CrawlerTask
from url import Url
#import pdb

class TestCrawler(unittest.TestCase):

    
    def test_url_protocol_parsing(self):
        
        self.assertEqual(Url("https://www.google.com").proto(), "https")
        self.assertEqual(Url("http://www.google.com").proto(), "http")
        self.assertEqual(Url("https://google.com").proto(), "https")

    def test_url_no_protocol(self):
        self.assertEqual(Url("//www.apple.com/uk", protocol="https").url(), "https://www.apple.com/uk")
        self.assertEqual(Url("//www.apple.com/uk", protocol="https").proto(), "https")
        self.assertEqual(Url("//www.apple.com/uk").proto(), "http")

    def test_url_relative_parsing(self):
        self.assertEqual(Url("/page", domain="google.com", protocol="http").url(), "http://google.com/page")
        self.assertEqual(Url("/page", domain="www.google.com", protocol="https").url(), "https://www.google.com/page")
        self.assertEqual(Url("/page.co.uk", domain="google.co.uk", protocol="https").url(), "https://google.co.uk/page.co.uk")

    def test_url_domain_parsing(self):
        
        self.assertEqual(Url("http://www.google.com").domain(), "google")
        self.assertEqual(Url("http://google.com").domain(), "google")
        self.assertEqual(Url("www.google.com").domain(), "google")
        self.assertEqual(Url("google.com").domain(), "google")
        self.assertEqual(Url("/page", domain="google.com", protocol="https").domain(), "google")
    
    def test_url_subdomain_parsing(self):

        self.assertEqual(Url("http://www.fake.google.com").subdomain(), "www.fake")
        self.assertEqual(Url("http://fake.google.com").subdomain(), "fake")

    def test_url_suffix_parsing(self):
        self.assertEqual(Url("http://www.google.com").suffix(), "com")
        self.assertEqual(Url("http://www.google.co.uk").suffix(), "co.uk")

    def test_urls_from_page(self):

        c = CrawlerTask("http://example.com")

        self.assertEqual(c.url().proto(), "http")
        self.assertEqual(c.url().domain(), "example")
        self.assertEqual(c.url().suffix(), "com")

        html_doc = """
            <html><head><title>Test</title></head>
            <body>
            <p class="title"><b>Test</b></p>

            <p class="story">Test test
            <a href="http://example.com/test1" class="s" id="link1">Test1</a>,
            <a href="http://example.com/test2" class="s" id="link2">Test2</a> and
            <a href="http://example.com/test3" class="s" id="link3">Test3</a>;
            <a href="test4" class="sister" id="link3">Test4</a>;
            <a href="/test5" class="sister" id="link3">Test5</a>;
            and they lived at the bottom of a well.</p>

            <p class="story">...</p>
        """

        urls = c.urls_from_content(html_doc)

        asserts = ["http://example.com/test1", "http://example.com/test2", "http://example.com/test3", "http://example.com/test4", "http://example.com/test5"]

        for i,u in enumerate(urls):
            self.assertEqual(asserts[i], u.url())

        self.assertEqual(len(urls), 5)

       
if __name__ == '__main__':
    unittest.main()