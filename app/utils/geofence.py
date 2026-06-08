from math import radians
from math import sin
from math import cos
from math import sqrt
from math import atan2


def distance_in_meters(
    lat1,
    lon1,
    lat2,
    lon2
):

    earth_radius = 6371000

    dlat = radians(
        float(lat2) - float(lat1)
    )

    dlon = radians(
        float(lon2) - float(lon1)
    )

    a = (
        sin(dlat / 2) ** 2
        +
        cos(
            radians(float(lat1))
        )
        *
        cos(
            radians(float(lat2))
        )
        *
        sin(dlon / 2) ** 2
    )

    c = (
        2 *
        atan2(
            sqrt(a),
            sqrt(1 - a)
        )
    )

    return earth_radius * c