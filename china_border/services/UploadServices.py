# -*- coding: utf-8 -*-

import os,io,pycurl
import uuid
import time
from china_border import BASEPATH,IMAGE1_UPLOAD_PATH,IMAGE1_BASEPATH
from PIL import Image
ISOTIMEFORMAT='%Y%m%d'
nowtime = time.strftime( ISOTIMEFORMAT, time.localtime() )

def upload_image(file_storage):
    _uuid = uuid.uuid1()
    ori_img = file_storage

    #目标图片大小
    dst_w = 1000
    dst_h = 1000
    #保存的图片质量
    save_q = 90
    #等比例压缩
    # ori_img = 'E:/python/xqd_edu_web/edu_web/static/upload/91ef76c6a7efce1bf3efe4bca951f3deb58f65fb.jpg'
    # dst_img = 'E:/python/xqd_edu_web/edu_web/static/upload/icon_022.jpg'
    name, extension = os.path.splitext(file_storage.filename)
    filename = "%s"%(_uuid) + extension
    fileurlpath = "static/upload/%s"%(nowtime)
    if not os.path.exists(fileurlpath):
        os.makedirs(fileurlpath)
    file_path = os.path.join(fileurlpath, filename)
    dst_img=file_path
    resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
    # file_storage.save(file_path)
    picurl = upload_pic(file_path)
    file_path2=picurl;
    return  file_path2

def upload_pic(path):
    storage = io.BytesIO()
    c = pycurl.Curl()
    values = [
        ("upload_file[]", (pycurl.FORM_FILE, path))
    ]
    c.setopt(c.URL, IMAGE1_UPLOAD_PATH)
    c.setopt(c.WRITEFUNCTION, storage.write)
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.HTTPPOST, values)
    c.perform()
    c.close()
    content = storage.getvalue().decode('UTF-8')
    PIC_MD5 = content[67:99]
    pic_url = IMAGE1_BASEPATH + PIC_MD5
    return pic_url
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
