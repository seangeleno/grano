
from grano.core import db
from grano.model import Schema, Entity, Relation


class SchemaCache(object):
    # TODO: move to model?
    SCHEMATA = {}

    @classmethod
    def get(cls, type, name):
        obj = type.OBJ
        if not (obj, name) in cls.SCHEMATA:
            schema = Schema.by_obj_name(obj, name)
            if schema is None:
                raise ValueError("Unknown schema: %s" % name)
            cls.SCHEMATA[(obj, name)] = schema
        return cls.SCHEMATA[(obj, name)]


class _Properties(object):

    def _setup(self):
        self.properties = []


    def set(self, name, value, source_url=None, active=True, key=False):
        self.properties.append({
            'name': name,
            'value': value,
            'source_url': source_url or self.source_url,
            'active': active,
            'key': key
            })


class EntityLoader(_Properties):
    
    def __init__(self, schemata, source_url=None):
        self._setup()
        self.source_url = source_url
        schemata = set(schemata + ['base'])
        self.schemata = [SchemaCache.get(Entity, s) for s in schemata]



class RelationLoader(_Properties):
    
    def __init__(self, schema, source, target, source_url=None):
        self._setup()
        self.source_url = source_url
        self.source = source 
        self.target = target
        self.schema = SchemaCache.get(Relation, schema)


class Loader(object):
    """ A loader is a factory object that can be used to make entities and 
    relations in the database. It will perform some validation and handle 
    database transactions. """

    def __init__(self, source_url=None):
        self.source_url = source_url
        self.entities = []
        self.relations = []


    def make_entity(self, schemata, source_url=None):
        entity = EntityLoader(schemata,
            source_url=source_url or self.source_url)
        self.entities.append(entity)
        return entity


    def make_relation(self, source, target, source_url=None):
        relation = RelationLoader(schema, source, target,
            source_url=source_url or self.source_url)
        self.relations.append(relation)
        return relation


    def persist(self):
        pass