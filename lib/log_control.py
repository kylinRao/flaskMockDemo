# coding=utf-8
####定义单例的日志logger模块
import configparser
import logging
import logging.config
import os


# cf = ConfigParser.ConfigParser()
# cf.read(os.path.join(os.path.dirname(__file__),'conf','global.conf'))  # 读配置文件（ini、conf）返回结果是列表
# cf.sections()  # 获取读到的所有sections(域)，返回列表类型
# logconfigPath = cf.get(cf.get('global', 'envType'),'logConfig')
# print logconfigPath
class log_control:
    print(os.path.abspath(__file__))
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","conf", 'logger.conf'))
    # logging.config.fileConfig("conf/logger.conf")
    logging.config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","conf", 'logger.conf'))

    ##create logger
    @staticmethod
    def getLogger():
        logger = logging.getLogger('run')
        return logger
