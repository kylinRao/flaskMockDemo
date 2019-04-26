#coding=utf-8
from logControl import logControl
def log_decorate(func):
    def inner(*args,**kwargs):
        '''执行函数之前要做的'''
        logControl.getLogger().info("enter function ---------------------------{func_name}---------------------------".format(func_name=func.__name__))
        logControl.getLogger().debug("##print list or tuple like ipnut args :")
        logControl.getLogger().debug(args)
        logControl.getLogger().debug("##print dic like ipnut kwargs :")
        logControl.getLogger().debug(kwargs)

        response_func = func(*args, **kwargs)
        '''执行函数之后要做的'''
        logControl.getLogger().info(
            "end function ---------------------------{func_name}---------------------------".format(
                func_name=func.__name__))
        return response_func
    return inner