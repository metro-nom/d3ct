import pprint
import sys

from d3ct.plugins.base import PluginBase
from d3ct.plugins.log_loggers import PLUGIN_LOG


class StdOut(PluginBase):
    def trans(self, outp):
        PLUGIN_LOG.debug("out.StdOut.trans()")
        if 'pretty' in self.call_params:
            pprint.pprint(outp, sys.stdout)
        else:
            print(outp, file=sys.stdout)
        return outp
