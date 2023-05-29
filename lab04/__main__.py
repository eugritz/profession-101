from app import app
from marshmallow import fields
import math
import unittest


class TetrahedronCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_validation(self):
        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '0',
            'radius': 'test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['radius'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '0',
            'edge': '12test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '0.2',
            'edge': '1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '-1',
            'edge': '-1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']


    def test_missing(self):
        res = self.client.post('/api/calculate/tetrahedron', json={
            'radius': '1',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Missing data for required field.']

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either edge or radius must be passed.'


    def test_volume(self):
        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': 1,
            'radius': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': 1,
            'edge': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        radius = 1
        edge = 4 * radius / math.sqrt(6)
        precision = 0
        volume = math.pow(edge, 3) * math.sqrt(2) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.23456789
        edge = 4 * radius / math.sqrt(6)
        precision = 8
        volume = math.pow(edge, 3) * math.sqrt(2) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.2345678912345789
        precision = 16
        volume = math.pow(edge, 3) * math.sqrt(2) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': precision,
            'edge': edge,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual


class HexahedronCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_validation(self):
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
            'radius': 'test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['radius'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
            'edge': '12test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0.2',
            'edge': '1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/tetrahedron', json={
            'precision': '-1',
            'edge': '-1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
            'x': '0,0',
            'y': '1,0',
            'z': '2,0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['x'] == ['Not a valid number.']
        assert data['errors']['y'] == ['Not a valid number.']
        assert data['errors']['z'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
            'x': '-0',
            'y': '-1',
            'z': '-2',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['y'] == ['Not a valid number.']
        assert data['errors']['z'] == ['Not a valid number.']


    def test_missing(self):
        res = self.client.post('/api/calculate/hexahedron', json={
            'radius': '1',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Missing data for required field.']

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either x, y, z or edge or radius must be passed.'

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': '0',
            'x': '0',
            'y': '0'
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either x, y, z or edge or radius must be passed.'


    def test_volume(self):
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': 1,
            'radius': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': 1,
            'edge': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': 1,
            'x': 0,
            'y': 1,
            'z': 2
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        radius = 1
        edge = 2 * radius / math.sqrt(3)
        precision = 0
        volume = edge * edge * edge
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.23456789
        edge = 2 * radius / math.sqrt(3)
        precision = 8
        volume = edge * edge * edge
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.2345678912345789
        precision = 16
        volume = edge * edge * edge
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': precision,
            'edge': edge,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        x, y, z = 0.12345678, 0.23456789, 0.34567891
        precision = 12
        volume = x * y * z
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/hexahedron', json={
            'precision': precision,
            'x': x,
            'y': y,
            'z': z,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual


class OctahedronCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_validation(self):
        res = self.client.post('/api/calculate/octahedron', json={
            'precision': '0',
            'radius': 'test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['radius'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/octahedron', json={
            'precision': '0',
            'edge': '12test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/octahedron', json={
            'precision': '0.2',
            'edge': '1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/octahedron', json={
            'precision': '-1',
            'edge': '-1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']


    def test_missing(self):
        res = self.client.post('/api/calculate/octahedron', json={
            'radius': '1',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Missing data for required field.']

        res = self.client.post('/api/calculate/octahedron', json={
            'precision': '0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either edge or radius must be passed.'


    def test_volume(self):
        res = self.client.post('/api/calculate/octahedron', json={
            'precision': 1,
            'radius': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/octahedron', json={
            'precision': 1,
            'edge': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        radius = 1
        edge = 2 * radius / math.sqrt(2)
        precision = 0
        volume = math.pow(edge, 3) * math.sqrt(2) / 3
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/octahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.23456789
        edge = 2 * radius / math.sqrt(2)
        precision = 8
        volume = math.pow(edge, 3) * math.sqrt(2) / 3
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/octahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.2345678912345789
        precision = 16
        volume = math.pow(edge, 3) * math.sqrt(2) / 3
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/octahedron', json={
            'precision': precision,
            'edge': edge,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual


class DodecahedronCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_validation(self):
        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': '0',
            'radius': 'test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['radius'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': '0',
            'edge': '12test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': '0.2',
            'edge': '1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': '-1',
            'edge': '-1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']


    def test_missing(self):
        res = self.client.post('/api/calculate/dodecahedron', json={
            'radius': '1',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Missing data for required field.']

        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': '0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either edge or radius must be passed.'


    def test_volume(self):
        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': 1,
            'radius': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': 1,
            'edge': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        radius = 1
        edge = 4 * radius / (1 + math.sqrt(5)) / math.sqrt(3)
        precision = 0
        volume = math.pow(edge, 3) * (15 + 7 * math.sqrt(5)) / 4
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.23456789
        edge = 4 * radius / (1 + math.sqrt(5)) / math.sqrt(3)
        precision = 8
        volume = math.pow(edge, 3) * (15 + 7 * math.sqrt(5)) / 4
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.2345678912345789
        precision = 16
        volume = math.pow(edge, 3) * (15 + 7 * math.sqrt(5)) / 4
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/dodecahedron', json={
            'precision': precision,
            'edge': edge,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual


class IcosahedronCalculator(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


    def test_validation(self):
        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': '0',
            'radius': 'test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['radius'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': '0',
            'edge': '12test',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': '0.2',
            'edge': '1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']

        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': '-1',
            'edge': '-1.2f',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Not a valid integer.']
        assert data['errors']['edge'] == ['Not a valid number.']


    def test_missing(self):
        res = self.client.post('/api/calculate/icosahedron', json={
            'radius': '1',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors']['precision'] == ['Missing data for required field.']

        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': '0',
        })
        data = res.get_json(force=True)
        assert res.status_code == 400
        assert data['errors'] == 'Either edge or radius must be passed.'


    def test_volume(self):
        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': 1,
            'radius': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': 1,
            'edge': 0,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == 0

        radius = 1
        edge = 4 * radius / (10 + 2 * math.sqrt(5))
        precision = 0
        volume = 5 * math.pow(edge, 3) * (3 + math.sqrt(5)) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.23456789
        edge = 4 * radius / (10 + 2 * math.sqrt(5))
        precision = 8
        volume = 5 * math.pow(edge, 3) * (3 + math.sqrt(5)) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': precision,
            'radius': radius,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual

        radius = 1.2345678912345789
        precision = 16
        volume = 5 * math.pow(edge, 3) * (3 + math.sqrt(5)) / 12
        actual = round(volume, precision)
        res = self.client.post('/api/calculate/icosahedron', json={
            'precision': precision,
            'edge': edge,
        })
        data = res.get_json(force=True)
        assert res.status_code == 200
        assert data['data']['volume'] == actual


if __name__ == '__main__':
    unittest.main()
