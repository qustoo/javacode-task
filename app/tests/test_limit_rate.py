import asyncio

import pytest
from httpx import AsyncClient


@pytest.fixture()
def num_requests():
    return 1000


@pytest.mark.asyncio
async def test_limit_rate(redis_connection, api_prefix, wallet_for_tests, constant_value, num_requests):
    url = f"{api_prefix}/wallets/{wallet_for_tests}/deposit"

    from main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        tasks = []

        for _ in range(num_requests + 1):
            tasks.append(client.post(url=url, json={"amount": constant_value}))

        # Send all requests concurrently
        responses = await asyncio.gather(*tasks)
        for i in range(num_requests):
            assert responses[i].status_code == 200

        # Error response
        final_response = responses[num_requests]
        assert final_response.status_code == 503

        new_resp = await client.post(url=url, json={"amount": constant_value})
        print(f'{new_resp=}')

