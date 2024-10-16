import json
from pyVmomi import vmodl, vim
from SDA.SDA.api import service_instance

def datastore(host,user,password):
    si = service_instance.connect(host, user, password, '443')
    content = si.RetrieveContent()
    objview = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.HostSystem],
                                                      True)
    esxi_hosts = objview.view
    objview.Destroy()

    datastores = []
    for esxi_host in esxi_hosts:

        # All Filesystems on ESXi host
        storage_system = esxi_host.configManager.storageSystem
        host_file_sys_vol_mount_info = \
            storage_system.fileSystemVolumeInfo.mountInfo

        datastore_dict = {}
        # Map all filesystems
        for host_mount_info in host_file_sys_vol_mount_info:
            # Extract only VMFS volumes
            if host_mount_info.volume.type == "VMFS":
                datastores.append(host_mount_info.volume.name)

    return datastores
