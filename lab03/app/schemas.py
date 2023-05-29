from .figures import Dodecahedron, Icosahedron, Octahedron, Tetrahedron, Hexahedron
from marshmallow import Schema, fields, post_dump, post_load


class FigureSchema(Schema):
    precision = fields.Int(data_key='precision', required=True)
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус (R)'})
    volume = fields.Float(data_key='volume', dump_only=True)

    groups = [[edge], [radius]]


    @post_dump
    def volume_precision(self, in_data, **kwargs):
        in_data['volume'] = round(in_data['volume'], in_data['precision'])
        return in_data


class TetrahedronSchema(FigureSchema):
    id = 'tetrahedron'
    name = 'Тетраэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/7/70/Tetrahedron.gif'


    @post_load
    def make_tetrahedron(self, data, **kwargs):
        return Tetrahedron(**data)


class HexahedronSchema(FigureSchema):
    x = fields.Float(data_key='x', metadata={'name': 'Ширина'})
    y = fields.Float(data_key='y', metadata={'name': 'Толщина'})
    z = fields.Float(data_key='z', metadata={'name': 'Высота'})

    id = 'hexahedron'
    name = 'Шестиугольник (Куб)'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/4/48/Hexahedron.gif'
    groups = [[x, y, z], *FigureSchema.groups]


    @post_load
    def make_hexahedron(self, data, **kwargs):
        return Hexahedron(**data)


class OctahedronSchema(FigureSchema):
    id = 'octahedron'
    name = 'Октаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Octahedron.gif'


    @post_load
    def make_octahedron(self, data, **kwargs):
        return Octahedron(**data)


class DodecahedronSchema(FigureSchema):
    id = 'dodecahedron'
    name = 'Додекаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Dodecahedron.gif'


    @post_load
    def make_dodecahedron(self, data, **kwargs):
        return Dodecahedron(**data)


class IcosahedronSchema(FigureSchema):
    id = 'icosahedron'
    name = 'Икосаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Icosahedron.gif'


    @post_load
    def make_icosahedron(self, data, **kwargs):
        return Icosahedron(**data)


FIGURES = [
    TetrahedronSchema,
    HexahedronSchema,
    OctahedronSchema,
    DodecahedronSchema,
    IcosahedronSchema
]
