# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

import paramiko
from stat import S_ISDIR
import os
import sys


class TransferApi(object):

    def __init__(self, source, s_port, s_code, l_code, username):
        # self.pkey = '~/.ssh/'
        self.remote_ip = source
        self.remote_port = s_port

        self.remote_username = username
        self.remote_password = ''

        self.remote_path = s_code
        self.local_path = l_code

    # ------获取远端linux主机上指定目录及其子目录下的所有文件------
    def __get_all_files_in_remote_dir(self, sftp, remote_dir):
        # 保存所有文件的列表
        all_files = list()

        # 去掉路径字符串最后的字符'/'，如果有的话
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取当前指定目录下的所有目录及文件，包含属性值
        files = sftp.listdir_attr(remote_dir)
        for x in files:
            # remote_dir目录中每一个文件或目录的完整路径
            filename = remote_dir + '/' + x.filename
            # 如果是目录，则递归处理该目录，这里用到了stat库中的S_ISDIR方法，与linux中的宏的名字完全一致
            if S_ISDIR(x.st_mode):
                all_files.extend(self.__get_all_files_in_remote_dir(sftp, filename))
            else:
                all_files.append(filename)
        return all_files

    def transfer(self):
        # 创建sftp对象
        remote_ip = self.remote_ip
        remote_port = self.remote_port
        remote_username = self.remote_username
        remote_password = self.remote_password
        remote_path = self.remote_path
        local_path = self.local_path

        # 创建SSH对象
        ssh = paramiko.SSHClient()

        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.load_host_keys()

        ssh.connect(hostname=remote_ip, port=remote_port, username=remote_username)

        #
        transport = ssh.get_transport()

        sftp = paramiko.SFTPClient.from_transport(transport)

        # 上传
        # sftp.put("test.py", "/home/svr/test.py")  # 将123.py 上传至服务器 /tmp下并改名为test.py

        # 获取远端linux主机上指定目录及其子目录下的所有文件
        all_files = self.__get_all_files_in_remote_dir(sftp, remote_path)
        # 依次get每一个文件
        for x in all_files:
            print(x)
            filename = x.split('/')[-1]
            local_filename = os.path.join(local_path, filename)
            sftp.get(x, local_filename)

        # 关闭sftp对象连接
        transport.close()

        return '传输完成'


class CommandApi(object):

    def __init__(self, source, s_port, username, password):
        self.remote_ips = source
        self.remote_port = s_port
        self.remote_username = username
        self.remote_password = password

    def command(self, shell_command):
        remote_ips = self.remote_ips
        remote_ips_list = remote_ips.split('\n')
        # print(remote_ips_list)

        remote_port = self.remote_port
        remote_username = self.remote_username
        remote_password = self.remote_password

        # 建立一个sshclient对象
        ssh = paramiko.SSHClient()
        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 调用connect方法连接服务器
        for remote_ip in remote_ips_list:
            ssh.connect(hostname=remote_ip, port=remote_port, username=remote_username, password=remote_password, timeout=10)
            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(shell_command)
            err_list = stderr.readlines()

            # 结果放到stdout中，如果有错误将放到stderr中
            # print(stdout.read().decode('utf-8'))
            exec_status = stdout.channel.recv_exit_status()
            # 关闭连接
            ssh.close()

            if exec_status != 0:
                print(err_list)
                print(exec_status)
                print(stdout.read().decode('utf-8'))

            else:
                print(exec_status)
                print(stdout.read().decode('utf-8'))








