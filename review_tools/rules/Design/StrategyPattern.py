from review_tools.rules.Design.utils import add_node_to_dict
from review_tools.rules.filters.JavaFilter import JavaFilter


def find_pattern(files):
    strategy_node_candidates = {}
    for file in files:
        for interface in JavaFilter(node_class='interface').get_instances_of(
                file.ast):
            methods = JavaFilter(node_class='method').get_instances_of(
                interface)
            if len(methods) > 0:
                strategy_node_candidates[interface.name] = methods

    if len(strategy_node_candidates) == 0:
        return False

    concrete_strategy_node_candidates = {}
    for file in files:
        for sn in strategy_node_candidates.keys():

            implementing_classes = JavaFilter(node_class='class',
                                              node_implements=[
                                                  sn]).get_instances_of(
                file.ast)

            if len(implementing_classes) > 0:
                for implementing_class in implementing_classes:
                    add_node_to_dict(concrete_strategy_node_candidates, sn,
                                     implementing_class)

    # Find Context

    return concrete_strategy_node_candidates
