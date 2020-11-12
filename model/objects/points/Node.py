from itertools import combinations
from math import pow, log10
from typing import Tuple, List
from model.objects.points.Point import Point
import csv


class Node(Point):
    def __init__(self, id: str, num: int, x: float, y: float, z: float):
        super(Node, self).__init__(id=id, num=num, x=x, y=y, z=z)

    @property
    def type(self) -> str:
        return self.__type

    def __lt__(self, other):
        return True if self.num < other.num else False

    def __le__(self, other):
        return True if self.num <= other.num else False

    def __gt__(self, other):
        return True if self.num > other.num else False

    def __ge__(self, other):
        return True if self.num >= other.num else False

    def _reset(self):
        pass

    @classmethod
    def create_point_list(cls, file_path: str, *args, **kwargs) -> list:
        points = list()

        return points
