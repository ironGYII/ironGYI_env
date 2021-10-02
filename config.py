# -*- coding:utf-8 -*-
import os
import yaml
from logger import logger

__all__ = ['get_env_config', 'set_config_path']

config_path = '~/my_env.conf'


def get_config_path():

    if config_path.startswith('~'):
        return os.environ['HOME'] + config_path[1:]
    return config_path


def set_config_path(path):
    try:
        with open(path, 'r') as fs:
            config = yaml.load(fs, Loader=yaml.FullLoader)
    except Exception:
        raise Exception("配置文件路径不存在")
    global config_path
    config_path = path


class ConfigParser(type):

    def __new__(cls, sub_class, bases, attrs):
        try:
            with open(get_config_path(), 'r') as fs:
                config = yaml.load(fs, Loader=yaml.FullLoader)
                if config is None:
                    raise Exception("配置文件为空, 路径: {}".format(get_config_path()))
                logger.info("加载配置文件{}成功".format(get_config_path()))

                app_path = config.get("app_path")
                # 加载当前配置需要的配置文件
                env = attrs.get("env_name", None)
                if env is None:
                    raise Exception("未定义工作环境名称:env_name")
                if config is None:
                    raise Exception("配置文件查找环境配置失败 env_name: {}".format(env))

                config = config.get(env)
                env_config = cls._config_attrs(cls, config)
                env_config['app_path'] = app_path
                attrs.update(env_config)
                logger.info("获取环境 {} 配置成功".format(env_config))
        except Exception as e:
            raise Exception("加载配置文件错误:  {}".format(str(e)))

        return super().__new__(cls, sub_class, bases, attrs)

    def _config_attrs(cls, config):
        ret = dict(app=config.get("app"),
                   chrome=config.get("chrome"),
                   tmux=config.get("tmux"))
        return ret


def get_env_config(env_name):
    return ConfigParser("EnvConfig", (), {"env_name": env_name})


if __name__ == '__main__':
    get_env_config("hello")