from geopy.distance import geodesic


def geo_distance(geo_point1, geo_point2, mode='km'):
    """
    Calculate the distance between geo-points.
    :param geo_point1: The geo (long, lat) of point 1.
    :param geo_point2: The geo (long, lat) of point2.
    :param mode: The type of measure to return.
    `km`: kilometers.
    `m`: meters.
    `mi`: miles.
    `ft`: feet.
    :return:
    """
    distance = geodesic(geo_point1, geo_point2)
    if mode.__eq__('km'):
        return distance.km
    if mode.__eq__('m'):
        return distance.m
    if mode.__eq__('mile'):
        return distance.mi
    if mode.__eq__('feet'):
        return distance.ft


# if __name__ == '__main__':
#     newport_ri = (41.49008, -71.312796)
#     cleveland_oh = (41.499498, -81.695391)
#     print(geo_distance(newport_ri, cleveland_oh, mode='m'))
