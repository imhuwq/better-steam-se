# encoding: utf-8

import os
from functools import wraps

from celery import Celery

from .chain import OsheChain

ChainNotFound = type("ChainNotFound", (Exception,), dict())


class OsheApp(Celery):
    def __init__(self, name, *args, **kwargs):
        self.name = name

        self.instance = None
        self.logs_dir = None

        self.chains = dict()
        super(OsheApp, self).__init__(self.name, *args, **kwargs)

    def config_from_object(self, instance, silent=False, force=False, namespace=None):
        self.instance = instance

        logs_dir = getattr(instance, "logs_dir", "/tmp/logs/{0}".format(self.name))
        os.makedirs(logs_dir, mode=0o777, exist_ok=True)
        self.logs_dir = logs_dir

        super(OsheApp, self).config_from_object(instance, silent, force, namespace)

    def chain(self, chain_name):
        chain = self.chains.get(chain_name, None)
        if chain is None:
            chain = OsheChain(chain_name, self)
            self.chains[chain_name] = chain

        def wrapper(duty_class):
            chain.add_duty(duty_class)

            @wraps(duty_class)
            def inner_wrapper(*args, **kwargs):
                return duty_class(*args, **kwargs)

            return inner_wrapper

        return wrapper

    def trigger(self, chain_name, init):
        chain = self.chains.get(chain_name, None)
        if chain is None:
            raise ChainNotFound("{0} is not a registered chain".format(chain_name))
        chain.trigger(init)
