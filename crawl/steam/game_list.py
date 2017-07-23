from . import steam
from . import SteamCrawl, SteamParse, SteamStore


@steam.chain("game_list")
class GameListCrawl(SteamCrawl):
    def run(self):
        pass


@steam.chain("game_list")
class GameListParse(SteamParse):
    def run(self):
        pass


@steam.chain("game_list")
class GameListStore(SteamStore):
    def run(self):
        pass
