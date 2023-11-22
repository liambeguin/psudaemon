from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    uvicorn: Dict[str, Any] = {}
