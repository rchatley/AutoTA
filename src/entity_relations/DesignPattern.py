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

    def relations_contained(self, pattern_relations, graph_relations):
        if pattern_relations is None:
            return True
        for relation_type in pattern_relations.keys():
            if len(pattern_relations[relation_type]) > len(
                    graph_relations[relation_type]):
                return False

            matching_types = [graph_relation.type for graph_relation in
                              graph_relations[relation_type]]

            for relation in pattern_relations[relation_type]:
                if self.entity_dict[relation].type not in matching_types:
                    return False

        return True

    def entity_expressed(self, pattern_entity, graph_entity, relations):
        return not_none_check(pattern_entity.type,
                              graph_entity.type) and check_dict(
            pattern_entity.info,
            graph_entity.info) and self.relations_contained(
            relations, graph_entity.relations)

    def find_potential_isomorphisms(self, graph):
        node_dict = {}
        missing_nodes = []

        # Find all potential nodes for each entity
        for from_node_name, entity in self.entity_dict.items():
            relations = self.relation_dict.get(
                from_node_name) if from_node_name in self.relation_dict else None
            potential_isomorphisms = [graph_entity for graph_entity in
                                      graph['entities'] if
                                      self.entity_expressed(entity,
                                                            graph_entity,
                                                            relations)]
            if len(potential_isomorphisms) == 0:
                missing_nodes.append(from_node_name)
            else:
                node_dict[from_node_name] = potential_isomorphisms

        single_missing_node = None
        if len(missing_nodes) > 1:
            return f'Could not find any potential instances of {self.pattern} pattern'
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
                        continue

                    for matching_from_entity in matching_from_entities:
                        matched_from = False

                        for i, matching_to_entity in enumerate(
                                matching_to_entities):
                            if matching_to_entity in \
                                    matching_from_entity.relations[
                                        rel_type]:
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
                            if single_missing_node is not None:
                                return f'Could not find any potential instances of {self.pattern} pattern'
                            single_missing_node = to_node_name

                    for from_ent in from_ents_to_remove:
                        node_dict[from_node_name].remove(from_ent)
                        if not node_dict[from_node_name]:
                            if single_missing_node is not None:
                                return f'Could not find any potential instances of {self.pattern} pattern'
                            single_missing_node = from_node_name

        if single_missing_node is not None:
            return f'Implementation of {self.pattern} pattern is almost complete: \n MISSING ENTITY: {single_missing_node}'

        return_string = f'Found potential instance of {self.pattern} pattern:\n'
        for node_name, entities in node_dict.items():
            if len(entities) == 1:
                return_string += ' -' + node_name.upper() + ':\n' + str(
                    entities[0]) + '\n'
            else:
                return_string += ' -' + node_name.upper() + ':\n'
                for entity in entities:
                    return_string += str(entity) + '\n'

        return return_string
