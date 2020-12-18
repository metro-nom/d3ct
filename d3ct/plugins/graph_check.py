import networkx as nx

from d3ct.plugins.base import PluginBase
from d3ct.plugins.log_loggers import PLUGIN_LOG


def if_empty(nx_graph):
    PLUGIN_LOG.debug("graph_check.if_empty()")
    if nx.is_empty(nx_graph):
        PLUGIN_LOG.error('graph is empty')
        exit(1)
    return nx_graph


def if_splitted(nx_graph):
    PLUGIN_LOG.debug("graph_check.if_splitted()")
    # other algo len(list(nx.weakly_connected_components(nx_graph))) > 1
    if not nx.is_weakly_connected(nx_graph):
        PLUGIN_LOG.error('split in graph')
        exit(1)
    return nx_graph


def if_connections_not_bidir(nx_graph):
    PLUGIN_LOG.debug("graph_check.if_connections_not_bi()")
    for node_id, node in nx_graph.nodes.items():
        __check_hasPart(nx_graph, node_id, node)
        __check_isPartOf(nx_graph, node_id, node)
        __check_containsProduct(nx_graph, node_id, node)
        __check_implementedBy(nx_graph, node_id, node)
        __check_usesFunction(nx_graph, node_id, node)
        __check_usedBy(nx_graph, node_id, node)
        __check_containedIn(nx_graph, node_id, node)
    return nx_graph


class AllTests(PluginBase):

    @staticmethod
    def trans(nx_graph):
        PLUGIN_LOG.debug("graph_check.AllTests.trans()")
        PLUGIN_LOG.info("   {}".format(nx.info(nx_graph).replace('\n', ' / ')))
        nx_graph = if_empty(nx_graph)
        nx_graph = if_splitted(nx_graph)
        nx_graph = if_connections_not_bidir(nx_graph)
        return nx_graph


def __check_hasPart(nx_graph, node_id, node):
    if 'hasPart' in node:
        hasPart = node['hasPart']
        if type(hasPart) is str:
            hasPart = [hasPart]
        for part_id in hasPart:
            if part_id not in nx_graph.node:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "obj '{}' is referenced by <hasPart> in '{}'  doesn't exists".format(part_id,
                                                                                         node['@id']))
                exit(1)
            part = nx_graph.node[part_id]
            if node_id not in part['isPartOf']:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "obj '{}' is referenced by <hasPart> in '{}' has no valid <isPartOf>".format(part['@id'],
                                                                                                 node['@id']))
                exit(1)


def __check_isPartOf(nx_graph, node_id, node):
    if 'isPartOf' in node:
        nodeisPartOf = node['isPartOf']
        if node_id not in nx_graph.nodes[nodeisPartOf]['hasPart']:
            PLUGIN_LOG.error('graph_check error: ')
            PLUGIN_LOG.error(
                "obj '{}' has <isPartOf> but no valid <hasPart> in '{}'".format(node['@id'],
                                                                                nodeisPartOf))
            exit(1)


def __check_containsProduct(nx_graph, node_id, node):
    if 'containsProduct' in node and len(node['containsProduct']) > 0:
        containsProducts = node['containsProduct']
        if type(containsProducts) is str:
            containsProducts = [containsProducts]
        for containsProductId in containsProducts:
            if containsProductId not in nx_graph.nodes:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "obj '{}' has <containsProduct> but '{}' doesn't exists".format(node['@id'],
                                                                                    containsProductId))
                exit(1)
            if containsProductId not in nx_graph.nodes:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "obj '{}' has <containsProduct> but '{}' doesn't exists".format(node['@id'],
                                                                                    containsProductId))
                exit(1)
            containsProduct = nx_graph.nodes[containsProductId]
            if 'containedIn' not in containsProduct:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "obj '{}' has <containsProduct> but no valid <containedIn> in '{}'".format(node['@id'],
                                                                                               containsProductId))
                exit(1)


def __check_implementedBy(nx_graph, node_id, node):
    if 'implementedBy' in node:
        implementedBy = node['implementedBy']
        if type(implementedBy) is str:
            implementedBy = [implementedBy]
        for impl_id in implementedBy:
            if impl_id not in nx_graph.node:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "implementation '{}' is referenced by <implementedBy> in '{}'  doesn't exists").format(impl_id,
                                                                                                           node['@id'])
                exit(1)
            impl = nx_graph.node[impl_id]
            if 'providesFunction' not in impl:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "implementation '{}' is referenced by <implementedBy> in '{}' has no valid <providesFunction>".format(
                        impl['@id'],
                        node['@id']))
                exit(1)
            if node_id not in impl['providesFunction']:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "implementation '{}' is referenced by <implementedBy> in '{}' has no valid <providesFunction>".format(
                        impl['@id'],
                        node['@id']))
                exit(1)


def __check_usesFunction(nx_graph, node_id, node):
    if 'usesFunction' in node:
        usesFunction = node['usesFunction']
        if type(usesFunction) is str:
            usesFunction = [usesFunction]
        for func_id in usesFunction:
            if func_id not in nx_graph.node:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "function '{}' is referenced by <usesFunction> in '{}'  doesn't exists".format(func_id,
                                                                                                   node['@id']))
                exit(1)
            funct = nx_graph.node[func_id]
            if 'usedBy' not in funct:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "function '{}' is referenced by <usesFunction> in '{}' has no valid <usedBy>".format(funct['@id'],
                                                                                                         node['@id']))
                exit(1)
            if node_id not in funct['usedBy']:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "function '{}' is referenced by <usesFunction> in '{}' has no valid <usedBy>".format(funct['@id'],
                                                                                                         node['@id']))
                exit(1)


def __check_usedBy(nx_graph, node_id, node):
    if 'usedBy' in node:
        usedBy = node['usedBy']
        if type(usedBy) is str:
            usedBy = [usedBy]
        for obj_id in usedBy:
            user = nx_graph.node[obj_id]
            if node_id not in user['usesFunction']:
                PLUGIN_LOG.error('graph_check error: ')
                PLUGIN_LOG.error(
                    "user '{}' is referenced by <usedBy> in '{}' has no valid <usesFunction>".format(user['@obj_id'],
                                                                                                     node['@obj_id']))
                exit(1)


def __check_containedIn(nx_graph, node_id, node):
    if 'containedIn' in node:
        containedInId = node['containedIn']
        containedIn = nx_graph.nodes[containedInId]
        if node_id not in containedIn['containsProduct']:
            PLUGIN_LOG.error('graph_check error: ')
            PLUGIN_LOG.error(
                "obj '{}' has <containedIn> but no valid <containsProduct> in '{}'".format(node['@id'],
                                                                                           containedIn))
            exit(1)
