import json

from d3ct.plugins.log_loggers import PLUGIN_LOG
from d3ct.plugins.base import PluginBase


class Converter(PluginBase):

    def __init__(self, call_params, runtime_infos):
        PluginBase.__init__(self, call_params, runtime_infos)
        self._data = None

        try:
            if 'inp' in self.call_params:
                f = open(self.call_params['inp'], "r")
                input_raw = f.read()
                self.inp_data = json.loads(input_raw)
            else:
                PLUGIN_LOG.error('no inp value found in: %s', self.call_params)
                exit(1)
        except FileNotFoundError as err:
            PLUGIN_LOG.error(err)
            exit(1)

    def traverse(self, py_obj):
        PLUGIN_LOG.debug("json_overlay.Converter.traverse()")
        if 'uuid' in py_obj:
            for obj in self.inp_data['objects']:
                if obj['uuid'] == py_obj['uuid']:
                    py_obj.update(obj)
        if 'children' in py_obj:
            for child in py_obj['children']:
                self.traverse(child)

    def trans(self, py_obj):
        PLUGIN_LOG.debug("json_overlay.Converter.trans()")
        PLUGIN_LOG.debug("    call params: %s", str(self.call_params))
        self.traverse(py_obj)
        self._data = py_obj
        return self._data
