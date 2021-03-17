#!/Users/whl/.virtualenvs/test/bin/python
import os
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
DEFAULT_PASSWORD_CTRL = 'letsg0'
DEFAULT_PASSWORD_MGR = 'cljslrl0620'
PASS_OPTION = ['Are you sure you want to continue connecting',
               'password: ',
               'already exist on the remote system']
DONE_OPTION = ['you wanted were added.',
               'Permission denied, please try again.']


class SSHAdd:
    def __init__(self, user, ip, password, alias):
        self.user = user
        self.ip = ip
        self.password = password
        self.alias = alias

    def check_config(self):
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

    def add_local_conf(self):
        with open(TEMPLATE, 'r') as template:
            temp = template.read()
        alias = temp.format(alias=self.alias, ip=self.ip, user=self.user)
        with open(CONFIG, 'r') as conf:
            exist_alias = conf.read()
        with open(CONFIG, 'a+') as conf:
            if alias not in exist_alias:
                conf.write(alias)

    def run(self):
        self.add_local_conf()
        self.copy_id()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', '-u',
                        dest='user',
                        default=DEFAULT_USER,
                        type=str,
                        help='SSH login user')

    parser.add_argument('--ip', '-i',
                        dest='ip',
                        type=str,
                        help='SSH login ip')

    parser.add_argument('--password', '-p',
                        dest='password',
                        default=DEFAULT_PASSWORD_MGR,
                        type=str,
                        help='SSH login password')

    parser.add_argument('--alias', '-a',
                        dest='alias',
                        type=str,
                        help='SSH login alias')

    parser.add_argument('--type', '-t',
                        dest='type',
                        default='mgr',
                        choices=['mgr', 'ctrl'],
                        type=str,
                        help='Node type, ctrl_node or mgr_node')

    option = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    user_ = option.user
    ip_ = option.ip
    password_ = option.password
    alias_ = option.alias
    type_ = option.type

    if not ip_:
        error_print('IP address must be configured!')

    if not alias_:
        alias_ = ip_.split('.')[-1]

    if type_ == 'ctrl':
        if not password_:
            password_ = DEFAULT_PASSWORD_CTRL

    s = SSHAdd(user_, ip_, password_, alias_)
    s.run()
