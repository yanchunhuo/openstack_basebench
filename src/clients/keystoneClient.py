#!-*- coding:utf8 -*-
from src.authTool import AuthTool
from src.common.strTool import StrTool
import subprocess

class KeystoneClient:
    def __init__(self):
        self._authTool = AuthTool()

    def createAccount(self, project_name, user_name, password, role_name='_member_'):
        """
        创建一个账户（创建项目、用户），并关联角色
        :param project_name:
        :param user_name:
        :param password:
        :param role_name: 角色，可选admin、TenantAdmin（二级账户）、_member_（三级账户），默认TenantAdmin
        :return: project_id, user_id
        """
        project_id = self._createProjectForAccount(project_name)
        user_id = self._createUserForAccount(user_name, password)
        command = "openstack role add " + "--user " + user_name + " --project " + project_name + " " + role_name
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        self._createUserForObjectStore(project_id, project_name)
        self._ActivateAccountQuota(project_id)
        return project_id, user_id

    def _createProjectForAccount(self, project_name):
        """
        创建项目
        :param project_name:
        :return: project_id
        """
        command = "openstack project create " + project_name + " -f json"
        command = self._authTool.insertAdminAuth(command)
        tmp_project_id = subprocess.check_output(command, shell=True)
        project_id = StrTool.getStringWithDic(tmp_project_id,"id")
        if not project_id:
            return None
        return project_id

    def getProjectId(self, project_name):
        """
        获取项目id
        :param project_name:
        :return: project_id
        """
        command = "openstack project list|grep -i " + project_name + "|awk '{print $2}'"
        command = self._authTool.insertAdminAuth(command)
        project_id = subprocess.check_output(command, shell=True)
        project_id = project_id.strip()
        if not project_id:
            return None
        return project_id


    def _createUserForAccount(self, user_name, password):
        """
        创建用户
        :param user_name:
        :param password:
        :return: user_id
        """
        command = "openstack user create " + user_name + " --password " + password + " -f json"
        command = self._authTool.insertAdminAuth(command)
        tmp_user_id = subprocess.check_output(command, shell=True)
        user_id = StrTool.getStringWithDic(tmp_user_id,"id")
        if not user_id:
            return None
        return user_id

    def getUserId(self, user_name):
        """
        获取用户id
        :param user_name:
        :return:
        """
        command = "openstack user list|grep -i " + user_name + "|awk '{print $2}'"
        command = self._authTool.insertAdminAuth(command)
        user_id = subprocess.check_output(command, shell=True)
        user_id = user_id.strip()
        if not user_id:
            return None
        return user_id

    @staticmethod
    def _createUserForObjectStore(project_id, project_name):
        """
        创建对象存储用户，并且生成keys
        :param project_id:
        :param project_name:
        :return:
        """
        command = "radosgw-admin user create --uid=" + project_id + " --display-name=" + project_name + " --gen-access-key --gen-secret"
        subprocess.check_output(command, shell=True)
        return True

    @staticmethod
    def _ActivateAccountQuota(project_id):
        """
        激活账户配额功能
        :param project_id:
        :return:
        """
        command = "radosgw-admin quota enable --quota-scope=user --uid=" + project_id
        subprocess.check_output(command, shell=True)
        return True

    @staticmethod
    def setObjectStoreQuota(objects_size, project_id):
        """
        更新账户对象存储大小
        :param objects_size: 文件总大小，单位字节，范围1-5497558138880
        :param project_id:
        :return:
        """
        command = "radosgw-admin quota set --quota-scope=user --max-size " + str(objects_size) + " --uid=" + project_id
        subprocess.check_output(command, shell=True)
        return True

    @staticmethod
    def setAccountBucketsQuota(bucket_size, project_id):
        """
        更新账户桶大小
        :param bucket_size: 桶大小，范围1-500
        :param project_id:
        :return:
        """
        command = "radosgw-admin user modify --max-buckets " + str(bucket_size) + " --uid=" + project_id
        subprocess.check_output(command, shell=True)
        return True

    def setInstanceStorageQuota(self, project_id, cores_size, instances_size, ram_size, volumes_size, snapshots_size, volumes_snapshots_size):
        """
        更新账户云主机\存储相关配额
        :param project_id:
        :param cores_size: 虚拟内核，范围1-65535
        :param instances_size: 云主机数，范围1-65535
        :param ram_size: 内存，范围1024-4194304
        :param volumes_size: 云硬盘，范围1-65535
        :param snapshots_size: 云硬盘快照，范围1-65535
        :param volumes_snapshots_size: 云硬盘和快照总大小，范围1-327675
        :return:
        """
        command = "openstack quota set " + project_id + " --cores " + str(cores_size) + " --instances " + str(instances_size) + " --ram " + str(ram_size) \
                  + " --volumes " + str(volumes_size) + " --snapshots " + str(snapshots_size) + " --gigabytes " + str(volumes_snapshots_size)
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def setAccountNetworkQuota(self, project_id, floatingip_size, loadbalancer_size, router_size, network_size, security_group_size):
        """
        更新账户网络相关配额
        :param project_id:
        :param floatingip_size: 浮动ip，范围1-65535
        :param loadbalancer_size: 负载均衡器，范围1-65535
        :param router_size: 路由器，范围1-65535
        :param network_size: 网络，范围1-65535
        :param security_group_size: 安全组，范围1-65535
        :return:
        """
        command = "openstack quota set " + "--floating-ips " + str(floatingip_size) + \
                  " --routers " + str(router_size) + " --networks  " + str(network_size) + " --secgroups " + str(security_group_size)+" "+project_id
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def setAccountImageQuota(self, snapshot_quota_size, image_quotas_size, project_id):
        """
        更新账户镜像相关配额
        :param snapshot_quota_size: 云主机快照，范围1-500
        :param image_quotas_size: 私有镜像,范围1-100
        :param project_id:
        :return:
        """
        command = "glance image-quota-set --snapshot_quota " + str(snapshot_quota_size) + " --image_quotas " + str(image_quotas_size) + " " + project_id
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def deleteAccount(self, user_id, project_id):
        """
        删除用户
        :param user_id:
        :param project_id:
        :return:
        """
        self._deleteUser(user_id)
        self._deleteProject(project_id)
        return True

    def _deleteUser(self, user_id):
        """
        删除用户
        :param user_id:
        :return
        """
        command = "openstack user delete " + user_id
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def _deleteProject(self, project_id):
        """
        删除项目
        :param project_id:
        :return:
        """
        command = "openstack project delete " + project_id
        command = self._authTool.insertAdminAuth(command)
        subprocess.check_output(command, shell=True)
        return True

    def delAccount(self,project_ids):
        """
        删除用户
        :param project_ids:
        :return:
        """
        if len(project_ids) != 0:
            for project_id in project_ids:
                command = "openstack role assignment list|grep -i " + project_id + "|awk -F '|' '{print $3}'"
                command = self._authTool.insertAdminAuth(command)
                tmp_user_ids = subprocess.check_output(command, shell=True)
                if tmp_user_ids:
                    user_ids = tmp_user_ids.split()
                    for user_id in user_ids:
                        self._deleteUser(user_id)
                self._deleteProject(project_id)
        return True