import datetime
import json
import os
import shutil

from flask import request, g

from lib.match import match
from lib.CONSTANTS import CONSTANTS
from lib.Tools import Tools
from lib.common_tools import Util_Tools


def updateConfig():
    Tools.runLogHander.debug("==================================================================")
    Tools.runLogHander.debug(request.url)
    Util_Tools.rm_old_file(CONSTANTS.RES_FILE_DIR, 3)
    g.request_data = request.data
    j_data = json.loads(g.request_data)

    if j_data["configType"] == "application/json":
        with open(os.path.join(CONSTANTS.RES_FILE_DIR, 'json.res'), "w") as f:
            f.write(j_data["configContent"])
        try:
            ori_file = os.path.join(CONSTANTS.RES_FILE_DIR, 'json.res')
            backupfile = os.path.join(CONSTANTS.RES_FILE_DIR, 'json.res.{datetime}'.format(
                datetime=datetime.datetime.now().strftime(
                    CONSTANTS.FILE_TIME_FORMAT)))
            shutil.copyfile(ori_file, backupfile)
            match.reload_config_dic()
        except:
            os.remove(ori_file)
            shutil.copyfile( backupfile, ori_file)
            match.reload_config_dic()
            g.response_data = {"code":100,"desc":"请按照参考格式填写"}
            return json.dumps(g.response_data)
    g.response_data ={"code":200,"desc":"配置刷新成功"}
    return json.dumps(g.response_data)

def getConfigContent():
    Tools.runLogHander.debug("==================================================================")
    Tools.runLogHander.debug(request.url)
    Util_Tools.rm_old_file(CONSTANTS.RES_FILE_DIR, 3)
    g.request_data = request.data
    j_data = json.loads(g.request_data)
    if j_data["configType"] == "application/json":
        with open(os.path.join(CONSTANTS.RES_FILE_DIR, 'json.res'), "r") as f:
            g.response_data = {"code":200,"desc":"请求成功"}
            g.response_data.update({"configContent":f.read()})
            print(g.response_data )
    return json.dumps(g.response_data)

