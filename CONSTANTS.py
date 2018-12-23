import fileinput
import configparser

"""
读取配置文件信息
"""


class ConfigParser():
    config_dic = {}
    config_file = 'conf/config.prop'
    cf = configparser.ConfigParser()
    cf.read(config_file, encoding='utf8')  # 注意setting.ini配置文件的路径
    def __init__(self):
        self.reload_config_dic()
    @classmethod
    def reload_config_dic(cls):
        for content_type in cls.cf.sections():
            cls.reload_config_dic(content_type=content_type)

    @classmethod
    def reload_config_dic(cls,content_type):
        res_file = cls.cf.get(content_type, 'config_file')
        with open(res_file, 'r') as f:
            for line in f.read():
                request_index, response_value = line.split('|')
                cls.config_dic[content_type][request_index] = response_value


    @classmethod
    def get_config(cls, sector, item):
        value = None
        try:
            value = cls.config_dic[sector][item]
        except KeyError:

            value = cls.cf.get(sector, item)
            cls.config_dic = value
        finally:
            return value
    # @classmethod
    # def get_all_sections(cls):
    #     return cls.cf.sections()
    @classmethod
    def get_request_match_res(cls,content_type,request_str):
        res = 'no match'
        content_type = content_type.lower()
        if content_type=='application/json':
            for request_index in cls.config_dic[content_type].keys():
                if compareJson(request_str,request_index):
                    return cls.config_dic[content_type][request_index]
                else:
                    return {"code",res}
        return cls.get_config(sector=content_type,item=request_str)



class CONSTANTS:
    MATCH_DIC = {}

    def __init__(self):
        self.refresh_match_dic()

    @staticmethod
    def refresh_match_dic(filename="matchResponse.py"):
        CONSTANTS.MATCH_DIC = {}
        for line in fileinput.input(filename):
            uri, request_match, response_match = line.split("|")
            CONSTANTS.MATCH_DIC.update({"uri": uri, "request_match": request_match, "response_match": response_match})


if __name__ == '__main__':
    print(configparser.__doc__)
    print(ConfigParser.get_all_sections())
    con = ConfigParser

    res = con.get_config('logging', 'level')
    print(res)
