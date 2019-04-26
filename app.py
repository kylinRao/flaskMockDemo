import datetime
import os
import shutil

from flask import Flask, request, g, json
from lib.CONSTANTS import CONSTANTS
from lib.Tools import Tools
from lib.api.logRead import getHistoryLog
from lib.common_tools import Util_Tools
from lib.api.configApi import updateConfig,getConfigContent
from lib.match import match
from lib.api.mockApi import mock
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


# routes = Blueprint('routes', __name__)
app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter


@app.after_request
def after_routes(environ):
    Tools.runLogHander.debug(type(g.request_data).__name__)
    Tools.runLogHander.debug("===========================================")
    Tools.runLogHander.debug(g.response_data)

    try:
        if type(g.request_data).__name__ == 'bytes':
            if ("reloadConfigContent" in request.url) or ("getHistoryLog" in request.url):
                pass
            else:
                Tools.interfaceHander.info("{url}|{contentType}|{method}|{request_str}|{response}".format(url=request.url,
                                                                                                      contentType=request.headers.get(
                                                                                                          "Content-Type"),
                                                                                                      method=request.method,
                                                                                                      request_str=str(
                                                                                                          g.request_data,
                                                                                                          "utf-8"),
                                                                                                      response=g.response_data))
        elif type(g.request_data).__name__ == 'str':
            Tools.interfaceHander.info("{url}|{contentType}|{method}|{request_str}|{response}".format(url=request.url,
                                                                                                      contentType=request.headers.get(
                                                                                                          "Content-Type"),
                                                                                                      method=request.method,
                                                                                                      request_str=g.request_data,
                                                                                                      response=g.response_data))

    except:
        Tools.runLogHander.debug("匹配mock uri过程，不记录接口日志")
    return environ
@app.before_request
def before_routes():
    Tools.runLogHander.debug(request.url)
    Tools.runLogHander.debug(request.host_url)
    Tools.runLogHander.debug("初始请求：")
    Tools.runLogHander.debug(request.headers)
    Tools.runLogHander.debug(request.data)

def init_dynamic_routers():
    uris = []
    for root, dirs, files in os.walk(CONSTANTS.RES_FILE_DIR):
        for file in files:
            Tools.runLogHander.debug("注册{file}中".format(file=file))
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resfile', file), 'r') as f:
                for line in f.readlines():
                    Tools.runLogHander.debug(line)
                    uri_pre, request_index, response_value = line.split('|')
                    uris.append(uri_pre)
    uris_tuple = tuple(uris)
    for item in uris_tuple:
        Tools.runLogHander.debug("启动时注册路由中，当前注册：{item}".format(item=item))
    g.response_data = '{"result":200}'
    return g.response_data


if __name__ == '__main__':
    app.add_url_rule("/api/config/reloadConfigContent", view_func=updateConfig, methods=['get', 'post'])
    app.add_url_rule("/api/config/getConfigContent", view_func=getConfigContent, methods=['get', 'post'])
    app.add_url_rule("/api/config/getHistoryLog", view_func=getHistoryLog, methods=['get', 'post'])
    app.add_url_rule("/<re('.*'):something>", view_func=mock, methods=['get', 'post'])



    match.reload_config_dic()
    Tools.runLogHander.debug("初始化结束")
    Tools.runLogHander.debug(match.config_dic)
    app.run(host="0.0.0.0", debug=True)
