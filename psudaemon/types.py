from typing import Union

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')

    port: int
    log_level: str = 'info'
