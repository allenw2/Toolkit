#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import argparse
import pexpect
from time import sleep

from common import error_print
from common import colored_print_msg

PWD = os.path.realpath(os.path.dirname(__file__))
TEMPLATE = os.path.join(PWD, 'template')
CONFIG = os.path.expanduser('~/.ssh/config')
DEFAULT_USER = 'root'
DEFAULT_PASSWORD = 'cljslrl0620'
IP_REGEX = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
PASS_OPTION = ['Are you sure you want to continue connecting',
               'password: ',
               'already exist on the remote system']
DONE_OPTION = ['you wanted were added.',
               'Permission denied, please try again.']


def ip_verify(ip):
    """
    判断是否是一个有效的日期字符串
    check if given ip is a valid ip address
    """
    try:
        ip = re.search(IP_REGEX, ip).group()
        return ip
    except (Exception, ):
        error_print('[ERROR]Not a valid ip: {0}'.format(ip))


class SSHAdd:
    def __init__(self, user, ip, password, alias, delete_ip):
        self.user = user
        self.ip = ip
        self.password = password
        self.alias = alias
        self.delete = delete_ip

    @staticmethod
    def check_config():
        if not os.path.exists(CONFIG):
            os.mknod(CONFIG)

    def copy_id(self):
        cmd = '/usr/bin/ssh-copy-id {user}@{ip}'.format(user=self.user, ip=self.ip)
        child = pexpect.spawn(cmd)
        sleep(1.5)
        index_pass = child.expect(PASS_OPTION, timeout=5)
        if index_pass == 0:
            child.sendline('yes')
            index_pass = child.expect(PASS_OPTION, timeout=5)
        if index_pass == 1:
            child.sendline(self.password)
            sleep(1.5)
            index_done = child.expect(DONE_OPTION)
            if index_done == 0:
                colored_print_msg('Success!', color='green')
            elif index_done == 1:
                error_print('Wrong password!')
            else:
                error_print('Send password error')
        if index_pass == 2:
            colored_print_msg('Already has key, Success!', color='green')

    def handle_local_conf(self):
        ip = self.ip if self.ip else self.delete
        with open(TEMPLATE, 'r') as template:
            temp = template.read()
        alias = temp.format(alias=self.alias, ip=ip, user=self.user)
        with open(CONFIG, 'r') as conf:
            exist_alias = conf.read()
        if self.ip:
            # 添加对应的 alias
            with open(CONFIG, 'a+') as conf:
                if alias not in exist_alias:
                    conf.write(alias)
        else:
            # 删除对应的 alias
            with open(CONFIG, 'w') as conf:
                content = ''.join(exist_alias.split(alias))
                conf.write(content)

    def run(self):
        self.handle_local_conf()
        if self.ip:
            self.copy_id()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='add-ssh',
                                     usage='%(prog)s [options]',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--user', '-u',
                        dest='user',
                        default=DEFAULT_USER,
                        type=str,
                        help='SSH login user')

    parser.add_argument('--ip', '-i',
                        dest='ip',
                        type=ip_verify,
                        help='SSH login ip')

    parser.add_argument('--password', '-p',
                        dest='password',
                        default=DEFAULT_PASSWORD,
                        type=str,
                        help='SSH login password')

    parser.add_argument('--alias', '-a',
                        dest='alias',
                        type=str,
                        help='SSH login alias')

    parser.add_argument('--delete', '-d',
                        dest='delete',
                        type=ip_verify,
                        help='delete alias of given ip')

    option = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    user_ = option.user
    ip_ = option.ip
    password_ = option.password
    alias_ = option.alias
    delete_ip_ = option.delete

    if not (ip_ or delete_ip_):
        error_print('[ERROR]请指定 --ip 或者 --delete')

    if ip_ and delete_ip_:
        error_print('[ERROR]--ip 和 --delete 不能同时指定')

    addr = ip_ or delete_ip_
    if not alias_:
        # 自动生成别名：
        # 如果 ip 的倒数第二位是 100，则别名为倒数第一位，如 218
        # 如果 ip 的倒数第二位不是 100，则别名为倒数后两位，如 90.218
        if addr.split('.')[-2] == '100':
            alias_ = addr.split('.')[-1]
        else:
            alias_ = '.'.join(addr.split('.')[-2:])

    s = SSHAdd(user_, ip_, password_, alias_, delete_ip_)
    s.run()
