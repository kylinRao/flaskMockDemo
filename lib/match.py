# coding=utf-8
import configparser
import os

from lib.common_tools import Util_Tools
from lib.decorate_tools import log_decorate
from logControl import logControl

"""
读取配置文件信息
"""


class match:
    config_dic = {}
    config_dic.update({"default_message": {"message": "not match"}})

    # config_file = 'conf/resconfig.prop'
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "conf", 'resconfig.prop')
    cf = configparser.ConfigParser()
    cf.read(config_file, encoding='utf8')  # 注意setting.ini配置文件的路径

    @log_decorate
    def __init__(self):
        self.reload_config_dic(self)

    @classmethod
    @log_decorate
    def reload_config_dic(cls):
        for content_type in cls.cf.sections():
            logControl.getLogger().debug("find config in sections:  " + content_type)
            cls.config_dic.update({content_type: {}})
            cls.reload_config_dic_one_content_type(content_type=content_type)
        logControl.getLogger().debug("config_dic is initializing and the result is:")
        logControl.getLogger().debug(cls.config_dic)

    @classmethod
    @log_decorate
    def reload_config_dic_one_content_type(cls, content_type):
        res_file = cls.cf.get(content_type, 'config_file')
        res_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resfile", res_file)

        with open(res_file, 'r') as f:
            for line in f.readlines():
                request_index, response_value = line.split('|')
                cls.config_dic[content_type][request_index] = response_value
                cls.config_dic[content_type].update({request_index: response_value})

    @classmethod
    @log_decorate
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[sector][item]
        except KeyError:

            value = cls.cf.get(sector, item)
            cls.config_dic = value
        finally:
            return value

    @classmethod
    @log_decorate
    def get_request_match_res(cls, content_type, request_str):

        res = ''
        content_type = content_type.lower()

        for request_index in cls.config_dic[content_type].keys():

            if content_type == "application/x-www-form-urlencoded":
                if Util_Tools.compareJson(request_str, request_index):
                    res =  cls.config_dic[content_type][request_index]
                else:
                    log_control.getLogger().debug("no response matches,return default error message:")
                    log_control.getLogger().debug({"message", res})
                    res =  str(cls.config_dic["default_message"]['message'])
            elif content_type == 'application/json':
                if Util_Tools.compareJson(request_str, request_index):
                    res =  cls.config_dic[content_type][request_index]
                else:
                    log_control.getLogger().debug("no response matches,return default error message:")
                    log_control.getLogger().debug({"message", res})
                    res =  str(cls.config_dic["default_message"])

        log_control.getLogger('interface').info("{content_type}|{request_str}|{response_str}".format(content_type=content_type,request_str=request_str,response_str=res))
        return res

if __name__ == '__main__':
    ##print(match.cf.sections())
    match.reload_config_dic()
    ##print(match.get_request_match_res(content_type='application/json', request_str="""{"a":"b"}"""))
