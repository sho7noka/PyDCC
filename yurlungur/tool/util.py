# -*- coding: utf-8 -*-
import sys
import os
import traceback
import functools
import time
import inspect
import re
import sqlite3
import keyword
import yurlungur


def log(obj):
    return yurlungur.logger.info(obj)


def cache(func, *args, **kwargs):
    saved = {}

    @functools.wraps(func)
    def Wrapper(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result

    return Wrapper if sys.version_info < (3, 2) else functools.lcu_cache(*args, **kwargs)


def trace(func):
    @functools.wraps(func)
    def Wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            yurlungur.logger.warn(traceback.format_exc())

    return Wrapper


def timer(func):
    @functools.wraps(func)
    def Wrapper(*args, **kwargs):
        yurlungur.logger.info(
            '{0} start'.format(func.__name__)
        )
        start_time = time.clock()
        ret = func(*args, **kwargs)
        end_time = time.clock()
        yurlungur.logger.info(
            '\n{0}: {1:,f}s'.format("total: ", (end_time - start_time))
        )
        return ret

    return Wrapper


def __db_loader():
    from collections import namedtuple

    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    cache = os.path.join(local, "user", "cache.db").replace(os.sep, "/")

    conn = sqlite3.connect(cache)
    c = conn.cursor()
    for row in c.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)

    return namedtuple


def __db_attr():
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    cache = os.path.join(local, "user", "cache.db").replace(os.sep, "/")

    conn = sqlite3.connect(cache)
    c = conn.cursor()
    c.execute('''CREATE TABLE stocks
                 (date text, trans text, symbol text, qty real, price real)'''
              )
    c.execute(
        "INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
    )
    conn.commit()
    conn.close()


def __import__(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass

    try:
        import imp
    except:
        from importlib import import_module
        return import_module(name)

    fp, pathname, description = imp.find_module(name)
    try:
        return imp.load_module(name, fp, pathname, description)
    finally:
        if fp:
            fp.close()


def __make_completer(mod):
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    completer = os.path.join(local, "user", "completer.pyi").replace(os.sep, "/")

    header = "\"\"\"this document generated by internal module.\"\"\"\n\n\n"
    module = __import__(mod)
    with open(completer, "w") as f:
        f.write(header)

        for fn, _ in inspect.getmembers(module):
            if fn.startswith("_"):
                continue

            f.write("def {0}(*args, **kwargsargs):\n".format(fn))
            f.write("   \"\"\"{0}\"\"\"\n".format(inspect.getdoc(fn)))
            f.write("   pass\n\n")

    # return inspect.getmembers(__import__(completer))
