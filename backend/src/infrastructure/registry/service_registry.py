from typing import Dict
import threading
import time


class ServiceUnavailable(Exception):
    pass


class ServiceRegistry:
    def __init__(self, ttl: int = 30):
        self._services: Dict[str, Dict] = {}
        self._lock = threading.Lock()
        self.ttl = ttl  # tiempo máximo sin heartbeat

    def register(self, name: str, host: str, port: int):
        with self._lock:
            self._services[name] = {
                "host": host,
                "port": port,
                "last_seen": time.time(),
                "status": "UP"
            }

    def heartbeat(self, name: str):
        with self._lock:
            if name in self._services:
                self._services[name]["last_seen"] = time.time()
                self._services[name]["status"] = "UP"

    def get(self, name: str) -> Dict:
        service = self._services.get(name)
        if not service:
            raise ServiceUnavailable(f"Service {name} not registered")

        if time.time() - service["last_seen"] > self.ttl:
            service["status"] = "DOWN"
            raise ServiceUnavailable(f"Service {name} is DOWN")

        return service

    def unregister(self, name: str):
        with self._lock:
            self._services.pop(name, None)


service_registry = ServiceRegistry()
