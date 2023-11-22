from typing import Literal, List

import pyvisa
import logging

from pydantic import BaseModel, computed_field


model_string = ('Keysight Technologies,E36313A', 'E36300')


class E36300_Channel(BaseModel):
    index: int
    model: Literal[model_string]


class E36300_PSU(BaseModel):
    uri: str
    name: str
    model: Literal[model_string]
    visabackend: str = '@py'

    _channel_count: int = 3
    _channel_names = ['CH1', 'CH2', 'CH3']
    _channels: List[E36300_Channel] = []
    _ep: pyvisa.resources.Resource = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            self._ep = pyvisa.ResourceManager(self.visabackend).open_resource(self.uri, write_termination='\n', read_termination='\n')
        except OSError as e:
            logging.warning(f'unable to open {self.uri}')
            return

        idn = self._ep.query('*IDN?').strip()
        assert self.model in idn, f'got {idn}'

    @computed_field
    def channels(self) -> List[E36300_Channel]:
        if self._channels:
            return self._channels

        for i in range(self._channel_count):
            self._channels.append(E36300_Channel(index=i, model=self.model))

        return self._channels

    @computed_field
    def enabled(self) -> bool:
        return self._ep is not None
