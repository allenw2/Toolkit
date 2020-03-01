import os
import string


def find_bash(target_path, key='git-bash.exe'):
    """
    :param target_path:
    :param key: target
    :return:
    """
    walk = os.walk(target_path)
    for super_dir, dir_names, file_names in walk:
        for file_name in file_names:
            if file_name == key:
                git_path = os.path.realpath(super_dir)
                cmd_path = os.path.join(git_path, 'cmd')
                bin_path = os.path.join(git_path, 'usr', 'bin')
                return cmd_path, bin_path
    return None, None


def find_git(target_path='D:', key='.git'):
    """
    :param target_path:
    :param key: target
    :return:
    """
    walk = os.walk(target_path)
    for super_dir, dir_names, file_names in walk:
        for dir_name in dir_names:
            if dir_name == key:
                git_path = os.path.realpath(super_dir)
                return git_path
    return None


def get_disk_list():
    """get windows disk names"""
    disk_list = []
    for c in string.ascii_uppercase:
        disk_name = c + ':\\'
        if os.path.isdir(disk_name):
            disk_list.append(disk_name)

    return disk_list


def get_paths():
    disks = get_disk_list()
    for disk in disks:
        cmd_path, bin_path = find_bash(target_path=disk)
        if cmd_path and bin_path:
            pass
            return cmd_path, bin_path
    return None, None


CMD_PATH, BIN_PATH = get_paths()
