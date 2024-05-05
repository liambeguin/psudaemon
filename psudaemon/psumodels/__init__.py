from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from . import e36300_series
from . import external

Unit = Annotated[Union[
    e36300_series.E36300_PSU,
    external.ExternalPSU,
], Field(discriminator='model')]
