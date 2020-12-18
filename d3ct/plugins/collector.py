from d3ct.plugins.base import PluginBase
from d3ct.plugins.log_loggers import PLUGIN_LOG


class Tags(PluginBase):
    """
    d3ct.plugins.filter.Tags:prod_tags=tag1+tag2,loct_tags=aa+bb,func_tags=cc+dd,user_tags=rr+tt
    """
    def traverse(self, py_obj, ret_obj):
        PLUGIN_LOG.debug("collector.Tags.traverse()")
        if type(py_obj) is list:
            for obj in py_obj:
                self.traverse(obj, ret_obj)
        else:
            if 'tags' in py_obj:
                if type(py_obj['tags']) is str:
                    tags = set((py_obj['tags'],))  # noqa
                elif type(py_obj['tags']) is list:
                    tags = set(py_obj['tags'])
                else:
                    tags = set()
                for tag in tags:
                    if tag in ret_obj:
                        ret_obj[tag] += 1
                    else:
                        ret_obj[tag] = 1

    def trans(self, py_obj):
        PLUGIN_LOG.debug("collector.Tags.trans()")
        PLUGIN_LOG.debug("    call params: %s", str(self.call_params))
        ret_obj = {}
        self.traverse(py_obj, ret_obj)
        return ret_obj
