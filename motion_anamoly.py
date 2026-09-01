import math
from collections import deque

WINDOW_SIZE = 10
IMPACT_THRESHOLD_G = 2.5
SUDDEN_STOP_DROP_G = 0.6
NORMAL_TRAVEL_MIN_G = 1.05


def magnitude(x, y, z):
    return math.sqrt(x * x + y * y + z * z)


class MotionAnomalyTracker:
    def __init__(self, window_size=WINDOW_SIZE):
        self.window = deque(maxlen=window_size)
        self.prev_avg = None

    def add_sample(self, x, y, z):
        mag = magnitude(x, y, z)
        self.window.append(mag)
        avg = sum(self.window) / len(self.window)

        result = None
        if mag > IMPACT_THRESHOLD_G:
            result = {"type": "IMPACT", "magnitude": round(mag, 2)}
        elif (
            self.prev_avg is not None
            and self.prev_avg > NORMAL_TRAVEL_MIN_G
            and (self.prev_avg - avg) > SUDDEN_STOP_DROP_G
        ):
            result = {"type": "SUDDEN_STOP", "magnitude": round(mag, 2)}

        self.prev_avg = avg
        return result


if __name__ == "__main__":
    tracker = MotionAnomalyTracker()
    normal_samples = [(0.1, 0.05, 1.1)] * 10
    stop_samples = [(0.0, 0.0, 0.2)] * 3

    for x, y, z in normal_samples + stop_samples:
        r = tracker.add_sample(x, y, z)
        if r:
            print("Anomaly detected:", r)