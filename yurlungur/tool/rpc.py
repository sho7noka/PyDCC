# coding: utf-8
import sys
import threading

if sys.version_info.major >= 3:
    import xmlrpc.server as _xmlrpc_server
    import xmlrpc.client as _xmlrpc_client
else:
    import SimpleXMLRPCServer as _xmlrpc_server
    import xmlrpclib as _xmlrpc_client

from yurlungur.core.app import application
from yurlungur.core import env


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

    # proxy = _xmlrpc_client.ServerProxy("http://localhost:8000/")
    # with open("fetched_python_logo.jpg", "wb") as handle:
    #     handle.write(proxy.python_logo().data)

    proxy = _xmlrpc_client.ServerProxy('http://127.0.0.1:%d' % port)
    return proxy


def listen(port=18811, server="127.0.0.1", use_thread=True, quiet=True):
    """
    rpc listen for server
    Args:
        port:
        use_thread:
        quiet:

    Returns:

    """
    if env.Houdini() or env.Unity():
        import hrpyc, houxmlrpc, bpy
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

    # if env.Maya():
    # import maya.cmds as cmds
    # cmds.commandPort(port)
    # runtime command
    # return

    client = _xmlrpc_server.SimpleXMLRPCServer((server, port), allow_none=True)
    print("Listening on port %s %d..." % (application.__name__, port))
    client.register_function(_mod, "yurlungur")
    client.register_function(_bin, 'python_logo')
    client.register_introspection_functions()
    client.serve_forever()


def _bin():
    with open("python_logo.jpg", "rb") as handle:
        return _xmlrpc_client.Binary(handle.read())
