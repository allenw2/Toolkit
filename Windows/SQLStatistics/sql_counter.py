# -*-coding=utf-8-*-
import os
import sqlite3
from time import strftime, localtime

import xlsxwriter
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from SQLStatistics.global_param import CHAR2NUM
from xlsxwriter.exceptions import FileCreateError


def select_path(path):
    """select a path"""
    path.set(askopenfilename())


def get_desktop_path():
    """get desktop path of user"""
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def data_init(path, window, check_var):
    """init data"""
    get_name = path.get().split('/')[-1]
    if not get_name.endswith('.db'):
        messagebox.showerror('Error', message='Please select db file')
        window.mainloop()
    if check_var.get():
        db_name = get_name[:-3] + strftime("%Y%m%d-%H%M%S", localtime())
    else:
        db_name = get_name.replace('.db', '')

    conn = sqlite3.connect(path.get())
    curs = conn.cursor()
    result = curs.execute('select name from sqlite_master where type="table"').fetchall()
    desktop = get_desktop_path()
    excel_name = os.path.join(desktop, db_name + '.xlsx')

    return excel_name, result, curs


def generate_pie(path, window, check_var):
    """generate pie chart"""
    try:
        excel_name, result, curs = data_init(path, window, check_var)
        # create excel file
        workbook = xlsxwriter.Workbook(excel_name)
        # create sheet
        worksheet = workbook.add_worksheet('Pie')
        worksheet.set_column('A:A', 15)

        # custom font style，bold
        bold = workbook.add_format({'bold': 1})

        # write data to excel
        headings = [item[0] for item in result]
        number = [curs.execute('select count(*) from {}'.format(table_name)).fetchone()[0] for table_name in headings]
        # write table head
        worksheet.write_row('A1', ['TableName'] + headings, bold)
        worksheet.write_row('A2', ['DataCount'], bold)
        # write table content
        worksheet.write_row('B2', number)

        # create pie chart
        chart_col = workbook.add_chart({'type': 'pie'})

        # set series
        chart_col.add_series({
            'name': 'Table Analysis',
            'categories': '=Pie!$B$1:${}$1'.format(CHAR2NUM[len(headings) + 1]),
            'values': '=Pie!$B$2:${}$2'.format(CHAR2NUM[len(headings) + 1]),
            'points': [
                {'fill': {'color': 'green'}},
                {'fill': {'color': 'red'}},
                {'fill': {'color': 'yellow'}},
            ],
        })

        # set title and x,y axis
        chart_col.set_title({'name': 'Table Analysis (Pie Chart)'})

        # set chart style
        chart_col.set_style(10)

        # insert chart to worksheet
        worksheet.insert_chart('B10', chart_col, {'x_offset': 25, 'y_offset': 0})
        workbook.close()
        messagebox.showinfo('Success',
                            message='Generate success! \nResult: {}'.format(excel_name))
    except FileCreateError:
        messagebox.showerror('Error', message='Please close current excel file and try again.')
        window.mainloop()


def generate_column(path, window, check_var):
    """generate column chart"""
    try:
        # init data
        excel_name, result, curs = data_init(path, window, check_var)

        # create excel file
        workbook = xlsxwriter.Workbook(excel_name)

        # create sheet
        worksheet = workbook.add_worksheet('Column')
        worksheet.set_column('A:A', 13)
        worksheet.set_column('B:B', 13)

        # custom font style, bold
        bold = workbook.add_format({'bold': 1})

        # write table head
        headings = ['TabelName', 'DataCount']
        worksheet.write_row('A1', headings, bold)

        # write data
        # worksheet.write_row('A2', number)
        table_list = [item[0] for item in result]
        data = [
            table_list,
            [curs.execute('select count(*) from {}'.format(table_name)).fetchone()[0] for table_name in table_list]
        ]
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])

        # create a column chart
        chart_col = workbook.add_chart({'type': 'column'})

        # set series 1
        chart_col.add_series({
            'name': '=Column!$B$1',
            'categories': '=Column!$A$2:$A${}'.format(len(table_list) + 1),
            'values': '=Column!$B$2:$B${}'.format(len(table_list) + 1),
            'line': {'color': 'red'},
        })

        # set title and x, y axis of chart
        chart_col.set_title({'name': 'Table Analysis (Column Chart)'})
        chart_col.set_x_axis({'name': 'Table Name'})
        chart_col.set_y_axis({'name': 'Data Count'})

        # set style of chart
        chart_col.set_style(1)

        # insert chart to worksheet
        worksheet.insert_chart('A10', chart_col, {'x_offset': 80, 'y_offset': 0})

        workbook.close()
        messagebox.showinfo('Success',
                            message='Generate success! \nResult: {}'.format(excel_name))
    except FileCreateError:
        messagebox.showerror('Error',
                             message='Please close current excel file and try again.')
        window.mainloop()


