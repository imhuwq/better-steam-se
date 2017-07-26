# encoding: utf-8

import abc


class DutyClass(abc.ABC):
    worker = None
    pass


class OsheCrawl(DutyClass):
    headers = None
    cookies = None
    proxies = None

    @classmethod
    @abc.abstractmethod
    def run(cls, *args, **kwargs):
        """
        所有子类复写该函数以实现该类的具体职责
        """


class OsheParse(DutyClass):
    headers = None
    cookies = None

    @classmethod
    @abc.abstractmethod
    def run(cls, *args, **kwargs):
        """
        所有子类复写该函数以实现该类的具体职责
        """


class OsheStore(DutyClass):
    headers = None
    cookies = None

    @classmethod
    @abc.abstractmethod
    def run(cls, *args, **kwargs):
        """
        所有子类复写该函数以实现该类的具体职责
        """
