# coding: utf-8
import sys
import threading
import types
import socket

if sys.version_info.major >= 3:
    import xmlrpc.server as _xmlrpc_server
    import xmlrpc.client as _xmlrpc_client
else:
    import SimpleXMLRPCServer as _xmlrpc_server
    import xmlrpclib as _xmlrpc_client

from yurlungur.core.app import application
from yurlungur.core import env
from yurlungur.core.deco import trace


@trace
def session(port=18811, server="127.0.0.1", name="hou"):
    """
    rpc session for client

    Args:
        port:
        server:
        name:

    Returns:
        proxy
    """

    """    
    if env.Houdini():
        import hrpyc
        _, hou = hrpyc.import_remote_module()

    # https://qiita.com/tm8r/items/29d598231b793be6c6ea
    if env.Unity():
        import unity_python.client.unity_client as unity_client
        unity_client
    """

    if env.Houdini() or env.Unity():
        import rpyc
        connection = rpyc.classic.connect(server, port)
        proxy = connection.modules[name]
        return proxy
    else:
        proxy = _xmlrpc_client.ServerProxy('http://%s:%d' % (server, port))
        # with open("fetched_python_logo.jpg", "wb") as handle:
        #     handle.write(proxy.python_logo().data)
        return proxy


def _bin():
    with open("python_logo.jpg", "rb") as handle:
        return _xmlrpc_client.Binary(handle.read())


@trace
def listen(port=18811, server="127.0.0.1", use_thread=True, quiet=True):
    """
    rpc listen for server

    NOTE: register_function は　オブジェクトを解釈しないので全入力が必要
    Args:
        port:
        use_thread:
        quiet:

    Returns:

    """

    """
    if env.Maya():
        import maya.cmds as cmds
        import maya.app.general.CommandPort
        cmds.commandPort(n=':%d' % port , stp='python')

    if env.Houdini():
        import hou
        hou.hscript("openport -p %d" % port)
    """

    if env.Houdini() or env.Unity():

        # Note that quiet=False only applies when use_thread=False.
        if use_thread:
            thread = threading.Thread(
                target=lambda: listen(port, use_thread=False))
            thread.start()
            return thread

        args = []
        if quiet:
            args.append("-q")
        args.extend(("-p", str(port), "--dont-register"))

        import rpyc.servers.classic_server
        options, args = rpyc.servers.classic_server.parser.parse_args(args)
        options.registrar = None
        options.authenticator = None
        rpyc.servers.classic_server.serve_threaded(options)
    else:
        server = _xmlrpc_server.SimpleXMLRPCServer((server, port), allow_none=True, logRequests=False)
        print("Listening on port %s %d..." % (application.__name__, port))

        import yurlungur
        for i in dir(yurlungur):
            # Ignore internal stuff
            if i[0] == "_" or i == "Qt":
                continue

            o = getattr(yurlungur, i)
            if type(o) == types.FunctionType:
                server.register_function(o, "yurlungur.%s" % i)

            else:
                try:
                    for m in dir(o) or []:
                        if m[0] == "_":
                            continue

                        meth = getattr(o, m)
                        if (type(meth) not in (types.MethodType, types.FunctionType)):
                            continue

                        # if isinstance(meth, hou.EnumValue):
                        #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                        if (type(o) in (type, type) and type(meth) == types.MethodType):
                            server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                        else:
                            for m in dir(o):
                                meth = getattr(o, m)
                                if (type(meth) not in (types.MethodType, types.FunctionType)) or m == "_":
                                    continue

                                # if isinstance(meth, hou.EnumValue):
                                #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                                if (type(o) in (type, type) and type(meth) == types.MethodType):
                                    server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                                else:
                                    server.register_function(meth, "yurlungur.%s.%s" % (i, m))
                except TypeError:
                    pass

        server.register_function(server.shutdown, "close")
        server.register_introspection_functions()
        server.serve_forever()


@trace
def send_chr(msg, port=18811, server="127.0.0.1"):
    """
    send socket
    Args:
        msg:
        port:
        server:

    Returns:

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    s.send(msg + '\n')
    res = s.recv(1024)
    s.close()
    return res
