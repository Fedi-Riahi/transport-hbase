import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    r.ping()
    print("Redis connected")
except redis.ConnectionError:
    print("Redis not reachable — is the container running?")
    raise

def cache_bus_position(bus_id: str, lat: str, lng: str, status: str, ttl: int = 60):
    key = f"bus:position:{bus_id}"
    r.setex(key, ttl, json.dumps({
        "latitude": lat,
        "longitude": lng,
        "status": status
    }))

def get_cached_position(bus_id: str) -> dict | None:
    key = f"bus:position:{bus_id}"
    data = r.get(key)
    return json.loads(data) if data else None

def delete_cached_position(bus_id: str):
    r.delete(f"bus:position:{bus_id}")
