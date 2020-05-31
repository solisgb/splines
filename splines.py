# -*- coding: utf-8 -*-
"""
Created on Sat May 30 20:01:59 2020

@author: solis
"""
import numpy as np


def func01(dir_out: str, xyg: bool=1):
    """
    I select results in table r0 and then I execute
        update r0 set r0=0.0 where r0<0
        because some interpolated values are <0
    xy graphs have the original values but yo can not appreciate values < 0
        by eye
    """
    from os.path import join
    import sqlite3

    DBNAME = 'r0.db'
    DROP_TABLE = "drop table if exists r0"
    CREATE_TABLE = """
    create table r0 (
    	lat integer,
        month integer,
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

    for m, x, y in _splines1():
        print(m)
        for x1, y1 in zip(x, y):
            cur.execute(INSERT, (int(x1), m, float(y1)))
        if xyg:
            _xygraph(dir_out, cur, m)
    con.commit()
    con.close()


def _splines1():
    from scipy import interpolate

    for m, x, y in _data1_get():
        tck = interpolate.splrep(x, y, s=0)
        xnew = [(x[i]+x[i-1])/2. for i in range(1, len(x))]
        xnew = np.array(xnew, np.float32)
        ynew = interpolate.splev(xnew, tck, der=0).astype(np.float32)
        yield m, np.concatenate((x, xnew)), np.concatenate((y, ynew))


def _data1_get():
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


def _xygraph(dir_out: str, cur, m: int):
    """
    cur: sqlite cursor
    """
    import matplotlib.pyplot as plt
    from os.path import join

    select = f"""
    select lat, r0
    from r0
    where month={m:02n}
    order by lat
    """

    cur.execute(select)
    rs = np.array([r1 for r1 in cur.fetchall()])
    fig, ax = plt.subplots()
    ax.plot(rs[:,0], rs[:,1])
    ax.set(xlabel='lat', ylabel='r0 mm)',
          title=f'r0 Allen interpolated odd lats month {m:02n}')
    ax.grid()
    fig.savefig(join(dir_out,f'r0_month_{m:02n}.png'))
    plt.close(fig)

