from . import steam
from . import SteamCrawl, SteamParse, SteamStore


@steam.chain("game_index")
class GameIndexCrawl(SteamCrawl):
    def run(self):
        raw = self.worker.get(url=self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        return raw.text


@steam.chain("game_index")
class GameIndexParse(SteamParse):
    def run(self):
        pagination = self.html.xpath("//div[@class='search_pagination_right']")[0]
        last_page = pagination.xpath("a")[-2].xpath("text()")[0]
        last_page = int(last_page)
        for page_index in range(1, last_page + 1):
            self.app.trigger("game_list", "{0}&page={1}".format(self.chain.init, page_index))


@steam.chain("game_index")
class GameIndexStore(SteamStore):
    def run(self):
        pass
