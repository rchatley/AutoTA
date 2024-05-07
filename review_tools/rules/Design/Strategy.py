from review_tools.rules.JavaFilter import get_instances_of


def add_node_to_dict(node_dict, key, item):
    if key in node_dict:
        node_dict[key].append(item)
    else:
        node_dict[key] = [item]


def get_strategy_candidates(files):
    strategy_node_candidates = {}
    for file in files:
        for interface in get_instances_of(file.ast, node_class='interface'):
            methods = get_instances_of(interface, node_class='method')
            if len(methods) > 0:
                strategy_node_candidates[interface.name] = methods

    return strategy_node_candidates


def get_concrete_strategy_candidates(files, strategy_node_candidates):
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

    return concrete_strategy_node_candidates


def check_for_strategy_pattern(files):
    strategy_node_candidates = get_strategy_candidates(files)
    if len(strategy_node_candidates) == 0:
        return False
    concrete_strategy_node_candidates = get_concrete_strategy_candidates(files,
                                                                         strategy_node_candidates)

    # Find Context

    return concrete_strategy_node_candidates
