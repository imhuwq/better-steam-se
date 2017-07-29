import re
from datetime import datetime

from lxml import etree

from . import steam
from . import SteamCrawl, SteamParse, SteamStore


@steam.chain("game_detail")
class GameDetailCrawl(SteamCrawl):
    def run(self):
        raw = self.worker.get(url=self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        return raw.text


@steam.chain("game_detail")
class GameDetailParse(SteamParse):
    def parse_appid(self):
        pass

    def parse_tags(self):
        pass

    def parse_features(self):
        pass

    def parse_languages(self):
        pass

    def parse_requirements(self):
        pass

    def parse_comments(self):
        pass

    def parse_details(self):
        detail_block = self.html.xpath("//div[@class='details_block']")[0]
        details = etree.tostring(detail_block, encoding="utf8").decode("utf8")
        details = re.findall("<div class=\"details_block\">(.*?)</div>", details, re.DOTALL)[0]
        details = re.sub("(&#13;)|\n|\t", "", details)
        details = details.split("<br/>")
        details = [detail for detail in details if detail]

        # parse_name
        name_block = details[0]
        name = name_block.split("</b>")[-1].strip()
        self.result["name"] = name

        # parse_genres
        genre_block = details[1]
        genres = re.findall("<a href=.*?>(.*?)</a>", genre_block, re.DOTALL)
        self.result["genres"] = genres

        # parse_developers
        developer_block = details[2]
        developers = re.findall("<a href=.*?>(.*?)</a>", developer_block, re.DOTALL)
        self.result["developers"] = developers

        # parse_publishers
        publisher_block = details[3]
        publishers = re.findall("<a href=.*?>(.*?)</a>", publisher_block, re.DOTALL)
        self.result["publishers"] = publishers

        # parse_release_date
        release_date_block = details[4]
        release_date = release_date_block.split("</b>")[-1].strip()
        release_date = datetime.strptime(release_date, "%d %b, %Y")
        self.result["release_date"] = release_date

    def run(self):
        self.parse_appid()
        self.parse_tags()
        self.parse_details()
        self.parse_features()
        self.parse_languages()
        self.parse_requirements()
        self.parse_comments()


@steam.chain("game_detail")
class GameDetailStore(SteamStore):
    def run(self):
        pass
