#coding=utf-8

from china_border import app,BASEPATH,server,info,getSelectSql,url_for
from flask import render_template,request,redirect,make_response
import traceback,json,datetime,flask_login,time,calendar
from functools import reduce
@app.route('/index', methods=['GET'])
def index():
    resp= render_template('login.html', basepath=BASEPATH)
    return resp

def getTree(value, key):
    k = key[::-1]
    _k = []
    _v = []
    for i, j in enumerate(k):
        _k += [[k[i], k[i + 1]]] if i < len(k) - 1 else [[k[i]]]
    for g, h in enumerate(_k):
        if g == 0:
            lit = [{"name": l[h[0]], "parent": l[h[-1]], "value": l} for l in value]
        elif g == len(_k) - 1:
            lit = [{"name": l[h[0]], "children": []} for l in value]
        else:
            lit = [{"name": l[h[0]], "parent": l[h[-1]], "children": []} for l in value]
        _v.append(lit)
    _v = [reduce(lambda x, y: x if y in x else x + [y], [[], ] + __v) for __v in _v]  # 清晰数组，去除重复项
    return reduce(mkTree, _v)
def mkTree(x, y):
    for i, j in enumerate(y):
        y[i]["children"] += [k for k in x if k["parent"] == j["name"]]
    return y

@app.route('/', methods=['GET'])
def web():
    return redirect(url_for("index"))