from functools import reduce

def getTree(values, res=None, temp=None, ids=None,result=None):
    if res==[]:
        return result
    ids = [i["id"] for i in values] if ids == None else ids
    if temp==None:
        res = [i for i in values if i["pid"] not in ids]
    else:
        _t = [i["id"] for i in values if i["pid"] in temp]
        _res=[i for i in values if i["pid"] in temp]
        for value in res:
            value["children"]=[_value for _value in _res if _value["pid"]==value["id"]]
        res=_res
    temp = [i["id"] for i in res]
    result = result or res
    return getTree(values,res,temp,ids,result)
