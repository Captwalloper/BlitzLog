import os
import sys
import shutil
from pathlib import Path

class Screenshotter:
    def __init__(self):
        self.folderPath = ''

    def setup(self):
        path = 'op_screenshots'
        if getattr(sys, "frozen", False):
            # If the 'frozen' flag is set, we are in bundled-app mode!
            self.folderPath = os.path.abspath(os.path.join(sys._MEIPASS, path))
        else:
            # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
            self.folderPath = os.path.abspath(os.path.join(os.getcwd(), path))

    def transfer(self, op: int, mission: int):
        steam_screenshot_folder = 'C:\\Program Files (x86)\\Steam\\userdata\\47539735\\760\\remote\\553850\\screenshots'
        # screenshot_path = self.__newest(steam_screenshot_folder)

        files = os.listdir(steam_screenshot_folder)
        paths = [os.path.join(steam_screenshot_folder, basename) for basename in files]
        screenshot_path = max(paths, key=os.path.getctime)

        # ensure op folder exists
        op_folder = os.path.join(self.folderPath, f'OP_{op}')
        Path(op_folder).mkdir(parents=True, exist_ok=True)
        # self.__copy_file_with_overwrite(screenshot_path, os.path.join(op_folder, f'M{mission}'))
        source_path = screenshot_path
        destination_path = os.path.join(op_folder, f'M{mission}.jpg')
        try:
            shutil.copy2(source_path, destination_path)
            print(f"File copied successfully from {source_path} to {destination_path} (overwritten if existed).")
        except FileNotFoundError:
            print(f"Error: Source file {source_path} not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # def __copy_file_with_overwrite(source_path: str, destination_path: str):
    #     """
    #     Copies a file from source to destination, overwriting if the destination exists.

    #     Args:
    #         source_path (str): The path to the source file.
    #         destination_path (str): The path to the destination file.
    #     """
    #     try:
    #         shutil.copy2(source_path, destination_path)
    #         print(f"File copied successfully from {source_path} to {destination_path} (overwritten if existed).")
    #     except FileNotFoundError:
    #         print(f"Error: Source file {source_path} not found.")
    #     except Exception as e:
    #         print(f"An error occurred: {e}")

    # def __newest(path):
    #     files = os.listdir(path)
    #     paths = [os.path.join(path, basename) for basename in files]
    #     return max(paths, key=os.path.getctime)

    