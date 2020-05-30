# -*- coding: utf-8 -*-
"""
Created on 06/09/2019

@author: Luis Solís

una interpolacion 2d con splines
"""

dir_out = r'C:\Users\solis\Documents\DEV\python3\ET\Hargreaves'

if __name__ == "__main__":

    try:
        from time import time
        import traceback
        from splines import func01
        import littleLogging as logging

        startTime = time()

        func01(dir_out)

        xtime = time() - startTime
        print(f'El script tardó {xtime:0.1f} s')

    except ValueError:
        msg = traceback.format_exc()
        logging.append(f'ValueError exception\n{msg}')
    except ImportError:
        msg = traceback.format_exc()
        print (f'ImportError exception\n{msg}')
    except Exception:
        msg = traceback.format_exc()
        logging.append(f'Exception\n{msg}')
    finally:
        logging.dump()
        print('se ha creado el fichero app.log')
