#!/Users/whl/.virtualenvs/test/bin/python
# -*- coding: utf-8 -*-
import termcolor


ERROR = 1
SUCCESS = 0


def colored_msg(msg, color):
    """
    对信息添加颜色
    add colour for message
    """
    return termcolor.colored(msg, color=color)


def colored_print_msg(msg, color='red'):
    """
    打印自定义颜色的信息
    print colored message
    """
    msg = termcolor.colored(msg, color=color)
    print msg + '\n'


def error_print(msg):
    """
    打印错误信息并退出程序
    print error message and exit process
    """
    colored_print_msg(str(msg))
    exit(1)