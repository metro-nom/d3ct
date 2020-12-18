#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
from testfixtures import log_capture

from d3ct import cli


def test_cli():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 1


def test_cli_help():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


@log_capture()
def test_cli_01(capture):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['d3ct.plugins.inp.Zero'])
    capture.check(
        ('plugin', 'ERROR', 'less than 2 plugins'),
    )


@log_capture()
def test_cli_02_class(capture):
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           ['d3ct.plugins.inp.Zero',
                            'd3ct.plugins.out.StdOut:pretty=True']
                           )
    capture.check()
    assert result.exit_code == 0
    assert result.output == '[]\n'


@log_capture()
def test_cli_02_function_01(capture):
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           ['d3ct.plugins.inp.empty_list',
                            'd3ct.plugins.out.StdOut:pretty=True']
                           )
    capture.check()
    assert result.exit_code == 0
    assert result.output == '[]\n'


@log_capture()
def test_cli_02_function_02(capture):
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           ['d3ct.plugins.inp.none',
                            'd3ct.plugins.out.StdOut:pretty=True']
                           )
    capture.check()
    assert result.exit_code == 0
    assert result.output == 'None\n'


@log_capture()
def test_cli_04(capture):
    """
    wrong paramater
    """
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           ['d3ct.plugins.inp.Zero',
                            'd3ct.plugins.out.StdOut:pretty+True']
                           )
    capture.check(('plugin',
                   'ERROR',
                   'plugin param should be in form of:  plugin:key1=value1,key2=value2'),
                  ('plugin',
                   'ERROR',
                   "your plugin param: 'd3ct.plugins.out.StdOut:pretty+True'"))
    assert result.exit_code == 1
    assert result.output == ''


@log_capture()
def test_cli_05(capture):
    """
    wrong paramater
    """
    runner = CliRunner()
    result = runner.invoke(cli.main,
                           ['d3ct.plugins.inp.Zero',
                            'd3ct.plugins.out.StdOut:pretty=True,']
                           )
    capture.check(('plugin',
                   'ERROR',
                   'plugin param should be in form of:  plugin:key1=value1,key2=value2'),
                  ('plugin',
                   'ERROR',
                   "your plugin param: 'd3ct.plugins.out.StdOut:pretty=True,'"))
    assert result.exit_code == 1
    assert result.output == ''
