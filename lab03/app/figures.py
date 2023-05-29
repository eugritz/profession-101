from dataclasses import dataclass
from typing import Optional
import math


class CalculationError(Exception):
    pass


@dataclass
class Figure:
    precision: int
    edge: Optional[float] = None
    radius: Optional[float] = None


@dataclass
class Tetrahedron(Figure):
    @property
    def volume(self):
        if self.edge != None:
            return math.pow(self.edge, 3) * math.sqrt(2) / 12
        elif self.radius != None:
            edge = 4 * self.radius / math.sqrt(6)
            return math.pow(edge, 3) * math.sqrt(2) / 12
        raise CalculationError('Either edge or radius must be passed.')


@dataclass
class Hexahedron(Figure):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None


    @property
    def volume(self):
        if self.x != None and self.y != None and self.z != None:
            return self.x * self.y * self.z
        elif self.edge != None:
            return self.edge * self.edge * self.edge
        elif self.radius != None:
            edge = 2 * self.radius / math.sqrt(3)
            return edge * edge * edge
        raise CalculationError('Either x, y, z or edge or radius must be passed.')


@dataclass
class Octahedron(Figure):
    @property
    def volume(self):
        if self.edge != None:
            return math.pow(self.edge, 3) * math.sqrt(2) / 3
        elif self.radius != None:
            edge = 2 * self.radius / math.sqrt(2)
            return math.pow(edge, 3) * math.sqrt(2) / 3
        raise CalculationError('Either edge or radius must be passed.')


@dataclass
class Dodecahedron(Figure):
    @property
    def volume(self):
        if self.edge != None:
            return math.pow(self.edge, 3) * (15 + 7 * math.sqrt(5)) / 4
        elif self.radius != None:
            edge = 4 * self.radius / (1 + math.sqrt(5)) / math.sqrt(3)
            return math.pow(edge, 3) * (15 + 7 * math.sqrt(5)) / 4
        raise CalculationError('Either edge or radius must be passed.')


@dataclass
class Icosahedron(Figure):
    @property
    def volume(self):
        if self.edge != None:
            return 5 * math.pow(self.edge, 3) * (3 + math.sqrt(5)) / 12
        elif self.radius != None:
            edge = 4 * self.radius / (10 + 2 * math.sqrt(5))
            return 5 * math.pow(edge, 3) * (3 + math.sqrt(5)) / 12
        raise CalculationError('Either edge or radius must be passed.')
