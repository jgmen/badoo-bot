import redis
import pickle

class CacheManager:
    _instance = None

    def __init__(self, host="localhost", port=6379, db=0, ttl=3600):
        self.redis_client = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            decode_responses=False
        )
        self.default_ttl = ttl

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get(self, key):
        val = self.redis_client.get(key)
        if val and isinstance(val, bytes):
            try:
                return pickle.loads(val)
            except (pickle.UnpicklingError, EOFError, ValueError) as e:
                print(f"[CACHE] Error deserializing value: {e}")
        return None

    def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        try:
            self.redis_client.setex(key, ttl, pickle.dumps(value))
        except (pickle.PicklingError, ValueError) as e:
            print(f"[CACHE] Error serializing value: {e}")

    def delete(self, key):
        self.redis_client.delete(key)
