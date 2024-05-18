from review_tools.rules.Design.utils import add_node_to_dict
from review_tools.rules.JavaFilter import get_instances_of


def find_pattern(files):
    strategy_node_candidates = {}
    for file in files:
        for interface in get_instances_of(file.ast, node_class='interface'):
            methods = get_instances_of(interface, node_class='method')
            if len(methods) > 0:
                strategy_node_candidates[interface.name] = methods

    if len(strategy_node_candidates) == 0:
        return False

    concrete_strategy_node_candidates = {}
    for file in files:
        for sn in strategy_node_candidates.keys():

            implementing_classes = get_instances_of(file.ast,
                                                    node_class='class',
                                                    node_implements=[sn])
            if len(implementing_classes) > 0:
                for implementing_class in implementing_classes:
                    add_node_to_dict(concrete_strategy_node_candidates, sn,
                                     implementing_class)

    # Find Context

    return concrete_strategy_node_candidates
