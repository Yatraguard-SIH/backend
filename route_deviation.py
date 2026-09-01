import time
from math import asin, cos, radians, sin, sqrt

try:
    from geopy.distance import geodesic
except ImportError:
    class _GeoDistance:
        def __init__(self, meters):
            self.meters = meters

    def geodesic(point1, point2):
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        meters = 6371000 * c
        return _GeoDistance(meters)


class Tier:
    SAFE = "SAFE"
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"


TIER_1_THRESHOLD_M = 200
TIER_2_THRESHOLD_M = 500


def _point_to_segment_distance_m(point, seg_start, seg_end):
    lat1, lng1 = seg_start
    lat2, lng2 = seg_end
    lat0, lng0 = point

    dx, dy = lat2 - lat1, lng2 - lng1
    if dx == 0 and dy == 0:
        return geodesic(point, seg_start).meters

    t = ((lat0 - lat1) * dx + (lng0 - lng1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    closest = (lat1 + t * dx, lng1 + t * dy)

    return geodesic(point, closest).meters


def check_deviation(current_point, route_coords):
    if not route_coords or len(route_coords) < 2:
        raise ValueError("route_coords must have at least 2 points")

    best_dist = float("inf")
    best_point = route_coords[0]

    for i in range(len(route_coords) - 1):
        seg_start, seg_end = route_coords[i], route_coords[i + 1]
        dist = _point_to_segment_distance_m(current_point, seg_start, seg_end)
        if dist < best_dist:
            best_dist = dist
            best_point = seg_start

    if best_dist > TIER_2_THRESHOLD_M:
        tier = Tier.TIER_2
    elif best_dist > TIER_1_THRESHOLD_M:
        tier = Tier.TIER_1
    else:
        tier = Tier.SAFE

    return {
        "tier": tier,
        "distance_m": round(best_dist, 1),
        "nearest_point": best_point,
    }


class DeviationTracker:
    def __init__(self, route_coords, ack_window_seconds=60):
        self.route_coords = route_coords
        self.ack_window_seconds = ack_window_seconds
        self.tier1_since = None
        self.acknowledged = False

    def update(self, current_point):
        result = check_deviation(current_point, self.route_coords)

        if result["tier"] == Tier.SAFE:
            self.tier1_since = None
            self.acknowledged = False
            result["action"] = "NONE"
            return result

        if result["tier"] == Tier.TIER_1:
            if self.tier1_since is None:
                self.tier1_since = time.time()
            elapsed = time.time() - self.tier1_since

            if not self.acknowledged and elapsed > self.ack_window_seconds:
                result["action"] = "ESCALATE_SOS"
            else:
                result["action"] = "NONE" if self.acknowledged else "WARN_USER"
            return result

        if result["tier"] == Tier.TIER_2:
            result["action"] = "ESCALATE_SOS"
            return result

    def acknowledge(self):
        self.acknowledged = True


if __name__ == "__main__":
    route = [(26.4499, 80.3319), (26.4550, 80.3400), (26.4600, 80.3480)]
    tracker = DeviationTracker(route, ack_window_seconds=5)
    print(tracker.update((26.4499, 80.3319)))
    print(tracker.update((26.4700, 80.3600)))