from review_tools.rules.JavaFilter import get_instances_of


def find_pattern(files):
    singletons = []
    for file in files:
        # Get classes
        s_classes = get_instances_of(file.ast, node_class='class')
        for s_class in s_classes:


            # Get private fields of type Class
            # Get methods of type Class
            # Get private constructors


            class_fields = get_instances_of(s_class,
                                            node_class='field',
                                            node_modifiers=['private'],
                                            node_type=s_class.name)
            if not class_fields:
                continue

            class_methods = get_instances_of(s_class,
                                             node_class='method',
                                             node_return_type=s_class.name)
            if not class_methods:
                continue

            private_constructors = get_instances_of(s_class,
                                                    node_class='constructor',
                                                    node_modifiers=['private'])
            if not private_constructors:
                continue
            singletons.append(s_class.name)
    return singletons
