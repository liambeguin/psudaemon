from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SettingsUvicorn(BaseModel):
    port: int
    log_level: str = 'info'
    timeout_keep_alive: Optional[int]


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    uvicorn: SettingsUvicorn
