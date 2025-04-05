import time
import redis
from fastapi import Depends, HTTPException, status, Request

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Configuration
SECONDS_PER_DAY = 86400

def rate_limit_dependency(user_id: str, user_quota: int = 100):
    key = f"user_quota:{user_id}"
    current = redis_client.get(key)

    if current is None:
        # First request of the day
        redis_client.set(key, 1, ex=SECONDS_PER_DAY)
    else:
        count = int(current)
        if count >= user_quota:
            raise HTTPException(status_code=429, detail="Daily quota exceeded.")
        redis_client.incr(key)
