import builtins
import sys
import uuid
from datetime import datetime


class ErrorDuringImport(Exception):
    """Errors that occurred while trying to import something to document it."""

    def __init__(self, filename, exc_info):
        self.filename = filename
        self.exc, self.value, self.tb = exc_info

    def __str__(self):
        exc = self.exc.__name__
        return 'problem in %s - %s: %s' % (self.filename, exc, self.value)


# noinspection PyDefaultArgument,PyBroadException
def safeimport(path, forceload=0, cache={}):
    """Import a module; handle errors; return None if the module isn't found.

    If the module *is* found but an exception occurs, it's wrapped in an
    ErrorDuringImport exception and reraised.  Unlike __import__, if a
    package path is specified, the module at the end of the path is returned,
    not the package at the beginning.  If the optional 'forceload' argument
    is 1, we reload the module from disk (unless it's a dynamic extension)."""
    # noinspection PyPep8
    try:
        # If forceload is 1 and the module has been previously loaded from
        # disk, we always have to reload the module.  Checking the file's
        # mtime isn't good enough (e.g. the module could contain a class
        # that inherits from another module that has changed).
        if forceload and path in sys.modules:
            if path not in sys.builtin_module_names:
                # Remove the module from sys.modules and re-import to try
                # and avoid problems with partially loaded modules.
                # Also remove any submodules because they won't appear
                # in the newly loaded module's namespace if they're already
                # in sys.modules.
                subs = [m for m in sys.modules if m.startswith(path + '.')]
                for key in [path] + subs:
                    # Prevent garbage collection.
                    cache[key] = sys.modules[key]
                    del sys.modules[key]
        module = __import__(path)
    except:  # noqa
        # Did the error occur before or after the module was found?
        (exc, value, tb) = info = sys.exc_info()
        if path in sys.modules:
            # An error occurred while executing the imported module.
            raise ErrorDuringImport(sys.modules[path].__file__, info)
        elif exc is SyntaxError:
            # A SyntaxError occurred before we could execute the module.
            raise ErrorDuringImport(value.filename, info)
        elif issubclass(exc, ImportError) and value.name == path:
            # No such module in the path.
            return None
        else:
            # Some other error occurred during the importing process.
            raise ErrorDuringImport(path, sys.exc_info())
    for part in path.split('.')[1:]:
        try:
            module = getattr(module, part)
        except AttributeError:
            return None
    return module


def locate(path, forceload=0):
    """Locate an object by name or dotted path, importing as necessary."""
    parts = [part for part in path.split('.') if part]
    module, n = None, 0
    while n < len(parts):
        nextmodule = safeimport('.'.join(parts[:n + 1]), forceload)
        if nextmodule:
            module, n = nextmodule, n + 1
        else:
            break
    if module:
        l_object = module
    else:
        l_object = builtins
    for part in parts[n:]:
        try:
            l_object = getattr(l_object, part)
        except AttributeError:
            return None
    return l_object


def uuid_4_plantuml(arg_uuid):
    return str(arg_uuid).replace('-', '')[:8]


def new_uuid5(arg_namespace, shorter=True):
    new_uuid = uuid.uuid5(uuid.NAMESPACE_URL,
                          arg_namespace)
    if shorter is True:
        return uuid_display_short(new_uuid)
    else:
        return new_uuid


def uuid_display_short(arg_uuid):
    return str(arg_uuid).split("-")[0]  # + "..."


def normalize_aspects(inp_aspects, my_logger):
    aspects = set()
    for i_asp in inp_aspects:
        if i_asp in ['location', 'product', 'function', 'user']:
            aspects.add(i_asp)
    if not (0 < len(aspects) < 5):
        my_logger.error("count of aspects must be 1-4 from 'location', 'product', 'function' or 'user'")
        exit(1)
    my_logger.debug('normalized aspects are: {}'.format(aspects))
    return aspects


def iso_ts_2int(dt_string):
    return int(datetime.strptime(dt_string,
                                 "%Y-%m-%dT%H:%M:%S"))
