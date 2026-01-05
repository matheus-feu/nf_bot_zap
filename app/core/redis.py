from redis.asyncio import Redis

from app.core.config import settings

redis_client: Redis | None = None


async def get_redis_client() -> Redis:
	"""
	Dependency que fornece o cliente Redis.
	Uso: redis: Redis = Depends(get_redis)
	"""
	global redis_client

	if redis_client is None:
		redis_client = Redis.from_url(
			settings.cache_redis_uri,
			decode_responses=True,
		)

	return redis_client
