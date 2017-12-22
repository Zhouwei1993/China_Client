#-*- coding: utf-8 -*-
from suds.client import Client
from suds.wsse import *
url="http://180.169.77.21:17070/mws/services/ShippingTracerRecordService?wsdl"
client=Client(url)

security = Security()
token = UsernameToken('test', '12345678')
security.tokens.append(token)
client.set_options(wsse=security)

payload = {'unid':'tttttlililililili','width':'100'}
aa=client.service.insertRecord(unid='tttttlililililili',width='100')
# aa=client.service.insertRecord(unid='unid123456',width=100)
print(aa)
