# encoding: utf-8

import os
import logging
import traceback
from datetime import datetime
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
    def __init__(self, name, app):
        self.name = name
        self.app = app
        self.crawl_class = None
        self.parse_class = None
        self.store_class = None
        self.duty_chain = None

        self.running = True

        self.init = None
        self.raw = None
        self.data = None

        self.std_log = logging.getLogger(self.name + "_std")
        self.std_log.setLevel(logging.INFO)
        std_log_file = os.path.join(self.app.logs_dir, self.name + "_std.log")
        self.std_log.addHandler(logging.FileHandler(std_log_file))

        self.err_log = logging.getLogger(self.name + "_err")
        self.err_log.setLevel(logging.ERROR)
        err_log_file = os.path.join(self.app.logs_dir, self.name + "_err.log")
        self.err_log.addHandler(logging.FileHandler(err_log_file))

    def log_std(self, message):
        self.std_log.info(message)

    def log_err(self, message):
        self.err_log.error(message)

    def auto_log_duty_chain(self, duty_chain):
        @wraps(duty_chain)
        def wrapper(*args, **kwargs):
            message = "[{0}] {1}: \nargs: {2}\nkwargs: {3}\n".format(datetime.now(), self.name, args, kwargs)
            try:
                duty_chain(*args, **kwargs)
            except Exception as err:
                message = "{0}\n{1}\n".format(message, traceback.format_exc())
                self.log_err(message)
                raise err
            else:
                self.log_std(message)

        return wrapper

    def try_to_establish_full_chain(self):
        if all([self.crawl_class, self.parse_class, self.store_class]):
            @self.app.task
            @rename_duty_chain_func(self.name)
            @self.auto_log_duty_chain
            def _duty_chain_func(init):
                self.init = init
                if self.running:
                    self.raw = self.crawl_class(init).run()
                if self.running:
                    self.data = self.parse_class(self.raw).run()
                if self.running:
                    self.store_class(self.data).run()

            self.duty_chain = _duty_chain_func

    def add_duty(self, duty_class):
        if self.duty_chain:
            raise DutyChainEstablished("Duty chain has been established already")

        if issubclass(duty_class, OsheCrawl):
            if self.crawl_class is not None:
                raise DutyRegistered("Chain <{0}> has already registered a crawl class".format(self.name))
            self.crawl_class = duty_class
        elif issubclass(duty_class, OsheParse):
            if self.parse_class is not None:
                raise DutyRegistered("Chain <{0}> has already registered a parse class".format(self.name))
            self.parse_class = duty_class
        elif issubclass(duty_class, OsheStore):
            if self.store_class is not None:
                raise DutyRegistered("Chain <{0}> has already registered a store class".format(self.name))
            self.store_class = duty_class
        else:
            raise DutyNotSupported("{0} is not a supported duty class".format(type(duty_class)))

        duty_class.app = self.app
        duty_class.chain = self
        self.try_to_establish_full_chain()

    def trigger(self, init):
        if self.duty_chain is None:
            raise DutyChainNotEstablished("Duty chain cannot be triggered since it has not been established")
        self.duty_chain.delay(init)
