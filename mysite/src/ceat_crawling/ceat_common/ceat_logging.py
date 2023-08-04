import os
import sys
import inspect
import logging
from datetime import datetime

#### CEAT common functions ####
def ceat_get_root_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    root_path = cur_path[:cur_path.find('CEAT') + len('CEAT')]
    return root_path

def ceat_create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def ceat_print_info():
    ### line number
    '''
      여기를 호출한 곳의 라인위치(라인번호)를 리턴한다.
    '''
    cf = inspect.currentframe()
    linenumber = cf.f_back.f_lineno

    ### Call to Function name
    '''
      여기를 호출한 곳의 함수이름(function name(def))를 리턴한다.
    '''
    func_name = cf.f_back.f_code.co_name

    ### file name
    '''
      여기를 호출한 파일 이름을 리턴한다.
    '''
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    get_filename = filename.split('\\')[-1]

    return f'{get_filename}({func_name}.{linenumber})'

#### CEAT common logging  ####
class ceat_logging_default():
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
      self.logger = logger
      self.level = level
      self.linebuf = ''

    def write(self, buf):
      for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

class ceat_logging():
    def __init__(self, logging_storage):
        logging_storage_path = os.path.join(ceat_get_root_path(), "log", str(logging_storage) + "_log", datetime.today().strftime('%Y.%m.%d_%H.%M.%S.%f') + ".txt")
        self.set_logging_default(logging_storage_path)
        print("======================================== Logging Start! ========================================")

    def set_logging_default(self, logging_storage_path):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(logging_storage_path, 'a', 'utf-8')
        handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s][%(thread)d] -> [%(message)s]'))
        logger.addHandler(handler)
        sys.stdout = ceat_logging_default(logger, logging.INFO)
        sys.stderr = ceat_logging_default(logger, logging.ERROR)