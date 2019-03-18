# coding:utf-8

import json
from lib.decorate_tools import  log_decorate


class Util_Tools():
    cur = None
    @classmethod
    def toStr(cls, strOrBytes):
        if type(strOrBytes).__name__ == "bytes":
            return strOrBytes.decode("UTF-8")
        else:
            return strOrBytes

    @classmethod
    def convert_doublecomma_to_singlecomma(cls, inputstr):
        return inputstr.replace('"', ",")

    @classmethod
    def convert_to_dictionary(cls, inputstr):
        return eval(inputstr)

    @classmethod
    def number_to_fixed_length_string(cls, number, fixed=5):
        str = "{number}".format(number=number)
        for egg in range(0, fixed - len(str)):
            str = "0" + str
        return str

    @classmethod
    @log_decorate
    def compareJson(cls, realStr, expectStr):
        """用于比较两个json串是否一致，支持模糊匹配@FM，仅校验key是否存在@CK，校验json内部的列表内部的json串，支持递归
         Compare Json    realStr=${res.content}    expectStr=${expectResponse}

         Examples:
         | Compare Json| realStr={"a":"a1"} | expectStr={"a":"a1"} |
         | Compare Json| realStr={"a":[{"innerA":"A"},{"innerB":"B"}]} | expectStr={"a":[{"innerA":"A"},{"innerB":"B"}]} |
         | Compare Json| realStr={"first":{"second":"something"}} | expectStr={"first":{"second":"something"}} |
         | Compare Json| realStr={"a":"abcdefg"} | expectStr={"a":"@FMabc"} |
         | Compare Json| realStr={"a":""} | expectStr={"a":"@CK"} |


        """

        expectStr = cls.toStr(expectStr)
        realStr = cls.toStr(realStr)
        if (not '{' in realStr) and (not '[' in realStr):
            if ((realStr) != (expectStr)):
                print("expect:", expectStr)
                print("in fact:", realStr)
                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=realStr,
                                                                                    expectStrDic=expectStr))
            else:
                return ;



        if "false" in expectStr or "true" in expectStr:

            expectStr=expectStr.replace("false","False").replace("true", "True")
        if "false" in realStr or "true" in expectStr:

            realStr = realStr.replace("false", "False").replace("true", "True")
        if(expectStr=="NC"):
            return ;

        expectStrDic = eval(expectStr)
        realStrDic = eval(realStr)
        print(type(expectStrDic))
        if (type(expectStrDic).__name__ == 'str'):
            if ((realStrDic) != (expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)
                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=realStrDic,expectStrDic=expectStrDic))
            else:
                return True;
        if (type(expectStrDic).__name__ == 'int'):
            if ((realStrDic) != (expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)
                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=realStrDic,expectStrDic=expectStrDic))
            else:
                return True;
        if (type(expectStrDic).__name__ == 'list'):
            if (len(realStrDic) != len(expectStrDic)):
                print("expect:", expectStrDic)
                print("in fact:", realStrDic)

                raise AssertionError("list length not match")
            for (item1, item2) in zip(realStrDic, expectStrDic):
                print(item1, item2)
                cls.compareJson(str(item1), str(item2))
            return
        expectStrDicKeys = expectStrDic.keys()
        realStrDicKeys = realStrDic.keys()

        for k in expectStrDicKeys:
            print(k,expectStrDic[k])
            if k not in realStrDicKeys:
                raise AssertionError("expect key :" + k + " ,but  doesnot found one ")
            elif (type(expectStrDic[k]).__name__ == 'list'):

                if len(realStrDic[k]) != len(expectStrDic[k]):
                    print("expect:", expectStrDic[k])
                    print("in fact:", realStrDic[k])

                    raise AssertionError("list length not match")
                for (item1, item2) in zip(realStrDic[k], expectStrDic[k]):
                    print(item1, item2)
                    print(type(item1))
                    if (type(item1).__name__ == 'str')  :
                        if not (( '{' in item1) or ( '[' in item1)):
                            if ((item1) != (item2)):
                                print("expect:", item2)
                                print("in fact:", item1)
                                raise AssertionError("{realStrDic} not match {expectStrDic}".format(realStrDic=item1,
                                                                                                    expectStrDic=item2))

                    cls.compareJson(str(item1), str(item2))

            elif (type(expectStrDic[k]).__name__ == 'dict'):
                cls.compareJson(str(realStrDic[k]), str(expectStrDic[k]))
            elif "@FM" in str(expectStrDic[k]):
                # 模糊匹配逻辑
                if expectStrDic[k].replace("@FM", "") in realStr:
                    # 模糊匹配ok
                    continue
                else:
                    # 模糊匹配失败
                    raise AssertionError(expectStrDic[k].replace("@FM", "") + " is not in " + realStrDic[k])
            elif "@CK" in str(expectStrDic[k]):
                # 仅检查key存在即可
                continue
            elif expectStrDic[k] != realStrDic[k]:

                raise AssertionError(str(expectStrDic[k]) + " not match " + str(realStrDic[k]))

if __name__ == '__main__':
    realstr = '''{"code":"uworker_1001","msg":"初次登陆","data":"b3ad55a6d9dca80dd6e8f0cb6263968f"}'''
    expectStr = '''{"code":"uworker_1001","msg":"初次登陆","data":"@C"}'''
    ##print(Util_Tools.compareJson(realStr=realstr, expectStr=expectStr))
