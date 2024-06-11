class Entity:
    types = {'class', 'abstractClass', 'interface', 'constructor', 'method',
             'abstractMethod', 'field'}

    def __init__(self, name, entity_type, info, node=None):
        self.name = name
        self.type = entity_type
        self.info = info
        self.node = node

    def __str__(self):
        return f'{self.type}: {self.name}'

    def __repr__(self):
        return f'Entity(name={self.name}, type={self.type}'


class Class(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'class', info, node)


class AbstractClass(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'abstractClass', info, node)


class Interface(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'interface', info, node)


class Constructor(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'constructor', info, node)


class Method(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'method', info, node)


class AbstractMethod(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'abstractMethod', info, node)


class Field(Entity):
    def __init__(self, name, info, node=None):
        super().__init__(name, 'field', info, node)


class Relation:
    def __init__(self, entity_from, entity_to, relation_type):
        self.entity_from = entity_from
        self.entity_to = entity_to
        self.relation_type = relation_type

    def __str__(self):
        return f'{self.entity_from} {self.relation_type} {self.entity_to}'

    def __repr__(self):
        return (f'Relation(entity_from={self.entity_from}, '
                f'entity_to={self.entity_to}, '
                f'relation_type={self.relation_type})')


class Has(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'has')


class Implements(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'implements')


class Extends(Relation):
    def __init__(self, class_entity, member_entity):
        super().__init__(class_entity, member_entity, 'extends')
