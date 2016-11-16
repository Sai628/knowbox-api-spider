# coding=utf-8

import sys
from flask import Flask


# 解决输出中文报错 UnicodeEncodeError 的问题
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


if __name__ == '__main__':
    from manage import manager
    manager.run()
