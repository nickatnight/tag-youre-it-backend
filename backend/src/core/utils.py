import inspect
import logging
from datetime import datetime, timezone

from pydantic import BaseModel as DanticBaseModel

from src.core.const import TAG_TIME


logger = logging.getLogger(__name__)


def is_tag_time_expired(tag_time: datetime) -> bool:
    tag_over_time: int = int((datetime.now(timezone.utc) - tag_time).total_seconds())

    return tag_over_time > TAG_TIME


# https://github.com/pydantic/pydantic/issues/1223
def optional(*fields):  # type: ignore
    def dec(_cls):  # type: ignore
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls

    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], DanticBaseModel):
        cls = fields[0]
        fields = cls.__fields__  # type: ignore
        return dec(cls)  # type: ignore
    return dec
