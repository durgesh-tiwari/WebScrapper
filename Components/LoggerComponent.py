"""
Dated : 2021-04-25
Class LoggerComponent
This class will create logs at runtime and will help us to find out errors.
"""

import os
import traceback
from datetime import datetime, timezone


class LoggerComponent:
    def __init__(self):
        self.BASE_DIR = os.getcwd()
        self.LOG_DIR = os.path.join(self.BASE_DIR, "Logs")
        if not os.path.exists(self.LOG_DIR):
            os.mkdir(self.LOG_DIR)

        self.log_file_path = os.path.join(self.LOG_DIR, "NaturalGasTool_{}.txt"
                                          .format(datetime.timestamp(datetime.now(timezone.utc))))

        self.error_log_file_path = os.path.join(self.LOG_DIR, "error_logs.txt")

    def log_info(self, message: object=None, exception: BaseException = None) -> None:
        padding = ["\n", "-"*200, "\n"]
        with open(self.log_file_path, "a+") as log_file:
            log_file.write("Run time in UTC : {} \n\n".format(datetime.now(timezone.utc)))
            if message:
                log_file.write(str(message))
            if exception:
                traceback.print_exc(file=log_file)
            log_file.writelines(padding)

    def log_error(self, message: object=None) -> None:
        padding = ["\n", "-"*200, "\n"]
        with open(self.error_log_file_path, "a+") as error_file:
            error_file.write("Run time in UTC : {} \n\n".format(datetime.now(timezone.utc)))
            error_file.write(str(message))
            error_file.writelines(padding)

    def handle_exception(self, exception: BaseException) -> None:
        padding = ["\n", "-"*200, "\n"]
        with open(self.error_log_file_path, "a+") as error_file:
            error_file.write("Run time in UTC : {} \n\n".format(datetime.now(timezone.utc)))
            traceback.print_exc(file=error_file)
            error_file.writelines(padding)
        raise Exception('Error : {}',format(exception))

    def show_progress(self, info: object) -> None:
        print(info)


logger = LoggerComponent()


def debug(func):
    def wrapper(self=None, *args, **kwargs):
        classname = type(self).__name__
        method = func.__name__
        try:
            logger.show_progress(info='Processing {}.{}()'.format(classname, method))
            logger.log_info(message='Processing of {}.{}() \n Attributes Passed as, \n{}\n{}'.format(classname, method, args, kwargs))
            result = func(self, *args, *kwargs)
            logger.show_progress(info="Processing {}.{}() Completed Successfully\n".format(classname, method))
            logger.log_info(message="Processing {}.{}() Completed Successfully\n".format(classname, method))
            return result
        except Exception as e:
            logger.log_info(message="Processing {}.{}() Interrupted\n".format(classname, method))
            logger.log_info(exception=e)
            logger.show_progress(info="Processing {}.{}() Interrupted\n".format(classname, method))
            logger.show_progress(info="Please check \"{}\" for more information".format(logger.log_file_path))
            raise Exception(e)
    return wrapper




