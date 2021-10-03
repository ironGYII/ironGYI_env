# -*- coding:utf8 -*-

import commandr
from config import get_env_config, set_config_path
from app import Chrome, App


class Cmd:
    _config = None
    def __init__(self, env_name, category=None, config_path=None):
        self.env_name = env_name
        self.category = category or [App, Chrome]
        if config_path is not None:
            set_config_path(config_path)

    @property
    def config(self):
        if self._config is None:
            self._config= get_env_config(self.env_name)
        if self._config is None:
            raise Exception('unknown config')
        return self._config

    def do(self):
        for o in self.category:
            o(self.config).open()


@commandr.command("open")
def open(env_name, config_path=None, category_strs=None):
    category_strs = category_strs or 'ac'
    cm = dict(a=App, c=Chrome)
    category = []
    for chr in category_strs:
        category.append(cm[chr])
    Cmd(env_name=env_name, category=category, config_path=config_path).do()


def Main():
    commandr.Run()


if __name__ == '__main__':
    pass