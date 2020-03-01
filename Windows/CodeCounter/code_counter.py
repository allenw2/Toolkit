# -*-coding=utf-8-*-
import os
import re
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory


from Toolkit.Windows.CodeCounter.tk_calendar import Calendar
from Toolkit.Windows.CodeCounter.get_path import CMD_PATH, BIN_PATH

SPECIAL_CHAR = r'[^a-zA-z0-9,\w]'


window = tk.Tk()
window.title('Code Counter V1.0')
width, height = 500, 500
x, y = (window.winfo_screenwidth() - width) / 2, (window.winfo_screenheight() - height) / 2
window.geometry('%dx%d+%d+%d' % (width, height, x, y))

path = tk.StringVar()
name = tk.StringVar()
date_begin = tk.StringVar()
date_end = tk.StringVar()


def select_path():
    """select a path"""
    path.set(askdirectory())


def get_begin():
    """select a begin date"""
    for date in [Calendar((x, y), 'll').selection()]:
        if date:
            date_begin.set(date)


def get_end():
    """select a end date"""
    for date in [Calendar((x, y), 'll').selection()]:
        if date:
            date_end.set(date)


def generate_result():
    """main function"""
    # get params
    result_window.delete('1.0', 'end')
    try:
        git_path = path.get()
        names = name.get()
        start = date_begin.get()
        over = date_end.get()

        # set windows environment temporarily
        if not (CMD_PATH and BIN_PATH):
            messagebox.showerror(title='error',
                                 message='Could not find git in your computer, please install git first.')
            window.mainloop()
        os.environ['path'] = os.environ['path'] + ';' + CMD_PATH + ';' + BIN_PATH

        # check git path
        if not git_path:
            messagebox.showerror(title='Error', message='Please select your local git project path.')
            window.mainloop()
        os.chdir(git_path)

        # check date
        if not (start and over):
            messagebox.showerror(title='Error', message='Please select date begin and end.')
            window.mainloop()

        # check names
        if not names:
            messagebox.showerror(title='Error', message='Please input author names.')
            window.mainloop()
        special_character = re.findall(SPECIAL_CHAR, names)
        if special_character:
            messagebox.showerror(title='Error',
                                 message="Invalid character: {}. "
                                         "\nNames must be full chinese pinyin joined by ','".format(special_character))
            window.mainloop()

        # init git statement
        auth_statement = "git log --author={} "
        date_statement = "--since=={} --until=={} ".format(start, over)
        comm_statement = "--pretty=tformat: --numstat | awk \'{ add += $1; subs += $2; loc += $1 - $2 } " \
                         "END { printf \"added lines: %s, removed lines: %s, total lines: %s\", add, subs, loc }\' -"

        # get result
        name_list = [item.split() for item in names.split(',')]
        auth_list = os.popen("git log --encoding=gbk --format='%aN' | awk '{ printf $0}'").read().split("'")
        auth_valid = list((set([auth for auth in auth_list if auth is not ''])))

        result_dict = dict()
        for human in name_list:
            if human[0] not in auth_valid:
                messagebox.showerror(title='Error', message='Invalid author name: {}\n'
                                                            'Valid names will show in result area.'.format(human[0]))
                result_window.insert('insert', 'Choose author from: {}'.format(','.join(auth_valid)))
                window.mainloop()
            git_statement = auth_statement.format(human[0]) + date_statement + comm_statement

            result = os.popen(git_statement).read()
            result_dict[human[0]] = result
        result_str = ''
        for item in result_dict:
            result_str += item + ":" + result_dict[item] + '\n'
        result_window.insert('insert', result_str)
    except (IndexError, WindowsError, Exception):
        # window.destroy()
        pass


# Path
# tk.Label(window, text='Git Path:', font=('Arial', 12)).place(x=50, y=30)
tk.Button(window, text='Git Project', font=('Arial', 12), width=10, command=select_path).place(x=40, y=30)
tk.Entry(window, textvariable=path, font=('Arial', 10), width=30, state='readonly').place(x=150, y=35)

# Date
# tk.Label(window, text='Date begin:', font=('Arial', 12)).place(x=50, y=70)
# tk.Label(window, text='Date end:', font=('Arial', 12)).place(x=50, y=120)

tk.Button(window, text='Date Begin', font=('Arial', 12), width=10, command=get_begin).place(x=40, y=80)
tk.Button(window, text='Date End  ', font=('Arial', 12), width=10, command=get_end).place(x=40, y=130)

tk.Entry(window, textvariable=date_begin, font=('Arial', 10), width=30, state='readonly').place(x=150, y=85)
tk.Entry(window, textvariable=date_end, font=('Arial', 10), width=30, state='readonly').place(x=150, y=135)

# Name
tk.Label(window, text='Names:', font=('Arial', 12)).place(x=40, y=200)
tk.Entry(window, textvariable=name, font=('Arial', 10), width=30).place(x=150, y=200)

# Generate
tk.Button(window, text='Generate', font=('Arial', 12), width=10, height=1, command=generate_result).place(x=200, y=400)

# result window
tk.Label(window, text='Result: ', font=('Arial', 12)).place(x=40, y=250)
result_window = tk.Text(window, height=5, width=65)
result_window.pack()
result_window.place(x=20, y=300)

# Run
window.mainloop()
