from model.objects.points.Point import Point
from model.objects.points.Node import Node
from typing import Dict, List
import csv


class GridPointADC(Point):

    def __init__(self, id: str, num: int, adcs: Dict[Node, int], x: float, y: float, z: float = 0.0):
        super(GridPointADC, self).__init__(id=id, num=num, x=x, y=y, z=z)
        self.__adcs = adcs  # type: Dict[Node, int]
        self.__distance: float = -1

    @property
    def distance(self) -> float:
        return self.__distance

    @distance.setter
    def distance(self, distance: float) -> None:
        self.__distance = distance

    def get_adcs(self, node: Node) -> int:
        return self.__adcs[node]

    def get_str_adcs(self, node_str: str) -> int:
        for node in self.__adcs.keys():
            if node_str == node.id:
                return self.__adcs[node]

    def __lt__(self, other):
        return True if self.distance < other.distance else False

    def __le__(self, other):
        return True if self.distance <= other.distance else False

    def __gt__(self, other):
        return True if self.distance > other.distance else False

    def __ge__(self, other):
        return True if self.distance >= other.distance else False

    def __eq__(self, other):
        return True if GridPointADC.approx_equal(self.distance, other.distance) else False

    def _reset(self):
        self.__distance = -1

    @classmethod
    def create_point_list(cls, file_path: str, *args, **kwargs) -> list:
        assert len(args) == 0, "Grid Points are unable to accept variable arguments."
        assert "access_points" in kwargs.keys(), "You must pass a list of Access Points."

        access_points = kwargs["access_points"]
        points = list()

        with open(file_path) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")

            for row_num, line in enumerate(readCSV):

                if row_num == 0:
                    continue

                point_num = int(line[0])
                x_val = float(line[1])
                y_val = float(line[2])

                adcs = dict()
                for i in range(len(line[3:]) - 1):
                    ap_bssid = line[3 + i]
                    adc = line[4 + i]

                    for ap in access_points:
                        if ap.id == ap_bssid:
                            adcs[ap] = int(adc)

                points.append(GridPointADC(id=str(point_num), num=point_num, x=x_val, y=y_val, adcs=adcs))

        return points

    @classmethod
    def create_point_list_db(cls, gp_list: list, ap_list: list) -> list:
        points = list()
        for gp in gp_list:
            rssis = dict()
            point_id = str(gp['gpnum'])
            point_num = int(point_id[6:])
            x_val = float(gp['x'])
            y_val = float(gp['y'])
            z_val = float(gp['z'])
            values = gp['values']
            for key, value in values.items():
                for ap in ap_list:
                    if key == ap.id:
                        rssis[ap] = int(value)
            points.append(GridPoint(id=point_id, num=point_num, x=x_val, y=y_val, z=z_val, rssis=rssis))

        return points
