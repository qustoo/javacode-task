import logging
import time
from contextlib import asynccontextmanager

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_limiter import FastAPILimiter

from api import wallet_router
from consts import WINDOW_SIZE, RPS_LIMIT
from core.config import settings
from core.database.helper import database_helper
from core.models.base import Base

logging.basicConfig(
    level=settings.logging.status[settings.logging.level],
    format=settings.logging.format,
)


# lifespan, create models in database
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with database_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await FastAPILimiter.init(redis_connection)

    yield

    async with database_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await database_helper.dispose()
    await FastAPILimiter.close()


redis_connection = redis.from_url(f"redis://{settings.redis.service}:{settings.redis.port}", encoding="utf8")
app = FastAPI(lifespan=lifespan)


# handler request errors
@app.exception_handler(RequestValidationError)
async def exception_request_error(_, exc):
    response_body = jsonable_encoder(
        {"detail": f"Invalid input request data.Try again with valid data.Error = {str(exc)}"})

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response_body)


# handler many requests
@app.exception_handler(HTTPException)
async def exception_to_many_requests(_, exc):
    if exc.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Rate limit exceeded. Please try again later."},
        )
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": "Invalid request or response data"})


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    is_deposit_or_withdraw_operation = str(request.url).split('/')[-1] in ('deposit', 'withdraw')

    if not is_deposit_or_withdraw_operation:
        return await call_next(request)

    wallet_id = request.path_params.get("wallet_uuid")
    if not wallet_id:
        return await call_next(request)

    current_time = int(time.time())
    key = f"rps:{wallet_id}:{current_time}"

    # Увеличиваем счетчик запросов
    redis_connection.incr(key)

    # Устанавливаем время жизни ключа в окно времени
    redis_connection.expire(key, WINDOW_SIZE)

    # Получаем общее количество запросов за текущее окно
    total_requests = sum(
        int(redis_connection.get(f"rps:{wallet_id}:{current_time - i}") or 0) for i in range(WINDOW_SIZE))

    # Если превышен лимит, отклоняем запрос
    if total_requests > RPS_LIMIT:
        logging.error("Get rate limit.")
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

    response = await call_next(request)
    return response


app.include_router(wallet_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
