#coding=utf-8
from lib.log_control import log_control
def log_decorate(func):
    def inner(*args,**kwargs):
        '''执行函数之前要做的'''
        log_control.getLogger().info("enter function ---------------------------{func_name}---------------------------".format(func_name=func.__name__))
        log_control.getLogger().debug("##print list or tuple like ipnut args :")
        log_control.getLogger().debug(args)
        log_control.getLogger().debug("##print dic like ipnut kwargs :")
        log_control.getLogger().debug(kwargs)
        # if args:
        #     for item in args:
        #         logControl.getLogger().debug('list like item:'+item)
        # if kwargs:
        #     for key,value in kwargs:
        #         logControl.getLogger().debug('dic like item:' + key +" "+ value)

        response_func = func(*args, **kwargs)
        '''执行函数之后要做的'''
        return response_func
    return inner