import os
import re
import abc
import requests
from lxml import etree

from crawl.oshe import OsheCrawl, OsheParse, OsheStore
from crawl.oshe import OsheApp

from . import instance

steam = OsheApp("steam")
steam.config_from_object(instance)


class SteamCrawl(OsheCrawl):
    worker = requests

    headers = {'user-agent': 'User-Agent:Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/55.0.2883.75 Safari/537.36',
               'host': 'store.steampowered.com',
               'connection': 'keep-alive'
               }

    cookies = {'birthtime': '667753201',
               'lastagecheckage': '1-March-1991',
               'Steam_Language': 'english',
               'steamCountry': 'CN',
               'mature_content': '1'
               }

    proxies = {
        "http": os.getenv("crawl_worker_http_proxy", None),
        "https": os.getenv("crawl_worker_https_proxy", None)
    }


class SteamParse(OsheParse):
    worker = etree

    @classmethod
    def strip_strings(cls, strings):
        result = []
        pattern = re.compile(r'^([\t\n\s]*)(?P<item>.*?)([\t\n\s]*)$')
        for item in strings:
            item = pattern.sub(r'\g<item>', item)
            result.append(item)
        return result

    def build_html(self):
        return self.worker.HTML(self.raw)

    @abc.abstractmethod
    def run(self):
        """
        所有子类复写该函数以实现该类的具体职责
        """


SteamStore = type("SteamStore", (OsheStore,), dict())

from .game_index import *
from .game_list import *
from .game_detail import *
