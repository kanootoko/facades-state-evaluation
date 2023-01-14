"""
Experimental performance boosting functions related to concurrency are defined here.
"""
import asyncio
import concurrent.futures
import itertools
from typing import Any, Callable, Iterable

import more_itertools


def inner_looping_function(function: Callable, params: Iterable[Any]) -> list[Any]:
    return [function(*p) for p in params]


async def map_in_process_pool_chunked(function: Callable, params: Iterable[Any], chunk_size: int = 1) -> list[Any]:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        futures = (
            loop.run_in_executor(pool, inner_looping_function, function, pr)
            for pr in more_itertools.ichunked(params, chunk_size)
        )
        return list(itertools.chain.from_iterable(await asyncio.gather(*futures)))


async def map_in_process_pool(function: Callable, params: Iterable[Any]) -> list[Any]:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        futures = [loop.run_in_executor(pool, function, *p) for p in params]
        return list(itertools.chain(await asyncio.gather(*futures)))
