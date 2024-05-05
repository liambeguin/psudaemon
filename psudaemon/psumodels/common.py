import abc

from typing import Dict, Optional

from pydantic import BaseModel, Field, computed_field


class PSUIdn(BaseModel):
    manufacturer: Optional[str]=Field(default=None)
    model: Optional[str]=Field(default=None)
    serial: Optional[str]=Field(default=None)
    revision: Optional[str]=Field(default=None)


class Channel(BaseModel):
    index: int=Field(description='Channel index')
    name: str=Field(description='Channel name')

    state: bool=Field(description='Channel present state')

    current: float=Field(description='Channel instantaneous current measurement')
    current_limit: float=Field(description='Channel current limit')

    voltage: float=Field(description='Channel instantaneous voltage measurement')
    voltage_limit: float=Field(description='Channel voltage limit')

    # injected in monitoring()
    psu_name: str=Field(description='PSU name', alias='psu.name', serialization_alias='psu.name')
    psu_idn_manuf:    Optional[str]=Field(default=None, alias='psu.idn.manufacturer', serialization_alias='psu.idn.manufacturer')
    psu_idn_model:    Optional[str]=Field(default=None, alias='psu.idn.model',        serialization_alias='psu.idn.model')
    psu_idn_serial:   Optional[str]=Field(default=None, alias='psu.idn.serial',       serialization_alias='psu.idn.serial')
    psu_idn_revision: Optional[str]=Field(default=None, alias='psu.idn.revision',     serialization_alias='psu.idn.revision')


class PSU(BaseModel, abc.ABC):
    name: str=Field(description='PSU pretty name')
    model: str=Field(desciption='PSU model, used to infer psudaemon class')

    uri: Optional[str]=Field(default=None)
    idn: Optional[PSUIdn]=Field(description='PSU identification dict', default=None)

    @computed_field
    @abc.abstractmethod
    def online(self) -> bool:
        pass

    @computed_field
    @abc.abstractmethod
    def channels(self) -> Dict[int, Channel]:
        pass

    def flatten_psu_idn(self) -> Dict[str, str]:
        ret = {
            'psu.name': self.name,
        }
        for k, v in self.idn.model_dump().items():
            ret[f'psu.idn.{k}'] = v
        return ret

    def monitoring(self):
        ret = []
        for channel in self.channels:
            c = channel.model_dump()
            c.update(self.flatten_psu_idn())
            ret.append(c)
        return ret
