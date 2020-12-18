from d3ct.plugins.log_loggers import PLUGIN_LOG


class PluginBase:
    def __init__(self, call_params, runtime_infos):
        PLUGIN_LOG.debug("PluginBase '%s'", str(self))
        PLUGIN_LOG.debug("    call_params: '%s'", str(call_params))
        PLUGIN_LOG.debug("    runtime_infos: '%s'", str(runtime_infos))
        self.call_params = call_params
        self.runtime_infos = runtime_infos

    def get_tags(self):
        if 'tags' in self.runtime_infos:
            return self.runtime_infos['tags']

    tags = property(get_tags)
