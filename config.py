from __future__ import annotations
import configparser
import os

from util import startInDefaultProgram

class Config:
    __FILENAME = 'config.ini'
    def __init__(self):
        self.screenshot_source_folder_path: str = ''
        self.screenshot_dest_folder_name: str = ''

    def reload(self):
        cp = configparser.ConfigParser()
        cp.read(Config.__FILENAME)
        self.screenshot_source_folder_path = cp.get('paths', 'screenshot_source_folder_path', fallback='')
        self.screenshot_dest_folder_name = cp.get('paths', 'screenshot_dest_folder_name', fallback='')
        return self

    #static
    __config: Config = None
    @staticmethod
    def get():
        if (Config.__config == None):
            Config.__config = Config()
            Config.__config.reload()
        return Config.__config
    @staticmethod
    def __createExample():
        config = Config()
        config.screenshot_source_folder_path = 'C:\\Program Files (x86)\\Steam\\userdata\\substitute-with-your-path-as-needed'
        config.screenshot_dest_folder_name = 'op_screenshots'
        cp = configparser.ConfigParser()
        with open(Config.__FILENAME, 'w') as configfile:
            cp.add_section('paths')
            cp.set('paths', 'screenshot_source_folder_path', config.screenshot_source_folder_path)
            cp.set('paths', 'screenshot_dest_folder_name', config.screenshot_dest_folder_name)
            cp.write(configfile)
        return config
    @staticmethod
    def ensureGet():
        config = Config.get()
        if (config.screenshot_source_folder_path == '' or config.screenshot_dest_folder_name == ''):
            config = Config.__createExample()
        return config
    @staticmethod
    def viewInDefaultProgram():
        startInDefaultProgram(Config.__FILENAME)
    