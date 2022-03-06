from typing import Any, Awaitable, Callable, Concatenate, ParamSpec
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)
from queen_api.config import Config
import asyncio

queryParams = ParamSpec("queryParams")


class QueryHandler:
    def __init__(self, conf: Config) -> None:
        self.__client = AsyncIOMotorClient(
            host=conf.DB_HOST, port=conf.DB_PORT, username="root", password="example"
        )
        self.__client.get_io_loop = asyncio.get_running_loop

    async def handle(
        self,
        query: Callable[
            Concatenate[AsyncIOMotorClientSession, AsyncIOMotorDatabase, queryParams],
            Awaitable[Any],
        ],
        *args: queryParams.args,
        **kwargs: queryParams.kwargs,
    ):
        print(f"starting sesh in loop {asyncio.get_running_loop()}")
        async with await self.__client.start_session() as sesh:
            print(f"received {query=}")
            return sesh.with_transaction(lambda s: query(s, *args, **kwargs))

    # TODO: validate query
    # TODO: document
    # TODO: logging!!!!!