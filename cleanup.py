#!-*- coding:utf8 -*-
from src.tools.cleanup.deleteAccountwithFloatIp import DeleteAccounts
from src.tools.cleanup.deleteAllComputes import DeleteAllComputes
from src.tools.cleanup.deleteAllNets import DeleteAllNets
from src.tools.cleanup.deleteAllObjectstores import DeleteAllObjectStores
from src.tools.cleanup.deleteAllRouters import DeleteAllRoutes
from src.tools.cleanup.deleteAllVolumes import DeleteAllVolumes
from src.readConfig import ReadConfig

if __name__=='__main__':
    readConfig=ReadConfig()
    deleteallcomputes = DeleteAllComputes(readConfig.base.admin_os_tenant_name,readConfig.base.admin_os_project_name,readConfig.base.admin_os_username,readConfig.base.admin_os_password)
    deleteallcomputes.deleteComputes() #删除云主机
    deleteallvolumes = DeleteAllVolumes(readConfig.base.admin_os_tenant_name,readConfig.base.admin_os_project_name,readConfig.base.admin_os_username,readConfig.base.admin_os_password)
    deleteallvolumes.deleteVolumes() #删除云硬盘
    deleteallobjectstores = DeleteAllObjectStores()
    deleteallobjectstores.deletebuckets() #删除桶
    deleteallroutes = DeleteAllRoutes(readConfig.base.admin_os_tenant_name,readConfig.base.admin_os_project_name,readConfig.base.admin_os_username,readConfig.base.admin_os_password)
    deleteallroutes.deleteRouters()  #删除路由器
    deleteallnets = DeleteAllNets(readConfig.base.admin_os_tenant_name,readConfig.base.admin_os_project_name,readConfig.base.admin_os_username,readConfig.base.admin_os_password)
    deleteallnets.deleteNet() #删除网络
    deleteallaccounts = DeleteAccounts()
    deleteallaccounts.deleteAccountwithFloatingips() #删除账户及名下的浮动ip