def generate_pie_column(path, window, check_var):
    """generate pie & column chart same time"""
    try:
        # init data
        excel_name, result, curs = data_init(path, window, check_var)

        # create excel file
        workbook = xlsxwriter.Workbook(excel_name)

        # ---------PIE---------
        # create Pie sheet
        worksheet = workbook.add_worksheet('Pie')
        worksheet.set_column('A:A', 15)

        # custom font style，bold
        bold = workbook.add_format({'bold': 1})

        # write data to excel
        headings = [item[0] for item in result]
        number = [curs.execute('select count(*) from {}'.format(table_name)).fetchone()[0] for table_name in headings]

        # write table head
        worksheet.write_row('A1', ['TableName'] + headings, bold)
        worksheet.write_row('A2', ['DataCount'], bold)

        # write table content
        worksheet.write_row('B2', number)

        # create pie chart
        chart_col = workbook.add_chart({'type': 'pie'})

        # set series
        chart_col.add_series({
            'name': 'Table Analysis',
            'categories': '=Pie!$B$1:${}$1'.format(CHAR2NUM[len(headings) + 1]),
            'values': '=Pie!$B$2:${}$2'.format(CHAR2NUM[len(headings) + 1]),
            'points': [
                {'fill': {'color': 'green'}},
                {'fill': {'color': 'red'}},
                {'fill': {'color': 'yellow'}},
            ],
        })

        # set title and x,y axis
        chart_col.set_title({'name': 'Table Analysis (Pie Chart)'})

        # set chart style
        chart_col.set_style(10)

        # insert chart to worksheet
        worksheet.insert_chart('B10', chart_col, {'x_offset': 25, 'y_offset': 0})

        # ---------Column---------
        # create Column sheet
        worksheet = workbook.add_worksheet('Column')
        worksheet.set_column('A:A', 13)
        worksheet.set_column('B:B', 13)

        # custom font style, bold
        bold = workbook.add_format({'bold': 1})

        # write table head
        headings = ['TabelName', 'DataCount']
        worksheet.write_row('A1', headings, bold)

        # write data
        # worksheet.write_row('A2', number)
        table_list = [item[0] for item in result]
        data = [
            table_list,
            [curs.execute('select count(*) from {}'.format(table_name)).fetchone()[0] for table_name in table_list]
        ]
        worksheet.write_column('A2', data[0])
        worksheet.write_column('B2', data[1])

        # create a column chart
        chart_col = workbook.add_chart({'type': 'column'})

        # set series 1
        chart_col.add_series({
            'name': '=Column!$B$1',
            'categories': '=Column!$A$2:$A${}'.format(len(table_list) + 1),
            'values': '=Column!$B$2:$B${}'.format(len(table_list) + 1),
            'line': {'color': 'red'},
        })

        # set title and x, y axis of chart
        chart_col.set_title({'name': 'Table Analysis (Column Chart)'})
        chart_col.set_x_axis({'name': 'Table Name'})
        chart_col.set_y_axis({'name': 'Data Count'})

        # set style of chart
        chart_col.set_style(1)

        # insert chart to worksheet
        worksheet.insert_chart('A10', chart_col, {'x_offset': 80, 'y_offset': 0})

        workbook.close()
        messagebox.showinfo('Success',
                            message='Generate success! \nResult: {}'.format(excel_name))
    except FileCreateError:
        messagebox.showerror('Error',
                             message='Please close current excel file and try again.')
        window.mainloop()


def main():
    """main function"""
    # init window
    window = tk.Tk()
    window.title('SQLite table analysis V1.0')

    # set window width and height
    width, height = 500, 500
    x, y = (window.winfo_screenwidth() - width) / 2, (window.winfo_screenheight() - height) / 2
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # init variable
    path = tk.StringVar()
    check_var = tk.IntVar()

    # init button
    tk.Button(window,
              text='Database',
              font=('Arial', 12),
              width=10,
              command=lambda: select_path(path)).place(x=40, y=30)

    tk.Entry(window,
             textvariable=path,
             font=('Arial', 10),
             width=30,
             state='readonly').place(x=150, y=35)

    tk.Button(window,
              text='Generate Pie Chart',
              font=('Arial', 12),
              width=24,
              height=1,
              command=lambda: generate_pie(path, window, check_var)).place(x=140, y=200)

    tk.Button(window,
              text='Generate Column Chart',
              font=('Arial', 12),
              width=24,
              height=1,
              command=lambda: generate_column(path, window, check_var)).place(x=140, y=270)

    tk.Button(window,
              text='Generate Pie&Column Chart',
              font=('Arial', 12),
              width=24,
              height=1,
              command=lambda: generate_pie_column(path, window, check_var)).place(x=140, y=340)

    tk.Checkbutton(window,
                   text='Keep old result',
                   variable=check_var,
                   onvalue=1,
                   offvalue=0).place(x=40, y=100)
    window.mainloop()


if __name__ == '__main__':
    main()
