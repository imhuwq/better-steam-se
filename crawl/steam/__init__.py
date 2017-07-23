from crawl.oshe import OsheCrawl, OsheParse, OsheStore
from crawl.oshe import OsheApp

from . import instance

steam = OsheApp("steam", instance)

SteamCrawl = type("SteamCrawl", (OsheCrawl,), dict())
SteamParse = type("SteamParse", (OsheParse,), dict())
SteamStore = type("SteamStore", (OsheStore,), dict())

from .game_list import *
