from . import steam
from . import SteamCrawl, SteamParse, SteamStore


@steam.chain("game_list")
class GameListCrawl(SteamCrawl):
    def run(self):
        raw = self.worker.get(url=self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        return raw.text


@steam.chain("game_list")
class GameListParse(SteamParse):
    def run(self):
        search_result_div = self.html.xpath("//div[@id='search_result_container']")[0].xpath("div")[1]
        game_link_list = search_result_div.xpath("a/@href")
        for game_link in game_link_list:
            self.app.trigger("game_detail", game_link)
        return game_link_list


@steam.chain("game_list")
class GameListStore(SteamStore):
    def run(self):
        pass
