"""
Simple Token Bucket Rate Limiter
Prevents hitting Gemini API rate limits
"""

import time
from collections import deque
from threading import Lock
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Token bucket rate limiter for API requests

    Ensures we never exceed the specified rate limit by
    blocking requests when necessary.
    """

    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds (default: 60s = 1 minute)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.lock = Lock()

        logger.info(f"Rate limiter initialized: {max_requests} requests per {time_window}s")

    def wait_if_needed(self):
        """
        Block execution if making a request would exceed rate limit

        This method should be called BEFORE making an API request.
        It will automatically wait if needed to stay within limits.
        """
        with self.lock:
            now = time.time()

            # Remove old requests outside the time window
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()

            # Check if we're at the limit
            if len(self.requests) >= self.max_requests:
                # Calculate how long to wait
                oldest_request = self.requests[0]
                time_until_available = self.time_window - (now - oldest_request) + 1

                if time_until_available > 0:
                    logger.warning(
                        f"Rate limit reached ({len(self.requests)}/{self.max_requests}). "
                        f"Waiting {time_until_available:.1f}s..."
                    )
                    time.sleep(time_until_available)

                    # After waiting, recursively check again
                    # (in case other threads made requests)
                    return self.wait_if_needed()

            # Record this request
            self.requests.append(time.time())

            remaining = self.max_requests - len(self.requests)
            if remaining <= 3:
                logger.info(f"Rate limit: {len(self.requests)}/{self.max_requests} used, {remaining} remaining")

    def get_stats(self) -> dict:
        """Get current rate limiter statistics"""
        with self.lock:
            now = time.time()

            # Clean old requests
            while self.requests and self.requests[0] < now - self.time_window:
                self.requests.popleft()

            return {
                "requests_in_window": len(self.requests),
                "max_requests": self.max_requests,
                "window_seconds": self.time_window,
                "remaining": self.max_requests - len(self.requests),
                "utilization_percent": (len(self.requests) / self.max_requests) * 100
            }
