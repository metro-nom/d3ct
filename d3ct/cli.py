#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for d3ct."""
import inspect
import json
import os
import sys
import urllib.parse

import click
import yaml

from _version import get_versions
from d3ct.plugins.log_loggers import PLUGIN_LOG
from d3ct.plugins.log_utils import add_loggers
from d3ct.utils.utils import locate


def compute_plugin(data_inp, data_out, first_plugin, last_plugin, plugin, plugin_obj, plugin_params, runtime_infos):
    if inspect.isclass(plugin_obj):
        data_out = compute_class(data_inp, data_out, plugin_obj, plugin_params, runtime_infos)
    elif inspect.isfunction(plugin_obj):
        data_out = plugin_obj(data_inp, plugin_params, runtime_infos)
    elif type(plugin_obj) is dict:
        data_out = plugin_obj
        PLUGIN_LOG.debug('first data_out: {}'.format(data_out))
    if plugin_obj is None:
        data_out = compute_files(data_out, first_plugin, last_plugin, plugin)
    return data_out


def compute_files(data_out, first_plugin, last_plugin, plugin):
    if first_plugin and os.path.isfile(plugin):
        f = open(plugin, "r")
        plugin_raw = f.read()
        if plugin[-5:] == '.json':
            data_out = json.loads(plugin_raw)
        if plugin[-5:] == '.yaml':
            data_out = yaml.load(plugin_raw)
        PLUGIN_LOG.debug('first data_out: {}'.format(data_out))
    elif last_plugin:
        PLUGIN_LOG.debug('last data_out: {}'.format(data_out))
        f = open(plugin, "w")
        if plugin[-5:] == '.json':
            json.dump(data_out, f,
                      indent=4,
                      sort_keys=True)
        if plugin[-5:] == '.yaml':
            yaml.dump_all(data_out, f,
                          indent=4,
                          default_flow_style=False)
        f.close()
    else:
        PLUGIN_LOG.error("plugin or file '{}' not correct".format(plugin))
    return data_out


def compute_class(data_inp, data_out, plugin_obj, plugin_params, runtime_infos):
    converter = plugin_obj(plugin_params, runtime_infos)
    PLUGIN_LOG.debug('new plugin: {}'.format(converter))
    data_out = converter.trans(data_inp)
    return data_out


def get_plugin_params(plugin, plugin_parsed):
    plugin_params = {}
    try:
        if len(plugin_parsed) > 1:
            params_list = plugin_parsed[1].split(',')
            for param_string in params_list:
                p_key, p_value = param_string.split('=')
                plugin_params[p_key] = urllib.parse.unquote(p_value)
    except ValueError:
        PLUGIN_LOG.error("plugin param should be in form of:  plugin:key1=value1,key2=value2")
        PLUGIN_LOG.error("your plugin param: '%s'", plugin)
        exit(1)
    PLUGIN_LOG.debug("your plugin params: '%s'", plugin_params)
    return plugin_params


@click.command()
@click.version_option(version=get_versions()['version'])
@click.argument('plugins', nargs=-1)
@click.option('--dm', default=0, count=True,
              help='Show model debug information (maybe multiple).')
@click.option('--dp', default=0, count=True,
              help='Show plugins debug information (maybe multiple).')
@click.option('--de', default=0, count=True,
              help='Show event debug information (maybe multiple).')
@click.option('--ds', default=0, count=True,
              help='Show simulation debug information (maybe multiple).')
def main(plugins, dm, dp, de, ds):
    add_loggers(dm, dp, de, ds)
    if len(plugins) < 2:
        PLUGIN_LOG.error("less than 2 plugins")
        exit(1)
    runtime_infos = {}
    data_out = None
    for plugin in plugins:
        PLUGIN_LOG.debug("Plugin: '{}'".format(plugin))
        data_inp = data_out
        first_plugin = plugins.index(plugin) == 0
        last_plugin = plugins.index(plugin) + 1 == len(plugins)
        # cast :
        plugin = plugin.replace('\\:', '##&&##')
        plugin_parsed = plugin.split(':')
        # cast back:
        plugin_parsed = [i.replace('##&&##', ':') for i in plugin_parsed]
        plugin_name = plugin_parsed[0]
        PLUGIN_LOG.info("PLUGIN '{}'".format(plugin_name))
        plugin_params = get_plugin_params(plugin, plugin_parsed)
        plugin_obj = locate(plugin_name)
        if plugin_obj is None:
            PLUGIN_LOG.error("PLUGIN '{}' not found".format(plugin_name))
            exit(1)
        data_out = compute_plugin(data_inp, data_out, first_plugin, last_plugin, plugin, plugin_obj, plugin_params,
                                  runtime_infos)
        PLUGIN_LOG.debug("f:{} l:{} plugin_obj: {} / '{}'".format(
            first_plugin,
            last_plugin,
            type(plugin_obj),
            plugin
        ))
    PLUGIN_LOG.info("Program exit")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
