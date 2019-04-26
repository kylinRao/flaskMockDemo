

from flask import request, g, json

from lib.Tools import run_log_decorate, Tools
from lib.match import match

@run_log_decorate
# @app.route('/mock', methods=['get', 'post'])
def mock(something=""):
    uri_pre = request.url.lstrip(request.host_url)
    uri_pre = "/"+ uri_pre
    Tools.runLogHander.debug(request.url)
    if request.form.to_dict():
        Tools.runLogHander.debug("获取到表单数据")
        g.request_data = request.form.to_dict()
    elif request.data:
        Tools.runLogHander.debug("获取到二进制数据")
        g.request_data = request.data
    else:
        Tools.runLogHander.debug("未获取到任何请求参数")
        g.request_data = "no data"
    if not request.headers.get("Content-Type"):
        return "请求类型不明或者Content-Type未传"
    # ##print(request.method)
    # ##print(request.method, request.headers)
    # ##print("headers展示：")
    # ##print(type(request.headers))
    # ##print(request.environ['CONTENT_TYPE'])
    # ##print(request.data)
    # log_control.getLogger().info(request.headers['Content-Type'])
    if "application/x-www-form-urlencoded" in  request.headers['Content-Type'] :
        # log_control.getLogger().info(request.headers['Content-Type'] )
        #
        # log_control.getLogger().info(str(request.form.to_dict()))
        g["request_data"] = str(request.form.to_dict())
        g["response_data"] = match.get_request_match_res(uri_pre=uri_pre,content_type="application/x-www-form-urlencoded",
                                                         request_str=str(request.form.to_dict()))

        return g["response_data"]
    elif  "application/json" in request.headers['Content-Type'] :
        Tools.runLogHander.debug("json 输入字符串为：")
        Tools.runLogHander.debug(request.headers['Content-Type'])
        Tools.runLogHander.debug(str(request.data))
        g.request_data = request.data
        g.response_data = match.get_request_match_res(uri_pre=uri_pre,content_type="application/json",
                                                      request_str=request.data)
    else:
        g.response_data="当前尚未支持类型:{contenttype}".format(contenttype=request.headers['Content-Type'])

    return g.response_data
