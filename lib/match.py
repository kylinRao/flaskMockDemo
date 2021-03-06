# coding=utf-8
import configparser
import os

from lib.common_tools import Util_Tools
from lib.decorate_tools import log_decorate
from lib.Tools import Tools
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
        Tools.runLogHander.debug("初始化完成，已配置的字典如下：")
        Tools.runLogHander.debug(self.config_dic)

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
                uri_pre,request_index, response_value = line.split('|')
                cls.config_dic[content_type].update({uri_pre: {}})
                response_value = response_value.rstrip()
                # cls.config_dic[uri_pre][content_type][request_index] = response_value
                cls.config_dic[content_type][uri_pre].update({request_index: response_value})

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
    def get_request_match_res(cls,uri_pre, content_type, request_str):

        res = ''
        content_type = content_type.lower()

        for request_index in cls.config_dic[content_type][uri_pre].keys():

            if content_type == "application/x-www-form-urlencoded":
                if Util_Tools.compareJson(request_str, request_index):
                    res = cls.config_dic[content_type][uri_pre][request_index]
                else:
                    logControl.getLogger().debug("no response matches,return default error message:")
                    logControl.getLogger().debug({"message", res})
                    res = str(cls.config_dic["default_message"]['message'])
            elif content_type == 'application/json':
                Tools.runLogHander.debug(
                    "开始匹配请求参数：{request_str}    和    {request_index}".format(request_str=str(request_str, "utf-8"),
                                                                            request_index=request_index))
                matchResult = Util_Tools.compareJson(str(request_str, "utf-8"), request_index)
                Tools.runLogHander.debug("字符匹配结果为：{matchResult}".format(matchResult=matchResult))

                if matchResult:
                    res = cls.config_dic[content_type][uri_pre][request_index]
                else:
                    logControl.getLogger().debug("no response matches,return default error message:")
                    logControl.getLogger().debug({"message", res})
                    res = str(cls.config_dic["default_message"])

            logControl.getLogger('interface').info(
                "{content_type}|{request_str}|{response_str}".format(content_type=content_type, request_str=request_str,
                                                                     response_str=res))
            return res



if __name__ == '__main__':
    ##print(match.cf.sections())
    match.reload_config_dic()
    ##print(match.get_request_match_res(content_type='application/json', request_str="""{"a":"b"}"""))
