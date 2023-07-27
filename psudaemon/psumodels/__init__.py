from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from . import e36300_series

Unit = Annotated[Union[
    e36300_series.E36300_PSU,
], Field(discriminator='model')]


Channel = Annotated[Union[
    e36300_series.E36300_Channel,
], Field(discriminator='_model')]

