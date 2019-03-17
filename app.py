from flask import Flask, request, Blueprint, url_for, redirect

from lib.Tools import run_log_decorate, Tools
from lib.match import match

routes = Blueprint('routes', __name__)
app = Flask(__name__)
app.register_blueprint(routes,)





@app.before_request
def before_routes():
    Tools.runLogHander.debug(request.url)
    if "/mock" not in request.url:
        return redirect(url_for('mock'))


@run_log_decorate
@app.route('/')
def hello_world():
    Tools.runLogHander.debug(request.url)
    return 'Hello World!'

@run_log_decorate
@app.route('/mock', methods=['get', 'post'])
def mock():
    Tools.runLogHander.debug("mock here")
    # ##print(request.method)
    # ##print(request.method, request.headers)
    # ##print("headers展示：")
    # ##print(type(request.headers))
    # ##print(request.environ['CONTENT_TYPE'])
    # ##print(request.data)
    # log_control.getLogger().info(request.headers['Content-Type'])
    if request.headers['Content-Type'] == "application/x-www-form-urlencoded":
        # log_control.getLogger().info(request.headers['Content-Type'] )
        #
        # log_control.getLogger().info(str(request.form.to_dict()))
        return match.get_request_match_res(content_type=request.headers['Content-Type'],
                                           request_str=str(request.form.to_dict()))
    else:
        # log_control.getLogger().info(request.data)
        return match.get_request_match_res(content_type=request.headers['Content-Type'],
                                           request_str=request.data)


if __name__ == '__main__':
    ##print(match.cf.sections())
    match.reload_config_dic()
    app.run(host="0.0.0.0",debug=False)
