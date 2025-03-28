import os
import sys
import shutil
from pathlib import Path

from util import startInDefaultProgram
from config import Config

class Screenshotter:
    def __init__(self, config: Config):
        self.config = config

    def transfer(self, dest_filename: str):
        screenshot_dest_folder_path = Screenshotter.relativeToAbsolutePath(self.config.screenshot_dest_folder_name)
        screenshot_path = Screenshotter.newest(self.config.screenshot_source_folder_path)
        Screenshotter.ensureExists(screenshot_dest_folder_path)
        Screenshotter.overwriteTo(screenshot_path, os.path.join(screenshot_dest_folder_path, dest_filename))

    def viewSourceFolder(self):
        startInDefaultProgram(self.config.screenshot_source_folder_path)

    def viewDestFolder(self):
        dest_folder_path = Screenshotter.relativeToAbsolutePath(self.config.screenshot_dest_folder_name)
        Screenshotter.ensureExists(dest_folder_path)
        startInDefaultProgram(dest_folder_path)

    @staticmethod
    def relativeToAbsolutePath(folderName: str):
        # If the 'frozen' flag is set, we are in bundled-app mode!
        # Otherwise, normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
        return os.path.abspath(os.path.join(sys._MEIPASS, folderName)) if getattr(sys, "frozen", False) else os.path.abspath(os.path.join(os.getcwd(), folderName))

    @staticmethod
    def ensureExists(folderPath: str):
        Path(folderPath).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def overwriteTo(source_path: str, destination_path: str):
        shutil.copy2(source_path, destination_path)

    @staticmethod
    def newest(path):
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        return max(paths, key=os.path.getctime)

    