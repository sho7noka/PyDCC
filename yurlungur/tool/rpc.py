# coding: utf-8
import sys
import threading
import types

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
    if env.Houdini() or env.Unity():
        import rpyc
        connection = rpyc.classic.connect(server, port)
        remote_module = connection.modules[name]
        return remote_module

    proxy = _xmlrpc_client.ServerProxy('http://%s:%d' % (server, port))
    # with open("fetched_python_logo.jpg", "wb") as handle:
    #     handle.write(proxy.python_logo().data)
    return proxy


@trace
def listen(port=18811, server="127.0.0.1", use_thread=True, quiet=True):
    """
    register_function は　オブジェクトを解釈しないので全入力が必要

    rpc listen for server
    Args:
        port:
        use_thread:
        quiet:

    Returns:

    """
    if env.Houdini() or env.Unity():
        import rpyc.servers.classic_server

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

        options, args = rpyc.servers.classic_server.parser.parse_args(args)
        options.registrar = None
        options.authenticator = None
        rpyc.servers.classic_server.serve_threaded(options)
        return

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


def _bin():
    with open("python_logo.jpg", "rb") as handle:
        return _xmlrpc_client.Binary(handle.read())
