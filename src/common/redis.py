from redis.asyncio import Redis


redis_client = Redis(
    host="localhost",      # замените на ваш хост
    port=6379,             # замените на ваш порт
    db=0,                  # замените на ваш Redis DB index
    decode_responses=True  # чтобы r.get возвращал str, а не bytes
)