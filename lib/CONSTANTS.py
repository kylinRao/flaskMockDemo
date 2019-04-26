import os


class CONSTANTS:
    FILE_TIME_FORMAT = "%Y_%m_%d_%H_%M_%S"
    RES_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", 'resfile')
    LOG_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", 'logs')