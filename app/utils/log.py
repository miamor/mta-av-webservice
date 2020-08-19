import logging
from ..settings.parameters import LOG_FOLDER
import datetime
import os
import threading

threadLock = threading.Lock()


def _common_logger(type, filename, log_content):
    threadLock.acquire()
    logger = logging.getLogger('hemm_ods')
    # log_content = today.strftime("%Y-%m-%d %H:%M:%S") + " - Digi thread: " + content
    # with open(filename, "a+") as file:
    #     file.write(log_content)
    logging.basicConfig(level=type)

    fh = logging.FileHandler(filename)
    fh.setLevel(type)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if type == logging.INFO:
        logger.info(msg=log_content)
    elif type == logging.ERROR:
        logger.error(msg=log_content)
    elif type == logging.WARNING:
        logger.warning(msg=log_content)
    else:
        logger.info(msg=log_content)
    formatter = None
    fh.close()
    logger = None
    threadLock.release()


def log_digi(content):
    if content is None or len(str(content).strip()) == 0:
        return
    today = datetime.datetime.today()
    filename = os.path.join(LOG_FOLDER, str(today.year) + str(today.month) + str(today.day) + "_digi_log_.txt")
    _common_logger(type=logging.INFO, filename=filename, log_content=content)


def log_mofa(content):
    if content is None or len(str(content).strip()) == 0:
        return
    today = datetime.datetime.today()
    filename = os.path.join(LOG_FOLDER, str(today.year) + str(today.month) + str(today.day) + "_mofa_log_.txt")
    _common_logger(type=logging.INFO, filename=filename, log_content=content)


def log_hemmelrath(content):
    if content is None or len(str(content).strip()) == 0:
        return
    today = datetime.datetime.today()
    filename = os.path.join(LOG_FOLDER,
                            str(today.year) + str(today.month) + str(today.day) + "_hemmelrath_log.txt")
    _common_logger(type=logging.INFO, filename=filename, log_content=content)


def log_sql_error(content):
    if content is None or len(str(content).strip()) == 0:
        return
    today = datetime.datetime.today()
    filename = os.path.join(LOG_FOLDER, str(today.year) + str(today.month) + str(today.day) + "_sql_log_.txt")
    _common_logger(type=logging.ERROR, filename=filename, log_content=content)


def log_main(content):
    if content is None or len(str(content).strip()) == 0:
        return
    today = datetime.datetime.today()
    filename = os.path.join(LOG_FOLDER,
                            str(today.year) + str(today.month) + str(today.day) + "_main_log_.txt")
    _common_logger(type=logging.INFO, filename=filename, log_content=content)

# if __name__ == '__main__':
#     # log_digi("This is Digi log")
#     # log_digi("The second Digi log")
#     # log_mofa("This is MOFA log")
#     log_sql_error(content="Error on updating SQL")
