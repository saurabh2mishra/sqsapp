import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from config import logpath


class Logger:
    """
    Logger class to support console and file level logging.
    Constructor of Logger.

    :param boolean debug: parameter to see console log. By default False for production.
    :param string log_file: log file name
    :param string log_name: log name
    :param string when: indicator to hint log file creation.
    :param int file_log_interval: duration of file rotation
    :returns Logger logger: logger object
    """

    def __init__(self, debug=False, log_file=None, log_name="logs", when='H', file_log_interval=6):
        self._logger = logging.getLogger(log_name)
        self._logger.setLevel(logging.INFO)
        self._logger.handlers = []
        self.debug = debug
        self.file_log_interval = file_log_interval
        self.when = when
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')
        date_dir = datetime.today().strftime('%Y%m%d')

        if log_file is not None:
            filename = log_file
        else:
            filename = f"{log_name}_{datetime.today().strftime('%Y%m%d')}"

        abs_path_of_logfile = os.path.join(os.sep, logpath, date_dir, filename)

        # Creating timed rotating file handler
        createdir(os.path.dirname(abs_path_of_logfile))
        timed_rotating_fh = TimedRotatingFileHandler(filename=abs_path_of_logfile,
                                                     when=self.when, interval=self.file_log_interval)
        timed_rotating_fh.setFormatter(formatter)
        self._logger.addHandler(timed_rotating_fh)

        # Creating console logging
        if self.debug:
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            self._logger.addHandler(sh)

    def get_logger(self):
        return self._logger


def createdir(path):
    """
    Function to create directory.

    :param string path: directory of file
    :returns None:
    """
    try:
        os.makedirs(path, exist_ok=True)
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise