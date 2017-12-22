import socket
import time,string,random

rule = string.ascii_letters + string.digits
str = random.sample(rule, 16)
print(str)
