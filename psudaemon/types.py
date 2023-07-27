from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')

    port: int
    log_level: str = 'info'
