import re

from pyVmomi import vim
from SDA.SDA.api import service_instance,pchelper


def portgroup(host,user,password,port,dvs,pgkey):
    pg_dict = []
    si = service_instance.connect(host,user,password,port)
    content = si.RetrieveContent()
    portgroup_n = pchelper.get_all_obj(content,[vim.Network])

    for x in portgroup_n:
        if re.search(f'vim.dvs.DistributedVirtualPortgroup:DVPG-{dvs}-{pgkey}',str(x)) or re.search(f'vim.dvs.DistributedVirtualPortgroup:{pgkey}',str(x)):
            pg_dict = (portgroup_n[x])
    return pg_dict
