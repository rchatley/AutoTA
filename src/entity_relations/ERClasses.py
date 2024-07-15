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
        self.relations = {'has': [], 'composes': [],
                          'extends': [], 'extendedBy': [],
                          'implements': [], 'implementedBy': [],
                          'instantiates': [], 'instantiatedBy': [],
                          'overrides': [], 'overridenBy': [],
                          'invokes': [], 'invokedBy': [],
                          'parameterOfType': [], 'typeOfParameter': [],
                          'isOfType': [], 'isTypeOf': [],
                          'hasReturnType': [], 'isReturnTypeOf': []}

    def __str__(self):
        if self.info is None or self.info["name"] is None:
            return f'{self.type}'
        return f'{self.file} : {self.type}: {self.info["name"]}'

    def __repr__(self):
        if self.info is None or self.info["name"] is None:
            return f'{self.type}'
        return f'{self.file} : {self.type}: {self.info["name"]}'


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
        class_entity.relations['has'].append(member_entity)
        member_entity.relations['composes'].append(class_entity)


class Implements(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'implements')
        class_entity.relations['implements'].append(member_entity)
        member_entity.relations['implementedBy'].append(class_entity)


class Extends(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'extends')
        class_entity.relations['extends'].append(member_entity)
        member_entity.relations['extendedBy'].append(class_entity)


class ParameterOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'parameterOfType')
        class_entity.relations['parameterOfType'].append(member_entity)
        member_entity.relations['typeOfParameter'].append(class_entity)


class IsOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'isOfType')
        class_entity.relations['isOfType'].append(member_entity)
        member_entity.relations['isTypeOf'].append(class_entity)


class HasReturnType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'hasReturnType')
        class_entity.relations['hasReturnType'].append(member_entity)
        member_entity.relations['isReturnTypeOf'].append(class_entity)


class Invokes(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'invokes')
        class_entity.relations['invokes'].append(member_entity)
        member_entity.relations['invokedBy'].append(class_entity)


class Overrides(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'overrides')
        class_entity.relations['overrides'].append(member_entity)
        member_entity.relations['overridenBy'].append(class_entity)


class Instantiates(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'instantiates')
        class_entity.relations['instantiates'].append(member_entity)
        member_entity.relations['instantiatedBy'].append(class_entity)
