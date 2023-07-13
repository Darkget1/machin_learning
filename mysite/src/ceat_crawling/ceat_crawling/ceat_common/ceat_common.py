import os
import logging
from datetime import datetime

#### CEAT common functions ####
def get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find('CEAT') + len('CEAT')]
    return root_path

def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

#### CEAT common logging class
class ceat_logging():
    logger = ''
    formatter = ''
    file_name = ''
    streamHandler = ''
    fileHandler = ''

    def __init__(self, logger_name, path):
        # logger instance create
        self.logger = logging.getLogger(logger_name)

        # setting log level
        self.logger.setLevel(level=logging.DEBUG)

        # formatter create
        self.formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')

        # handler create
        self.log_file_name = os.path.join(get_root_path(), 'log', str(path) + "_log",
                                          str(datetime.today().year) + "." + str(datetime.today().month) + "." + str(
                                              datetime.today().day) + ".txt")
        self.streamHandler = logging.StreamHandler()
        self.fileHandler = logging.FileHandler(self.log_file_name, encoding='utf-8')

        # setting formatter of logger instance
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # setting handler of logger instance
        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)