import pprint

from d3ct.plugins.base import PluginBase


class Generator(PluginBase):

    @staticmethod
    def output(py_obj):
        pprint.pprint(py_obj.data)
