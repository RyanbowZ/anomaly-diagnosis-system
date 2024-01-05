import cgi
import traceback
import cgitb
import json
import sys
from flask_cors import CORS
from flask import Flask, request, jsonify,make_response  # 导入Flask类
app = Flask(__name__)  # 实例化flask
CORS(app)
@app.route('/ainfo', methods=['GET', 'POST'])

def testGet():
    data=request.get_json(silent=True)
    print(data["search"])
    print(data["arithmetic"])
    return "hello"
    # todo something


#@app.route('/', methods=['GET', 'DELETE', 'POST'])

if __name__ == '__main__':
    app.run()
