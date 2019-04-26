import datetime
import json
import os
import shutil

from flask import request, g

from lib.match import match
from lib.CONSTANTS import CONSTANTS
from lib.Tools import Tools
from lib.common_tools import Util_Tools
import sys


def getHistoryLog():
    Tools.runLogHander.debug("==================================================================")
    Tools.runLogHander.debug(request.url)
    Util_Tools.rm_old_file(CONSTANTS.RES_FILE_DIR, 3)
    g.request_data = request.data
    j_data = json.loads(g.request_data)
    intface_log_file = os.path.join(CONSTANTS.LOG_FILE_DIR, 'interface','interface.log')


    with open(os.path.join(CONSTANTS.LOG_FILE_DIR, 'interface','interface.log'), "rb") as f:
        # 在文本文件中，没有使用b模式选项打开的文件，只允许从文件头开始,只能seek(offset,0)
        file_size = os.path.getsize(intface_log_file)
        if file_size > 1000:

            lastLines = f.readlines()

            # lastLines = f.readlines( -40)
            g.response_data = {"code":100,"desc":"请求成功"}
            g.response_data.update({"historyLog":str(lastLines)})
        else:
            g.response_data = {"code": 100, "desc": "请求成功"}
    return json.dumps(g.response_data)
