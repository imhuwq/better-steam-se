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
        url = self.chain.init
        appid = re.findall("http://.*?/app/(.*?)/.*?", url, re.DOTALL)
        self.result["appid"] = appid

    def parse_tags(self):
        tags_div = self.html.xpath("//div[@class='glance_tags popular_tags']")[0]
        tags = tags_div.xpath("a/text()")
        tags = SteamParse.strip_strings(tags)
        self.result["tags"] = tags

    def parse_features(self):
        features = self.html.xpath("//div[@class='game_area_details_specs']/a/text()")
        self.result["features"] = features

    def parse_languages(self):
        languages = dict()
        language_options = self.html.xpath("//table[@class='game_language_options']/tr")[1:]
        for language_option in language_options:
            options = language_option.xpath("td")
            language = SteamParse.strip_strings(options[0].xpath("text()"))[0]
            ui = options[1].xpath("img") != []
            audio = options[2].xpath("img") != []
            dialog = options[3].xpath("img") != []

            languages[language] = {
                "UI": ui,
                "Audio": audio,
                "Dialog": dialog
            }

        self.result["languages"] = languages

    def parse_os(self):
        os_div = self.html.xpath("//div[@class='sysreq_tabs']")[0]
        win = os_div.xpath("div[@data-os='win']") != []
        mac = os_div.xpath("div[@data-os='mac']") != []
        linux = os_div.xpath("div[@data-os='linux']") != []

        self.result["os"] = {
            "win": win,
            "mac": mac,
            "linux": linux
        }

    def parse_comments(self):
        def convert_count(count_num_str):
            if count_num_str:
                return int(re.sub(r"[,()]", "", count_num_str, re.DOTALL))
            return 0

        comment_filter_div = self.html.xpath("//div[@class='user_reviews_filter_section']")[0]
        counts = comment_filter_div.xpath("label/span[@class='user_reviews_count']/text()")
        counts = map(convert_count, counts)
        all_counts, positive_counts, negative_counts = counts
        self.result["comments"] = {
            "all": all_counts,
            "positive": positive_counts,
            "negative": negative_counts
        }

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
        self.parse_os()
        self.parse_comments()

        return self.result


@steam.chain("game_detail")
class GameDetailStore(SteamStore):
    def run(self):
        pass
