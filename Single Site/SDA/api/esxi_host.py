
from SDA.SDA.api import service_instance
from pyVmomi import vmodl, vim

def esxi_host (host,user,password):
    si = service_instance.connect(host, user, password, '443')
    content = si.RetrieveContent()
    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()

    datastores = []
    for esxi_host in esxi_hosts:
        summary = esxi_host.summary
        stats = summary.quickStats
        hardware = esxi_host.hardware
        cores = (esxi_host.hardware.cpuInfo.numCpuCores)
        total_mem = (((esxi_host.hardware.memorySize / 1024) / 1024) / 1024)
        used_mem = stats.overallMemoryUsage / 1024
        avail_mem = (total_mem - used_mem)
    return [cores,avail_mem]
