from d3ct.plugins.base import PluginBase
from d3ct.plugins.log_loggers import PLUGIN_LOG


class Runtime(PluginBase):

    def __init__(self, call_params, runtime_infos):
        PluginBase.__init__(self, call_params, runtime_infos)
        for param_k, param_v in call_params.items():
            if param_v.lower() == "true":
                runtime_infos[param_k] = True
            elif param_v.lower() == "false":
                runtime_infos[param_k] = False
            else:
                runtime_infos[param_k] = param_v

    def trans(self, py_obj):
        PLUGIN_LOG.debug("update.Runtime.trans()")
        PLUGIN_LOG.debug("   runtime_infos: '{}'".format(self.runtime_infos))
        return py_obj
