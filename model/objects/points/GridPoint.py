from model.objects.points.Point import Point
from model.objects.points.Node import Node
from typing import Dict, List
import csv


class GridPoint(Point):

    def __init__(self, id: str, ple_vals: Dict[Node, float], x: float, y: float, z: int = 0):
        super(GridPoint, self).__init__(id=id, x=x, y=y, z=z)
        self.__pleValues = ple_vals     # type: Dict[Node, float]
        self.__distance: float = -1

    # region Properties
    @property
    def distance(self) -> float:
        return self.__distance
    # endregion

    # region Setters
    @distance.setter
    def distance(self, distance: float) -> None:
        self.__distance = distance

    # region Comparison Operators
    def __lt__(self, other):
        return True if self.distance < other.distance else False

    def __le__(self, other):
        return True if self.distance <= other.distance else False

    def __gt__(self, other):
        return True if self.distance > other.distance else False

    def __ge__(self, other):
        return True if self.distance >= other.distance else False

    def __eq__(self, other):
        return True if GridPoint.approx_equal(self.distance, other.distance) else False
    # endregion

    # region Method Overrides
    def _reset(self):
        self.__distance = -1

    @classmethod
    def create_point_list_db(cls, gp_list: list, ap_list:list) -> list:
        points = list()
        for gp in gp_list:
            point_num = int(gp['gpnum'])
            x_val = float(gp['x'])
            y_val = float(gp['y'])

            ple_vals = dict()
            for ap in ap_list:
                if ap.id == str(gp['ap1']):
                    ple_vals[ap] = float(gp['ple1'])
                if ap.id == str(gp['ap2']):
                    ple_vals[ap] = float(gp['ple2'])
                if ap.id == str(gp['ap3']):
                    ple_vals[ap] = float(gp['ple3'])
                if ap.id == str(gp['ap4']):
                    ple_vals[ap] = float(gp['ple4'])
            points.append(GridPoint(id=str(point_num), x=x_val, y=y_val, ple_vals=ple_vals))
        return points

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

                ple_vals = dict()
                for i in range(len(line[3:]) - 1):
                    ap_bssid = line[3 + i]
                    ple = line[4 + i]

                    for ap in access_points:
                        if ap.id == ap_bssid:
                            ple_vals[ap] = float(ple)

                points.append(GridPoint(id=str(point_num), x=x_val, y=y_val, ple_vals=ple_vals))

        return points
    # endregion

