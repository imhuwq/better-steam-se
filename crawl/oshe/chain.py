# encoding: utf-8

import logging
from functools import wraps

from .duty import OsheCrawl, OsheParse, OsheStore

ChainCreated = type("ChainCreated", (Exception,), dict())
DutyNotSupported = type("DutyNotSupported", (Exception,), dict())
DutyRegistered = type("DutyRegistered", (Exception,), dict())
DutyChainEstablished = type("DutyChainEstablished", (Exception,), dict())
DutyChainNotEstablished = type("DutyChainNotEstablished", (Exception,), dict())


def rename_duty_chain_func(new_name):
    def wrapper(duty_chain_func):
        duty_chain_func.__name__ = new_name

        @wraps(duty_chain_func)
        def inner_wrapper(*args, **kwargs):
            return duty_chain_func(*args, **kwargs)

        return inner_wrapper

    return wrapper


class OsheChain:
    def __init__(self, name):
        self.name = name
        self.app = None
        self.crawl_class = None
        self.parse_class = None
        self.store_class = None
        self.duty_chain = None

    def _add_crawl_duty(self, duty_class):
        if self.crawl_class is not None:
            raise DutyRegistered("Chain <{0}> has already registered a crawl class".format(self.name))
        self.crawl_class = duty_class

    def _add_parse_duty(self, duty_class):
        if self.parse_class is not None:
            raise DutyRegistered("Chain <{0}> has already registered a parse class".format(self.name))
        self.parse_class = duty_class

    def _add_store_duty(self, duty_class):
        if self.store_class is not None:
            raise DutyRegistered("Chain <{0}> has already registered a store class".format(self.name))
        self.store_class = duty_class

    def add_duty(self, duty_class):
        if self.duty_chain:
            raise DutyChainEstablished("Duty chain has been established already")

        if issubclass(duty_class, OsheCrawl):
            self._add_crawl_duty(duty_class)
        elif issubclass(duty_class, OsheParse):
            self._add_parse_duty(duty_class)
        elif issubclass(duty_class, OsheStore):
            self._add_store_duty(duty_class)
        else:
            raise DutyNotSupported("{0} is not a supported duty class".format(type(duty_class)))

        if all([self.crawl_class, self.parse_class, self.store_class]):
            @self.app.task
            @rename_duty_chain_func(self.name)
            def _duty_chain_func(init):
                raw = self.crawl_class.run(init)
                data = self.parse_class.run(raw)
                report = self.store_class.run(data)
                logging.info(report)

            self.duty_chain = _duty_chain_func

    def trigger(self, init):
        if self.duty_chain is None:
            raise DutyChainNotEstablished("Duty chain cannot be triggered since it has not been established")
        self.duty_chain.delay(init)
