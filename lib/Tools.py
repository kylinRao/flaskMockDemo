import os

from logControl import logControl
class Tools:
    logHander = logControl()
    runLogHander = logHander.getLogger("run")
    fileLogHander = logHander.getLogger("file")
    interfaceHander = logHander.getLogger("interfacelog")
def run_log_decorate(func):
    def decorate_inner(*args, **kwargs):
        Tools.runLogHander.debug("=============当前正在调用函数："+func.__name__)
        if (args):
            Tools.runLogHander.debug([value for value in args])
        if  ( kwargs):
            Tools.runLogHander.debug([key+":"+kwargs[key]+" " for key in kwargs])

        return func(*args, **kwargs)
    return decorate_inner
