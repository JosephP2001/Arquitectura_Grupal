import time
from functools import wraps
from src.infrastructure.resilience.exceptions import CircuitBreakerOpen


class CircuitBreaker:
    def __init__(self, fail_max=3, reset_timeout=30):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.reset_timeout:
                    self.state = "HALF_OPEN"
                else:
                    raise CircuitBreakerOpen()

            try:
                result = func(*args, **kwargs)
                self._reset()
                return result
            except Exception:
                self._record_failure()
                raise

        return wrapper

    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.fail_max:
            self.state = "OPEN"

    def _reset(self):
        self.failures = 0
        self.state = "CLOSED"
