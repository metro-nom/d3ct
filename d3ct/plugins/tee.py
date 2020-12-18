import pprint

from d3ct.plugins.base import PluginBase


class Converter(PluginBase):

    def __init__(self, call_params, runtime_infos):
        PluginBase.__init__(self, call_params, runtime_infos)
        self._data = None

    def trans(self, py_obj):
        self._data = py_obj
        pprint.pprint(self._data)
        return self._data
