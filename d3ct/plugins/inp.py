from d3ct.plugins.base import PluginBase
from d3ct.plugins.log_loggers import PLUGIN_LOG


def empty_list(data_inp, plugin_params, runtime_infos):  # noqa
    return []


def none(data_inp, plugin_params, runtime_infos):  # noqa
    return None


# noinspection PyUnusedLocal
class Zero(PluginBase):

    def trans(self, py_obj=None):
        PLUGIN_LOG.debug("Zero.trans()")
        PLUGIN_LOG.debug("    call params: %s", str(self.call_params))
        return []
