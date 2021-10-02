# -*- coding:utf-8 -*-
import os
import json
from logger import logger


class App:
    def __init__(self, config):
        self.config = config
        self.app_config = self.config.app or dict()
        self.app_path = self.config.app_path or dict()
        self.app_path.update(self._get_app_path())

    def _get_app_path(self):
        app_path = dict()

        app_names = [name for name, _ in self.app_config.items()]
        logger.info("start scan app for {}".format(','.join(app_names)))
        unknown_app_names = [an for an in app_names if an not in self.app_path]
        if len(unknown_app_names) == 0:
            logger.info("scan app done for {}".format(json.dumps(app_path)))
            return app_path

        unknown_app_names = set(unknown_app_names)
        # 默认mac系统, /Application下找
        for root, dirs, files in os.walk('/Applications'):
            for file in files:
                if len(unknown_app_names) == 0:
                    break
                if file in unknown_app_names:
                    unknown_app_names.remove(file)
                    app_path[file] = os.path.join(root, file)
                    logger.info("scan_app||find {}".format(file))
        if len(unknown_app_names) > 0:
            raise Exception('scan_app||can\'t find apps [{}]'.format(','.join(app_names)))
        logger.info("scan app done for {}".format(json.dumps(app_path)))
        return app_path

    def open(self):
        for app, params in self.app_config.items():
            self.app_path[app] = self.app_path[app].replace(" ", "\ ")
            if isinstance(params, (str, int, )):
                cmd = self.app_path.get(app, "") + " "+ params
                logger.info("app||do {}".format(cmd))
                os.popen(cmd)
            elif isinstance(params, (list, )):
                for p in params:
                    cmd = self.app_path.get(app, "") + " " + p
                    logger.info("app||do {}".format(cmd))
                    os.popen(cmd)


class Chrome(App):

    def __init__(self, config):
        self.config = config
        self.app_config = {"Google Chrome": config.chrome}
        self.app_path = self.config.app_path or dict()
        print(self.app_config)
        self.app_path.update(self._get_app_path())

    def open(self):
        return super(Chrome, self).open()


if __name__ == '__main__':
    import config
    a = App(config.get_env_config("driver_card"))
    a.open()

    c = Chrome(config.get_env_config("driver_card"))
    c.open()
