from typing import Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from .psumodels import e36300_series


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')

    port: int
    log_level: str = 'info'


Unit = Annotated[Union[
    e36300_series.E36300_PSU,
], Field(discriminator='model')]


Channel = Annotated[Union[
    e36300_series.E36300_Channel,
], Field(discriminator='_model')]

