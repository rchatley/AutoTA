class Entity:
    types = {'class', 'abstractClass', 'interface', 'constructor', 'method',
             'abstractMethod', 'field'}

    def __init__(self, entity_type=None, name=None, info=None, node=None):
        self.type = entity_type
        self.name = name
        self.info = info
        self.node = node

    def __str__(self):
        return f'{self.type}: {self.name}'

    def __repr__(self):
        return f'{self.type} : {self.name}'


class Class(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('class', name, info, node)


class AbstractClass(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('abstractClass', name, info, node)


class Interface(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('interface', name, info, node)


class Constructor(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('constructor', name, info, node)


class Method(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('method', name, info, node)


class AbstractMethod(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('abstractMethod', name, info, node)


class Field(Entity):
    def __init__(self, name=None, info=None, node=None):
        super().__init__('field', name, info, node)


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


class Implements(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'implements')


class Extends(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'extends')


class ParameterOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'parameterOfType')


class IsOfType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'isOfType')


class HasReturnType(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'hasReturnType')


class Invokes(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'invokes')
