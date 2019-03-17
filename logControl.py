#coding=utf-8
####定义单例的日志logger模块
import configparser
import  logging
import logging.config
import os

# cf = ConfigParser.ConfigParser()
# cf.read(os.path.join(os.path.dirname(__file__),'conf','global.conf'))  # 读配置文件（ini、conf）返回结果是列表
# cf.sections()  # 获取读到的所有sections(域)，返回列表类型
# logconfigPath = cf.get(cf.get('global', 'envType'),'logConfig')
# print logconfigPath
class logControl:
	# printos.path.abspath(__file__)
	##create logger
	log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"conf", 'logger.conf')
	print(log_file)
	# 初始化log目录
	# 	print(handle.__doc__)
	cp = configparser.ConfigParser()
	cp.read(log_file)
	hlist = cp["handlers"]["keys"]
	print(hlist)
	for hand in hlist.split(','):
		print(hand)
		section = cp["handler_%s" % hand]
		args = section.get("args", '()')
		if 'sys.stdout' not in args:
			args = eval(args)
			print(args[0])
			path_name = os.path.dirname(os.path.join(os.path.dirname(os.path.abspath(__file__)), args[0]))
			print(path_name)
			print(os.path.exists(path_name))
			try:
				print("正在新建log相关目录")
				os.makedirs(path_name)
			except Exception:
				print(Exception.mro())
				print("文件目录{path}已存在，无需重复创建".format(path=path_name))

	logging.config.fileConfig(log_file)
	# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
	# print(logging.getLogger().__doc__)
	# print(dir(logging.config))
	# for handle in logging._handlerList:





	def __init__(self):
		self.runLogHandle = logControl.getLogger("run")
	@staticmethod
	def getLogger(logerType="run"):
		logger = logging.getLogger(logerType)
		return logger

