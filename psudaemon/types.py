from __future__ import annotations

from typing import Dict, Optional

from fastapi import Depends
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from psudaemon import context, psumodels

Units = Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]


class ChannelModel(BaseModel):
    '''Channel Serializer'''
    model_config = ConfigDict(extra='ignore')

    index: int=Field(description='Channel index')
    name: str=Field(description='Channel name')
    psu_name: str=Field(description='PSU name', serialization_alias='psu.name')

    state: bool=Field(description='Channel present state')

    current: float=Field(description='Channel instantaneous current measurement')
    voltage: float=Field(description='Channel instantaneous voltage measurement')

    current_limit: Optional[float]=Field(default=None, description='Channel current limit')
    voltage_limit: Optional[float]=Field(default=None, description='Channel voltage limit')

    psu_idn_manuf:    Optional[str]=Field(default=None, serialization_alias='psu.idn.manufacturer')
    psu_idn_model:    Optional[str]=Field(default=None, serialization_alias='psu.idn.model')
    psu_idn_serial:   Optional[str]=Field(default=None, serialization_alias='psu.idn.serial')
    psu_idn_revision: Optional[str]=Field(default=None, serialization_alias='psu.idn.revision')


class PSUModel(BaseModel):
    model_config = ConfigDict(extra='ignore')

    name: str=Field(description='PSU pretty name')
    model: str=Field(desciption='PSU model, used to infer psudaemon class')

    uri: Optional[str]=Field(default=None)
    online: Optional[bool]=Field(default=None)
