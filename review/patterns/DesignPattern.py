from review.filters.JavaFilter import JavaFilter


def add_node_to_dict(node_dict, key, item):
    if key in node_dict:
        node_dict[key].append(item)
    else:
        node_dict[key] = [item]


def find_template_pattern(files):
    template_class_candidates = {}
    for file in files:
        # Get abstract classes
        abstract_classes = JavaFilter(node_class='class',
                                      node_modifiers=[
                                          'abstract']).get_nodes(
            file.ast)

        for abstract_class in abstract_classes:
            class_methods = JavaFilter(node_class='method').get_nodes(
                abstract_class)

            abstract_methods = JavaFilter(node_class='method',
                                          node_modifiers=[
                                              'abstract']).get_nodes(
                abstract_class)

            non_abstract_methods = [method for method in class_methods if
                                    method not in abstract_methods]

            abstract_method_names = [method.name for method in
                                     abstract_methods]
            if len(abstract_methods) > 0:
                method_dict = {}
                for method in non_abstract_methods:
                    for invocation in JavaFilter(
                            node_class='method_invocation').get_nodes(method):
                        if invocation.member in abstract_method_names:
                            add_node_to_dict(method_dict, method.name,
                                             invocation.member)

                if len(method_dict) > 0:
                    template_class_candidates[
                        abstract_class.name] = method_dict

    if len(template_class_candidates) == 0:
        return False

    template_subclasses = {}
    for file in files:
        for tc in template_class_candidates.keys():
            extending_classes = JavaFilter(node_class='class',
                                           node_extends=tc).get_nodes(
                file.ast)
            for extending_class in extending_classes:
                override_methods = JavaFilter(node_class='method',
                                              node_annotations=[
                                                  'Override']).get_nodes(
                    extending_class)
                override_method_names = [method.name for method in
                                         override_methods]
                method_dict = template_class_candidates[tc]

                for template_method in method_dict.keys():
                    methods_to_override = method_dict[template_method]
                    if set(methods_to_override).issubset(
                            set(override_method_names)):
                        add_node_to_dict(template_subclasses, tc,
                                         extending_class.name)

    return template_subclasses


def find_singleton_pattern(files):
    singletons = []
    for file in files:
        # Get classes
        s_classes = JavaFilter(node_class='class').get_nodes(file.ast)
        for s_class in s_classes:
            # Get private fields of type Class
            class_fields = JavaFilter(
                node_class='field',
                node_modifiers=['private'],
                node_type=s_class.name).get_nodes(s_class)
            if not class_fields:
                continue
            # Get methods of type Class
            class_methods = JavaFilter(
                node_class='method',
                node_return_type=s_class.name).get_nodes(s_class)
            if not class_methods:
                continue
            # Get private constructors
            private_constructors = JavaFilter(
                node_class='constructor',
                node_modifiers=['private']).get_nodes(s_class)
            if not private_constructors:
                continue
            singletons.append(s_class.name)
    return singletons


def find_strategy_pattern(files):
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


pattern_dict = {'template': find_template_pattern,
                'strategy': find_strategy_pattern,
                'singleton': find_singleton_pattern}


def find_pattern(pattern, project):
    return pattern_dict[pattern](project.files)

# pattern = {'SINGLETON': {'CLASSNAME': JavaFilter(node_class='class'),
#                              'with':
#                                  {'INSTANCE': JavaFilter(node_class='field',
#                                                          node_modifiers=[
#                                                              'private'],
#                                                          node_type='CLASSNAME'),
#                                   'GETTER': JavaFilter(node_class='method',
#                                                        node_return_type='CLASSNAME'),
#                                   'PRIVATE CONSTRUCTOR': JavaFilter(
#                                       node_class='constructor',
#                                       node_modifiers=['private'])}
#                              }}
