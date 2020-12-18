import yaml

from d3ct.plugins.base import PluginBase


class Generator(PluginBase):

    @staticmethod
    def output(py_obj):
        print(yaml.dump(py_obj.data))
