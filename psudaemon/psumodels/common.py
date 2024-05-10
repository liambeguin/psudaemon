from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, computed_field


class PSUIdn(BaseModel):
    manufacturer: Optional[str]=Field(default=None)
    model: Optional[str]=Field(default=None)
    serial: Optional[str]=Field(default=None)
    revision: Optional[str]=Field(default=None)


class Channel(ABC, BaseModel):
    index: int=Field(description='Channel index')
    name: str=Field(description='Channel name')

    # injected by PSU
    psu_name: str=Field(description='PSU name')
    psu_idn_manuf:    Optional[str]=Field(default=None)
    psu_idn_model:    Optional[str]=Field(default=None)
    psu_idn_serial:   Optional[str]=Field(default=None)
    psu_idn_revision: Optional[str]=Field(default=None)

    @abstractmethod
    @computed_field(description='Channel instantaneous current measurement')
    def current(self) -> float:
        raise NotImplementedError(f'{self.name}: common.Channel.current')

    @abstractmethod
    @computed_field(description='Channel current limit')
    def current_limit(self) -> float:
        ...

    @abstractmethod
    @current_limit.setter
    def current_limit(self, current: Union[int, float]) -> Union[int, float]:
        ...

    @abstractmethod
    @computed_field(description='Channel present state')
    def state(self) -> bool:
        raise NotImplementedError(f'{self.name}: common.Channel.state')

    @abstractmethod
    @state.setter
    def state(self, state: Union[bool]) -> bool:
        ...

    @abstractmethod
    @computed_field(description='Channel instantaneous voltage measurement')
    def voltage(self) -> float:
        raise NotImplementedError(f'{self.name}: common.Channel.voltage')

    @abstractmethod
    @computed_field(description='Channel voltage limit')
    def voltage_limit(self) -> float:
        ...

    @abstractmethod
    @voltage_limit.setter
    def voltage_limit(self, volt: Union[int, float]) -> Union[int, float]:
        ...


class PSU(BaseModel):
    name: str=Field(description='PSU pretty name')
    model: str=Field(desciption='PSU model, used to infer psudaemon class')

    uri: Optional[str]=Field(default=None)
    idn: Optional[PSUIdn]=Field(description='PSU identification dict', default=None)

    @computed_field
    def online(self) -> bool:
        raise NotImplementedError(f'{self.name}: common.PSU.online')

    @computed_field
    def channels(self) -> List[Channel]:
        raise NotImplementedError(f'{self.name}: common.PSU.channels')

    def flatten_psu_idn(self) -> Dict[str, str]:
        ret = { 'psu_name': self.name }
        for k, v in self.idn.model_dump().items():
            ret[f'psu_idn_{k}'] = v
        return ret

    def monitoring(self):
        ret = []
        for channel in self.channels:
            c = channel.model_dump()
            c.update(self.flatten_psu_idn())
            ret.append(c)
        return ret
