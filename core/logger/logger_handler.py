import logging
import os
import pathlib
import sys

from core.utils.constant import Constant

global_logger_name = Constant.TOP_LEVEL_SCOPE
sensitive_info = set()


class Logger:

    def __init__(self):
        self.app_logger = logging

    @staticmethod
    def _add_custom_log_level(logger, name, level_code):
        logging.addLevelName(level_code, name.upper())
        setattr(logger, name.lower(), lambda message, *args: getattr(logger, '_log')(level_code, message, args))

    @classmethod
    def _add_multiple_log_level(cls, logger, custom_log_dict_list):
        for custom_log_dict in custom_log_dict_list:
            cls._add_custom_log_level(logger=logger, name=custom_log_dict['name'],
                                      level_code=custom_log_dict['code'])

    def _hook_handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.app_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    @staticmethod
    def _setup_logger_console(logger, is_use_color_log=True):

        # Just need to display in console when running task file directly
        # define a Handler which writes INFO messages or higher to the sys.stderr

        console = logging.StreamHandler(sys.stdout)

        console.setLevel(logging.INFO)
        logger.addHandler(console)

    def init_deployment_logger(self, logger_name, log_file_path):
        return self.init_logger(logger_name, log_file_path)

    @staticmethod
    def add_log_file_handler(logger, log_file_path, mode, level, log_format):
        log_handler = logging.FileHandler(
            filename=log_file_path, mode=mode)
        log_handler.setLevel(level)
        log_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(log_handler)

    def init_logger(self, logger_name, log_file_path=None, remove_old_log=False) -> logging.Logger:
        logging.getLogger('requests').setLevel(logging.CRITICAL)
        logging.getLogger('botocore').setLevel(logging.CRITICAL)

        log_level = logging.INFO
        log_format = Constant.LOG_FORMAT
        logger = logging.getLogger(logger_name)
        if log_file_path:
            os.makedirs(pathlib.Path(log_file_path).resolve().parents[0], exist_ok=True)
            normal_log_file_path = '{}.log'.format(log_file_path)
            error_log_file_path = '{}_error.log'.format(log_file_path)
            mode = 'w' if remove_old_log else 'a'

            logging.basicConfig(format=log_format,
                                filename=normal_log_file_path,
                                level=log_level, datefmt='%Y-%m-%d %H:%M:%S')

            self.add_log_file_handler(logger=logger, level=logging.ERROR, log_file_path=error_log_file_path,
                                      mode=mode, log_format=log_format)

        self._setup_logger_console(logger)

        logger.info('*********************INIT LOGGING***********************')
        self.app_logger = logger

        sys.excepthook = self._hook_handle_uncaught_exception
        global global_logger_name
        global_logger_name = logger_name
        return logger

    @classmethod
    def get_logger(cls):
        global global_logger_name
        logger = logging.getLogger(global_logger_name or '')
        return logger

    def add_sensitive_info(self, info_list):
        global sensitive_info
        logger = self.get_logger()
        len_sensitive_info_before_update = len(sensitive_info)
        for item in info_list:
            if len(item) < 3:
                logger.warning(
                    'Sensitive info must be a string having more than 3 chars'
                    ' If it still an sensitive info, it mean that your credential is very weak and'
                    'it also affects to your log when filtering')
        sensitive_info.update(info_list)
        if len_sensitive_info_before_update == sensitive_info:
            return
        for handler in logging.root.handlers + logger.handlers:
            handler.setFormatter(RemoveSensitiveInfoFormatter(handler.formatter, patterns=sensitive_info))


class RemoveSensitiveInfoFormatter(logging.Formatter):
    def __init__(self, orig_formatter, patterns):
        super().__init__()
        self.orig_formatter = orig_formatter
        self._patterns = patterns

    def format(self, record):
        msg = self.orig_formatter.format(record)
        for pattern in self._patterns:
            filtered_text = '<filtered>'
            if len(pattern) > 7:
                filtered_text = ''.join(
                    ['*' if index < len(pattern) - 3 else letter for index, letter in enumerate(pattern)])
            msg = msg.replace(pattern, filtered_text)
        return msg

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)
