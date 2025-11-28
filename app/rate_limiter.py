"""
Naive sliding-window rate limiter (no external libs).
- KEY: client identifier (API key or IP)
- LIMIT: N requests per WINDOW seconds
"""
import time
from collections import deque
from threading import Lock
from typing import Deque, Dict

class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self._buckets: Dict[str, Deque[float]] = {}
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = time.time()
        with self._lock:
            q = self._buckets.setdefault(key, deque())
            # drop stale
            cutoff = now - self.window
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= self.limit:
                return False
            q.append(now)
            return True

# Global limiter: tweak as needed
GLOBAL_LIMITER = SlidingWindowLimiter(limit=30, window_seconds=60)  # 30 req / 60s per client
