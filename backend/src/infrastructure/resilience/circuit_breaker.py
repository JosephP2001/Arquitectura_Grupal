import time
from functools import wraps

from src.infrastructure.resilience.exceptions import CircuitBreakerOpen
from src.infrastructure.observability.logger import get_logger


logger = get_logger("circuit_breaker")


class CircuitBreaker:
    def __init__(self, fail_max: int = 3, reset_timeout: int = 30):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Circuit OPEN → bloquear llamadas
            if self.state == "OPEN":
                elapsed = time.time() - self.last_failure_time

                if elapsed > self.reset_timeout:
                    self.state = "HALF_OPEN"
                    logger.info(
                        "Circuit breaker HALF_OPEN",
                        extra={
                            "extra": {
                                "state": self.state,
                                "reset_timeout": self.reset_timeout,
                            }
                        },
                    )
                else:
                    logger.warning(
                        "Circuit breaker OPEN - call blocked",
                        extra={
                            "extra": {
                                "state": self.state,
                                "failures": self.failures,
                            }
                        },
                    )
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

        logger.warning(
            "Circuit breaker failure",
            extra={
                "extra": {
                    "failures": self.failures,
                    "state": self.state,
                    "fail_max": self.fail_max,
                }
            },
        )

        if self.failures >= self.fail_max:
            self.state = "OPEN"
            logger.error(
                "Circuit breaker OPEN",
                extra={
                    "extra": {
                        "state": self.state,
                        "failures": self.failures,
                    }
                },
            )

    def _reset(self):
        if self.state != "CLOSED":
            logger.info(
                "Circuit breaker reset to CLOSED",
                extra={
                    "extra": {
                        "previous_state": self.state,
                    }
                },
            )

        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = None
