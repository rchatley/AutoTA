from review_tools.rules.Design.utils import add_node_to_dict
from review_tools.rules.JavaFilter import get_instances_of


def find_pattern(files):
    template_class_candidates = {}
    for file in files:
        # Get abstract classes
        abstract_classes = get_instances_of(file.ast, node_class='class',
                                            node_modifiers=['abstract'])

        for abstract_class in abstract_classes:
            class_methods = get_instances_of(abstract_class,
                                             node_class='method')
            abstract_methods = get_instances_of(abstract_class,
                                                node_class='method',
                                                node_modifiers=[
                                                    'abstract'])
            non_abstract_methods = [method for method in class_methods if
                                    method not in abstract_methods]

            abstract_method_names = [method.name for method in
                                     abstract_methods]
            if len(abstract_methods) > 0:
                method_dict = {}
                for method in non_abstract_methods:
                    for invocation in get_instances_of(method,
                                                       node_class='method_invocation'):
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
            extending_classes = get_instances_of(file.ast,
                                                 node_class='class',
                                                 node_extends=tc)
            for extending_class in extending_classes:
                override_methods = get_instances_of(extending_class,
                                                    node_class='method',
                                                    node_annotations=[
                                                        'Override'])
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
