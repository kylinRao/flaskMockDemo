from logControl import logControl
class Tools:
    logHander = logControl()
    runLogHander = logHander.getLogger("run")
    fileLogHander = logHander.getLogger("file")
def run_log_decorate(func):
    def decorate_inner(*args, **kwargs):
        Tools.runLogHander.debug("=============当前正在调用函数："+func.__name__)
        if (args):
            Tools.runLogHander.debug([value for value in args])
        if  ( kwargs):
            Tools.runLogHander.debug([key+":"+value+" " for key,value in zip(**kwargs)])

        # print(type(args), type(kwargs))
        # print('args', args, 'kwargs', kwargs)
        return func(*args, **kwargs)
    return decorate_inner