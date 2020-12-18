import uuid

from d3ct.plugins.base import PluginBase


class Converter(PluginBase):

    def __init__(self, call_params, runtime_infos):
        PluginBase.__init__(self, call_params, runtime_infos)
        self._data = None

    def trans(self, py_obj):
        self._data = py_obj
        ret_data = []
        for i in self._data:
            i['uuid'] = str(uuid.uuid4())
            ret_data.append(i)

        return ret_data
