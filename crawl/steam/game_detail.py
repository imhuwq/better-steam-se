import re
from collections import namedtuple

from lxml import etree

from . import steam
from . import SteamCrawl, SteamParse, SteamStore

ReleaseDate = namedtuple("release_date", ["year", "month", "day"])


@steam.chain("game_detail")
class GameDetailCrawl(SteamCrawl):
    def run(self):
        raw = self.worker.get(url=self.url, headers=self.headers, cookies=self.cookies, proxies=self.proxies)
        if raw.status_code != 200:
            self.chain.running = False
        return raw.text


@steam.chain("game_detail")
class GameDetailParse(SteamParse):
    def check_accessibility(self):
        if self.html.xpath("//div[@id='error_box']"):
            self.chain.running = False

    def parse_appid(self):
        url = self.chain.init
        appid = re.findall("http://.*?/app/(.*?)/.*?", url, re.DOTALL)
        self.result["appid"] = appid

    def parse_tags(self):
        try:
            tags_div = self.html.xpath("//div[@class='glance_tags popular_tags']")[0]
        except IndexError:
            tags = []
        else:
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
            if len(options) == 4:
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
        win = self.html.xpath("div[@data-os='win']") != []
        mac = self.html.xpath("div[@data-os='mac']") != []
        linux = self.html.xpath("div[@data-os='linux']") != []

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

        try:
            comment_filter_div = self.html.xpath("//div[@class='user_reviews_filter_section']")[0]
        except IndexError:
            all_counts, positive_counts, negative_counts = [0, 0, 0]
        else:
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

        def parse_name():
            name = re.findall("<b>名称:</b>(.*?)<br/>", details, re.DOTALL)
            name = SteamParse.strip_strings(name)[0] if name else ""
            self.result["name"] = name.strip()

        def parse_genres():
            genres = re.findall("<b>类型:</b>(.*?)<br/>", details, re.DOTALL)
            genres = genres[0] if genres else ""
            genres = re.findall("<a href=.*?>(.*?)</a>", genres, re.DOTALL)
            self.result["genres"] = genres

        def parse_developers():
            developers = re.findall("<b>开发商:</b>(.*?)<br/>", details, re.DOTALL)
            developers = developers[0] if developers else ""
            developers = re.findall("<a href=.*?>(.*?)</a>", developers, re.DOTALL)
            self.result["developers"] = developers

        def parse_publishers():
            publishers = re.findall("<b>发行商:</b>(.*?)<br/>", details, re.DOTALL)
            publishers = publishers[0] if publishers else ""
            publishers = re.findall("<a href=.*?>(.*?)</a>", publishers, re.DOTALL)
            self.result["publishers"] = publishers

        def parse_release_date():
            if self.html.xpath("//div[contains(@class, 'game_area_comingsoon')]"):
                self.result["release_date"] = ReleaseDate(1970, 1, 1)
                return

            release_date = re.findall("<b>发行日期:</b>(.*?)<br/>", details, re.DOTALL)
            release_date = SteamParse.strip_strings(release_date)[0] if release_date else ""
            if release_date:
                release_date = re.split("[年月日]", release_date)
                release_date = release_date + [0] * 4
                year, month, day, *_ = release_date
                release_date = ReleaseDate(int(year or 1970), int(month or 0), int(day or 0))
                self.result["release_date"] = release_date
            else:
                self.result["release_date"] = ReleaseDate(1970, 1, 1)

        parse_name()
        parse_genres()
        parse_developers()
        parse_publishers()
        parse_release_date()

    def run(self):
        self.check_accessibility()

        if self.chain.running:
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
