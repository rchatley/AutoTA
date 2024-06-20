class Entity:
    types = {'class', 'abstractClass', 'interface', 'constructor', 'method',
             'abstractMethod', 'field'}

    def __init__(self, entity_type='entity', info=None, node=None,
                 package=None, file=None):
        self.type = entity_type
        self.info = info
        self.node = node
        self.package = package
        self.file = file
        self.out_relations = {'has': [],
                              'extends': [],
                              'implements': [],
                              'instantiates': [],
                              'overrides': [],
                              'invokes': [],
                              'parameterOfType': [],
                              'isOfType': [],
                              'hasReturnType': []}
        self.in_relations = {'composes': [],
                             'extendedBy': [],
                             'implementedBy': [],
                             'instantiatedBy': [],
                             'overridenBy': [],
                             'invokedBy': [],
                             'typeOfParameter': [],
                             'isTypeOf': [],
                             'isReturnTypeOf': []}

    def out_degree(self):
        return sum([len(out_relation) for out_relation in
                    self.out_relations.values()])

    def in_degree(self):
        return sum([len(in_relation) for in_relation in
                    self.in_relations.values()])

    def __str__(self):
        return f'{self.file} : {self.type}: {self.info["name"]}'

    def __repr__(self):
        return f'{self.type} : {self.info["name"]}'


class Class(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('class', info, node, package, file)


class AbstractClass(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('abstractClass', info, node, package, file)


class Interface(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('interface', info, node, package, file)


class Constructor(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('constructor', info, node, package, file)


class Method(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('method', info, node, package, file)


class AbstractMethod(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('abstractMethod', info, node, package, file)


class Field(Entity):
    def __init__(self, info=None, node=None, package=None, file=None):
        super().__init__('field', info, node, package, file)


class Relation:
    def __init__(self, entity_from, entity_to, relation_type):
        self.entity_from = entity_from
        self.entity_to = entity_to
        self.relation_type = relation_type

    def __str__(self):
        return f'{self.entity_from} {self.relation_type} {self.entity_to}'

    def __repr__(self):
        return f'{self.entity_from} {self.relation_type} {self.entity_to}'


class Has(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'has')
        class_entity.out_relations['has'].append(member_entity)
        member_entity.in_relations['composes'].append(class_entity)


class Implements(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'implements')
        class_entity.out_relations['implements'].append(member_entity)
        member_entity.in_relations['implementedBy'].append(class_entity)


class Extends(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'extends')
        class_entity.out_relations['extends'].append(member_entity)
        member_entity.in_relations['extendedBy'].append(class_entity)


class ParameterOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'parameterOfType')
        class_entity.out_relations['parameterOfType'].append(member_entity)
        member_entity.in_relations['typeOfParameter'].append(class_entity)


class IsOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'isOfType')
        class_entity.out_relations['isOfType'].append(member_entity)
        member_entity.in_relations['isTypeOf'].append(class_entity)


class HasReturnType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'hasReturnType')
        class_entity.out_relations['hasReturnType'].append(member_entity)
        member_entity.in_relations['isReturnTypeOf'].append(class_entity)


class Invokes(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'invokes')
        class_entity.out_relations['invokes'].append(member_entity)
        member_entity.in_relations['invokedBy'].append(class_entity)


class Overrides(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'overrides')
        class_entity.out_relations['overrides'].append(member_entity)
        member_entity.in_relations['overridenBy'].append(class_entity)


class Instantiates(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'instantiates')
        class_entity.out_relations['instantiates'].append(member_entity)
        member_entity.in_relations['instantiatedBy'].append(class_entity)
