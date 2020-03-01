import sqlite3

conn = sqlite3.connect('whl.db')
curs = conn.cursor()

curs.execute('drop table if exists name')
curs.execute('drop table if exists whl')
curs.execute('drop table if exists age')
curs.execute('drop table if exists height')
curs.execute('drop table if exists single')

curs.execute('create table name(name CHAR)')
curs.execute('create table whl(test CHAR)')
curs.execute('create table age(age INT)')
curs.execute('create table height(height REAL)')
curs.execute('create table single(isornot BOOL)')

for i in range(1000):
    curs.execute('insert into name values (?)', ('Allen {}'.format(str(i)), ))
    curs.execute('insert into whl values (?)', ('whl {}'.format(str(i)),))
    curs.execute('insert into single values (?)', (False if i == 999 else True,))


for i in range(3000):
    curs.execute('insert into age values (?)', (25 + i, ))

for i in range(5000):
    curs.execute('insert into height values (?)', ('175 {}'.format(str(i)), ))

conn.commit()
