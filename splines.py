# -*- coding: utf-8 -*-
"""
Created on Sat May 30 20:01:59 2020

@author: solis
"""
import numpy as np


def func01(dir_out: str):
    from os.path import join
    import sqlite3
    DBNAME = 'r0.db'
    DROP_TABLE = "drop table if exists r0"
    CREATE_TABLE = """
    create table r0 (
    	lat integer,
        month, integer,
    	r0 real,
    	primary key (lat, month)
    	)
    """
    DELETE = "delete from r0"
    INSERT = """
    insert into r0 (lat, month, r0)
    values (?, ?, ?)
    """

    con = sqlite3.connect(join(dir_out, DBNAME))
    cur = con.cursor()
    cur.execute(DROP_TABLE)
    cur.execute(CREATE_TABLE)
    cur.execute(DELETE)
    con.commit()

    for m, xnew, ynew in splines1():
        for x1, y1 in zip(xnew, ynew):
            print(f'{x1} {m:n} {y1}')
            cur.execute(INSERT, (int(x1), m, float(y1)))

    con.commit()
    con.close()


def splines1():
    from scipy import interpolate

    for m, x, y in data1_get():
        tck = interpolate.splrep(x, y, s=0)
        xnew = [x[0]]
        for i in range(1, len(x)):
            xnew.append((x[i]+x[i-1])/2.)
        xnew.append(x[-1])
        xnew = np.array(xnew, np.float32)
        ynew = interpolate.splev(xnew, tck, der=0)
        yield m, xnew, ynew


def data1_get():
    from db_connection import con_get

    con = con_get('postgres', 'bda')
    cur = con.cursor()

    for i in range(1, 13):
        select1 = f'select lat x, r{i:02n} y from met.r0 order by lat'
        cur.execute(select1)
        row = [r for r in cur.fetchall()]
        x = np.array([r[0] for r in row], np.float32)
        y = np.array([r[1] for r in row], np.float32)
        yield i, x, y
    con.close()
