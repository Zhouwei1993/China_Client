from china_border import app,BASEPATH,server,info,getSelectSql,updateSql
from flask import render_template,request,redirect,make_response,url_for,jsonify
import traceback,json,uuid,time,os
from PIL import Image
ISOTIMEFORMAT='%Y%m%d'
nowtime = time.strftime( ISOTIMEFORMAT, time.localtime() )
def upload_file(file_storage):
    fileurlpath1 = "china_border/china_border/static/upload/%s"%(nowtime)
    fileurlpath2 = "static/upload/%s"%(nowtime)
    dst_w = 1000
    dst_h = 1000
    save_q = 90
    name,extension = os.path.splitext(file_storage.filename)
    if not os.path.exists(fileurlpath1):
        os.makedirs(fileurlpath1)
    _uuid = uuid.uuid1()
    filename = "%s"%(_uuid) + extension
    file_path1 = os.path.join(fileurlpath1, filename)
    file_path2 = os.path.join(fileurlpath2, filename)
    file_storage.save(file_path1)
    dst_img=ori_img = file_path1
    resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
    picurl=BASEPATH+file_path2
    return picurl
def resizeImg(**args):
    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = Image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth,newHeight),Image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])


