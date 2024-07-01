import asyncio
from typing import Optional


class AsyncTimedIterable:
    def __init__(self, iterable, timeout: Optional[int] = None):
        class AsyncTimedIterator:
            def __init__(self):
                self._iterator = iterable.__aiter__()

            async def __anext__(self):
                try:
                    result = await asyncio.wait_for(
                        self._iterator.__anext__(), timeout=timeout
                    )
                    return result
                except asyncio.TimeoutError as e:
                    raise e

        self._factory = AsyncTimedIterator

    def __aiter__(self):
        return self._factory()
