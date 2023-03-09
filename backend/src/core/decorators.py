# import logging
# from typing import Any, Callable

# import asyncprawcore
# from result import Result, Ok, Err


# logger = logging.getLogger(__name__)


# class CatchAsyncPraw:
#     """generic catch handler for methods using asyncpraw"""
#     def __init__(self, function: Callable[..., Any]) -> None:
#         self.function = function

#     def __call__(self, *args: str, **kwargs: Any) -> Result[Any, str]:
#         try:
#             result: Any = self.function(*args, **kwargs)
#         except asyncprawcore.exceptions.RequestException as a_exc:
#             logger.error(a_exc, exc_info=True)
#             return Err(str(a_exc))
#         except Exception as e:
#             logger.error(e, exc_info=True)
#             return Err(f"Unknown error occurred: {e}")
#         else:
#             return Ok(result)
