import logging.config
import os.path


class DocumentExplorerLogger:
    logger_name = 'DocumentExplorerTest'
    logger_config_file = '/Users/ashukla/PycharmProjects/DocumentExplorerTest/logger.cfg'

    if os.path.isfile(logger_config_file):
        logging.config.fileConfig(logger_config_file)

    log = logging.getLogger(logger_name)

    def __init__(self):
        self.log.info('DocumentExplorerLogger: __init__')

    def log_enter(self, method):
        self.log.debug('==> %s()', method)

    def log_exit(self, method):
        self.log.debug('<== %s()', method)

    def log_debug(self, msg, test_name=None):
        if test_name is None:
            self.log.debug(str(msg))
        else:
            self.log.debug('test name=%s: %s', test_name, str(msg))

    def log_info(self, msg, test_name=None):
        if test_name is None:
            self.log.info(str(msg))
        else:
            self.log.info('test name=%s: %s', test_name, str(msg))

    def log_warning(self, msg, test_name=None):
        if test_name is None:
            self.log.warning(str(msg))
        else:
            self.log.warning('test name=%s: %s', test_name, str(msg))

    def log_error(self, msg, test_name=None):
        if test_name is None:
            self.log.error(str(msg))
        else:
            self.log.error('test name=%s: %s', test_name, str(msg))

    def log_fatal(self, msg, test_name=None):
        if test_name is None:
            self.log.critical(str(msg))
        else:
            self.log.critical('test name=%s: %s', test_name, str(msg))
