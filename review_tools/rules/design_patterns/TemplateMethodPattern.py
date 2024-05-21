from review_tools.filters.JavaFilter import JavaFilter
from review_tools.rules.design_patterns.utils import add_node_to_dict


def find_pattern(files):
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
