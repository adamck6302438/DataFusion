from model.objects.points.GridPointADC import GridPointADC
from model.objects.points.Node import Node
from model.objects.points.Centroid import Centroid
from typing import Tuple, List, Dict
import numpy as np
import math

def get_KNNv1(centroid_points: List[Centroid], rssis: Dict[Node, int],
              grid_points_only: List[GridPointADC] = None) -> Tuple[float, float]:
    """
    :param grid_points_only:
    :param centroid_points: List of Centroid Points to search against.
    :param rssis: Dict of Access Point: RSSI values.
    :return: A tuple of X, Y denoting the position related to the passed RSSIs.
    """

    for cp in centroid_points:
        if grid_points_only is None:
            grid_points_only = cp.CornerPoints
        else:
            for cnp in cp.CornerPoints:
                if cnp in grid_points_only:
                    pass
                else:
                    grid_points_only.append(cnp)

    for gp in grid_points_only:
        distances = 0
        for ap, rssi in rssis.items():
            distance = math.pow((rssi - gp.get_rssis(ap)), 2)
            distances += distance
        try:
            distances = math.sqrt(distances)
            gp.distance = distances
            # gp.distance = np.sqrt(gp.distance)
        except RuntimeWarning:
            print("Oop!")

        # Sort the grid points by distance:
        ####  ref: closest_cp.sort_corner_points_by_distance()

        # Selection sort
    for i in range(len(grid_points_only)):
        min_index = i
        for j in range(i + 1, len(grid_points_only)):
            if grid_points_only[min_index] > grid_points_only[j]:
                min_index = j

        grid_points_only[i], grid_points_only[min_index] = grid_points_only[min_index], grid_points_only[i]

        #### TODO: could consider use other sorting algorithms

        # Create a new central point of the K (current K=3) proximate Gird-Points:
    x = round(((grid_points_only[0].x + grid_points_only[1].x + grid_points_only[2].x) / 3), 2)
    y = round(((grid_points_only[0].y + grid_points_only[1].y + grid_points_only[2].y) / 3), 2)

    return x, y