# encoding: utf-8

from functools import wraps

from celery import Celery

from .chain import OsheChain

ChainNotFound = type("ChainNotFound", (Exception,), dict())


class OsheApp(Celery):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.instance = None
        self.chains = dict()
        super(OsheApp, self).__init__(self.name, *args, **kwargs)

    def config_from_object(self, instance, silent=False, force=False, namespace=None):
        self.instance = instance
        super(OsheApp, self).config_from_object(instance, silent, force, namespace)

    def chain(self, chain_name):
        chain = self.chains.get(chain_name, None)
        if chain is None:
            chain = OsheChain(chain_name)
            self.chains[chain_name] = chain
            chain.app = self

        def wrapper(duty_class):
            chain.add_duty(duty_class)

            @wraps(duty_class)
            def inner_wrapper(*args, **kwargs):
                return duty_class(*args, **kwargs)

            return inner_wrapper

        return wrapper

    def trigger(self, chain_name, init, *args, **kwargs):
        chain = self.chains.get(chain_name, None)
        if chain is None:
            raise ChainNotFound("{0} is not a registered chain".format(chain_name))
        chain.trigger(init, *args, **kwargs)
