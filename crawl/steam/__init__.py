import os
import requests

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

    @classmethod
    def run(cls, url, headers=None, cookies=None, proxies=None):
        headers = headers or cls.headers
        cookies = cookies or cls.cookies
        proxies = proxies or (cls.proxies if cls.proxies.get("http") else None)
        raw = cls.worker.get(url=url, headers=headers, cookies=cookies, proxies=proxies)
        return raw.text


SteamParse = type("SteamParse", (OsheParse,), dict())
SteamStore = type("SteamStore", (OsheStore,), dict())

from .game_list import *
