from pythonping import ping
import re

def ping_test(dest):
    a = ping(dest, count=5)
    b = re.findall(f'Reply from {dest}',str(a))
    if len(b) >= 3 :
        value = 'success'
    else:
        value = 'failure'
    return value
