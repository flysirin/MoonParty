from aiogram.fsm.storage.redis import Redis, RedisStorage

# Initialize  Redis storage
redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)

