from src.entity_relations.ERClasses import *


def not_none_check(a, b):
    return a is None or a == b


def check_dict(dict_a, dict_b):
    if dict_a is None:
        return True
    if dict_b is None:
        return False
    for k, vs in dict_a.items():
        if k == 'modifiers':
            for v in vs:
                if v not in dict_b[k]:
                    return False
    return True


def entities_equal_on_left(entity1, entity2):
    return not_none_check(entity1.name, entity2.name) and not_none_check(
        entity1.type, entity2.type) and check_dict(entity1.info, entity2.info)


def find_matching_entities(entity, graph):
    return [graph_entity for graph_entity in graph['entities'] if
            entities_equal_on_left(entity, graph_entity)]


def relation_in_graph(entity_from, rel_type, entity_to, graph):
    for relation in graph['relations']:
        if rel_type == relation.relation_type and entity_from == relation.entity_from and entity_to == relation.entity_to:
            return True
    return False


class DesignPattern:
    def __init__(self, pattern='singleton'):
        self.pattern = pattern
        if pattern == 'singleton':
            self.entity_dict = {
                'singleton': Class(),
                'private constructor': Constructor(
                    info={'modifiers': {'private'}}),
                'private instance': Field(
                    info={'modifiers': {'private'}}),
                'get_instance': Method()
            }
            self.relation_dict = {
                'singleton': {
                    'has': ['private constructor', 'private instance',
                            'get_instance']
                },
                'private instance': {
                    'isOfType': ['singleton']
                },
                'get_instance': {
                    'hasReturnType': ['singleton']
                }
            }
        elif pattern == 'templateMethod':
            self.entity_dict = {
                'template': AbstractClass(),
                'abstract method': AbstractMethod(),
                'hook method': Method(),
                'subclass': Class(),
                'override': Method()
            }
            self.relation_dict = {
                'template': {
                    'has': ['abstract method', 'hook method']
                },
                'subclass': {
                    'extends': ['template'],
                    'has': ['override']
                },
                'hook method': {
                    'invokes': ['abstract method']
                }
            }
        elif pattern == 'strategy':
            self.entity_dict = {
                'context': Class(),
                'strategy': Interface(),
                'strategy_method': AbstractMethod(),
                'concrete_strategy_a': Class(),
                'concrete_strategy_b': Class(),
                'execute_strategy': Method(),
            }
            self.relation_dict = {
                'context': {
                    'has': ['execute_strategy']
                },
                'strategy': {
                    'has': ['strategy_method']
                },
                'concrete_strategy_a': {
                    'implements': ['strategy']
                },
                'concrete_strategy_b': {
                    'implements': ['strategy']
                },
                'execute_strategy': {
                    'invokes': ['strategy_method']
                }
            }

    def find_potential_isomorphisms(self, graph):
        node_dict = {}
        missing_nodes = []

        # Find all potential nodes for each entity
        for from_node_name, entity in self.entity_dict.items():
            potential_isomorphisms = find_matching_entities(entity, graph)
            if len(potential_isomorphisms) == 0:
                missing_nodes.append(from_node_name)
            else:
                node_dict[from_node_name] = potential_isomorphisms

        single_missing_node = None

        if len(missing_nodes) > 1:
            print('COULD NOT FIND PATTERN')
            for missing_node in missing_nodes:
                print(missing_node)
            return
        elif len(missing_nodes) == 1:
            single_missing_node = missing_nodes[0]
            node_dict[missing_nodes[0]] = [Entity()]

        for from_node_name, relations in self.relation_dict.items():
            for rel_type, to_node_names in relations.items():
                for to_node_name in to_node_names:
                    from_ents_to_remove = []
                    to_ents_to_remove = []

                    matching_from_entities = node_dict[from_node_name]
                    matching_to_entities = node_dict[to_node_name]
                    ents_to_matches = [False] * len(matching_to_entities)
                    if to_node_name == single_missing_node or from_node_name == single_missing_node:
                        print('MISSING')
                        continue

                    for matching_from_entity in matching_from_entities:
                        matched_from = False

                        for i, matching_to_entity in enumerate(
                                matching_to_entities):
                            if relation_in_graph(matching_from_entity,
                                                 rel_type, matching_to_entity,
                                                 graph):
                                matched_from = True
                                ents_to_matches[i] = True
                        if not matched_from:
                            from_ents_to_remove.append(matching_from_entity)

                    for i, matches in enumerate(ents_to_matches):
                        if not matches:
                            to_ents_to_remove.append(matching_to_entities[i])

                    for to_ent in to_ents_to_remove:
                        node_dict[to_node_name].remove(to_ent)
                        if not node_dict[to_node_name]:
                            print('COULD NOT FIND PATTERN')
                            return

                    for from_ent in from_ents_to_remove:
                        node_dict[from_node_name].remove(from_ent)
                        if not node_dict[from_node_name]:  #
                            print('COULD NOT FIND PATTERN')
                            return

        return_string = "Found potential instance of " + self.pattern + " pattern:"
        for node_name, entities in node_dict.items():
            if len(entities) == 1:
                return_string += node_name.upper() + ': ' + str(
                    entities[0]) + '\n'
            else:
                return_string += node_name.upper() + ': '
                for entity in entities:
                    return_string += str(entity) + '\n'

        return return_string
