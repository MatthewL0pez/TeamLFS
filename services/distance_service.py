import math


class DistanceService:
    EARTH_RADIUS_KM = 6371  # Earth's radius in km

    @staticmethod
    def haversine(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2

        # Convert to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return DistanceService.EARTH_RADIUS_KM * c

    @staticmethod
    def get_distance(city1_name, city2_name, locations_dict):
        coord1 = locations_dict[city1_name]
        coord2 = locations_dict[city2_name]
        return DistanceService.haversine(coord1, coord2)