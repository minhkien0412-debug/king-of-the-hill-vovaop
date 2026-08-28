import asyncio
import time
from typing import Callable, Any

class TargetRequestGate:
    def __init__(self, requests_per_sec: int = 30):
        self.capacity: int = requests_per_sec
        self.tokens: float = float(requests_per_sec)
        self.last_update: float = time.time()
        self.lock: asyncio.Lock = asyncio.Lock()
        self.latency_window: list[float] = []

    async def consume_token(self) -> bool:
        async with self.lock:
            now: float = time.time()
            elapsed: float = now - self.last_update
            self.tokens = min(float(self.capacity), self.tokens + (elapsed * self.capacity))
            self.last_update = now
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

    async def execute(self, task_id: str, async_coro: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        while not await self.consume_token():
            await asyncio.sleep(0.005)
        start: float = time.time()
        try:
            result = await async_coro(*args, **kwargs)
            latency = time.time() - start
            self.latency_window.append(latency)
            if len(self.latency_window) > 50: 
                self.latency_window.pop(0)
            return result
        except Exception:
            return None

    def get_adaptive_delay(self) -> float:
        return sum(self.latency_window) / len(self.latency_window) if self.latency_window else 0.02
