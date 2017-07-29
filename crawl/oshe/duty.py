# encoding: utf-8

import abc


class DutyClass(abc.ABC):
    app = None
    chain = None
    worker = None


class OsheCrawl(DutyClass):
    headers = None
    cookies = None
    proxies = None

    def __init__(self, url):
        self.url = url

    @abc.abstractmethod
    def run(self):
        """
        所有子类复写该函数以实现该类的具体职责
        """


class OsheParse(DutyClass):
    def __init__(self, raw):
        self.raw = raw
        self.html = self.build_html()
        self.result = dict()

    @abc.abstractclassmethod
    def build_html(self):
        """
        所有子类复写该函数以实现从 raw 中构建 html 的过程
        """

    @abc.abstractmethod
    def run(self):
        """
        所有子类复写该函数以实现该类的具体职责
        """


class OsheStore(DutyClass):
    def __init__(self, data):
        self.data = data

    @abc.abstractmethod
    def run(self):
        """
        所有子类复写该函数以实现该类的具体职责
        """
