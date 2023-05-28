from marshmallow import Schema, fields


class TetrahedronSchema(Schema):
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус'})

    id = 'tetrahedron'
    name = 'Тетраэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/7/70/Tetrahedron.gif'
    groups = [[edge], [radius]]


class HexahedronSchema(Schema):
    x = fields.Float(data_key='x', metadata={'name': 'Ширина'})
    y = fields.Float(data_key='y', metadata={'name': 'Толщина'})
    z = fields.Float(data_key='z', metadata={'name': 'Высота'})
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус'})

    id = 'hexahedron'
    name = 'Шестиугольник (Куб)'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/4/48/Hexahedron.gif'
    groups = [[x, y, z], [edge], [radius]]


class OctahedronSchema(Schema):
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус'})

    id = 'octahedron'
    name = 'Октаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/1/14/Octahedron.gif'
    groups = [[edge], [radius]]


class DodecahedronSchema(Schema):
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус'})

    id = 'dodecahedron'
    name = 'Додекаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/7/73/Dodecahedron.gif'
    groups = [[edge], [radius]]


class IcosahedronSchema(Schema):
    edge = fields.Float(data_key='edge', metadata={'name': 'Ребро'})
    radius = fields.Float(data_key='radius', metadata={'name': 'Радиус'})

    id = 'icosahedron'
    name = 'Икосаэдр'
    preview_src = 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Icosahedron.gif'
    groups = [[edge], [radius]]
