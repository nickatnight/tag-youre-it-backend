import functools
import logging
from typing import Any, Callable

import asyncprawcore


logger = logging.getLogger(__name__)


# TODO: revisit this
def catch_apraw_and_log(func: Callable[..., Any]) -> Any:
    @functools.wraps(func)
    async def wrapper_catch_apraw_and_log(*args: str, **kwargs: int) -> Any:
        try:
            result: Any = await func(*args, **kwargs)
        except asyncprawcore.exceptions.RequestException as a_exc:
            logger.warning(a_exc, exc_info=True)
        except Exception as e:
            logger.warning(e, exc_info=True)
        else:
            return result
        return False

    return wrapper_catch_apraw_and_log
