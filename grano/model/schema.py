from grano.core import db
from grano.model.common import IntBase
from grano.model.util import slugify_column
from grano.model.attribute import Attribute
from grano.model.property import Property


class Schema(db.Model, IntBase):
    __tablename__ = 'schema'
    SCHEMATA = {}

    name = db.Column(db.Unicode())
    label = db.Column(db.Unicode())
    label_in = db.Column(db.Unicode())
    label_out = db.Column(db.Unicode())
    hidden = db.Column(db.Boolean())
    obj = db.Column(db.Unicode())

    attributes = db.relationship(Attribute, backref='schema', lazy='joined')
    properties = db.relationship(Property, backref='schema', lazy='dynamic')
    relations = db.relationship('Relation', backref='schema', lazy='dynamic')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def get_attribute(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute


    @classmethod
    def cached(cls, project, type, name):
        obj = type.__tablename__
        if not (project, obj, name) in cls.SCHEMATA:
            schema = Schema.by_obj_name(obj, name)
            if schema is None:
                raise ValueError("Unknown schema: %s" % name)
            cls.SCHEMATA[(project, obj, name)] = schema
        return cls.SCHEMATA[(project, obj, name)]


    @classmethod
    def by_name(cls, project, name):
        q = db.session.query(cls).filter_by(name=name)
        q = q.filter_by(project=project)
        return q.first()


    @classmethod
    def by_obj_name(cls, project, obj, name):
        q = db.session.query(cls)
        q = q.filter_by(project=project)
        q = q.filter_by(name=name)
        q = q.filter_by(obj=obj)
        return q.first()
