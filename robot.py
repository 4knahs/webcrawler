#from urllib.robotparser import RobotFileParser
from robotexclusionrulesparser import RobotExclusionRulesParser

from urllib.parse import urljoin

from url import Url

class Robot:
    def __init__(self, url):
        self.url = Url(urljoin(url, '/robots.txt'))
        self.rerp = RobotExclusionRulesParser()
        self.rerp.user_agent = 'Mozilla/5.0'
        self.rerp.fetch(self.url.url())

    def throttle_time(self):
        return self.rerp.get_crawl_delay('Mozilla/5.0')

    def should_block(self,url):
        return not self.rerp.is_allowed('Mozilla/5.0', url.url())
