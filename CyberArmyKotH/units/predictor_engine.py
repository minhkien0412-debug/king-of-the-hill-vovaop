import numpy as np
import time

class KotHTickPredictor:
    def __init__(self, window_size: int = 10):
        self.window_size: int = window_size
        self.timestamps: list[float] = []
        self.estimated_period: float = 60.0

    def register_tick(self) -> None:
        self.timestamps.append(time.time())
        if len(self.timestamps) > self.window_size: 
            self.timestamps.pop(0)
        if len(self.timestamps) >= 2:
            diffs = np.diff(self.timestamps)
            if len(diffs) > 0:
                self.estimated_period = float(np.median(diffs))

    def get_seconds_until_next_tick(self) -> float:
        if not self.timestamps: 
            return 5.0
        return self.estimated_period - ((time.time() - self.timestamps[-1]) % self.estimated_period)

    def should_activate_burst(self, network_latency: float) -> bool:
        return self.get_seconds_until_next_tick() <= (network_latency * 4)
