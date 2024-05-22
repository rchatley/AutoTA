from review_tools.filters.JavaFilter import JavaFilter
from review_tools.rules.design_patterns.utils import add_node_to_dict


def find_pattern(files):
    strategy_node_candidates = {}
    for file in files:
        for interface in JavaFilter(node_class='interface').get_nodes(
                file.ast):
            methods = JavaFilter(node_class='method').get_nodes(
                interface)
            if len(methods) > 0:
                method_names = [method.name for method in methods]
                strategy_node_candidates[interface.name] = {
                    'methods': method_names}

    if len(strategy_node_candidates) == 0:
        return False

    for file in files:
        for sn in strategy_node_candidates.keys():
            for context in JavaFilter(node_class='class').get_nodes(
                    file.ast):
                fields = JavaFilter(
                    node_class='field', node_type=sn).get_nodes(context)
                if len(fields) > 0:
                    field_names = [field.declarators[0].name for field in
                                   fields]
                    constructors = JavaFilter(
                        node_class='constructor').get_nodes(context)
                    methods = JavaFilter(
                        node_class='method').get_nodes(context)

                    con_and_meth = constructors + methods

                    for method in con_and_meth:
                        if sn in [param.type.name for param in
                                  method.parameters]:
                            for next_method in methods:
                                invocations = JavaFilter(
                                    node_class='method_invocation').get_nodes(
                                    next_method)
                                for invocation in invocations:
                                    if invocation.member in \
                                            strategy_node_candidates[sn][
                                                'methods']:
                                        if invocation.qualifier in field_names:
                                            add_node_to_dict(
                                                strategy_node_candidates[sn],
                                                'context',
                                                context.name)

    for file in files:
        for sn in strategy_node_candidates.keys():

            implementing_classes = JavaFilter(node_class='class',
                                              node_implements=[
                                                  sn]).get_nodes(
                file.ast)

            if len(implementing_classes) > 0:
                for implementing_class in implementing_classes:
                    add_node_to_dict(strategy_node_candidates[sn],
                                     'concrete_classes',
                                     implementing_class.name)

    return strategy_node_candidates
