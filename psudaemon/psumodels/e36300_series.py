from typing import Literal

import pyvisa
import logging

from pydantic import BaseModel, computed_field

model_string = ['Keysight E36313A', 'E36300']


class E36300_Channel(BaseModel):
    index: int
    _model: Literal[*model_string] = model_string[0]


class E36300_PSU(BaseModel):
    uri: str
    name: str
    model: Literal[*model_string]

    _channel_count: int = 3
    _channel_names = ['CH1', 'CH2', 'CH3']
    _channels: list = []
    _ep: pyvisa.resources.Resource = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            self._ep = pyvisa.ResourceManager('@py').open_resource(self.uri)
        except OSError as e:
            logging.warning(f'unable to open {self.uri}')
            pass

    @computed_field
    def channels(self) -> list[E36300_Channel]:
        if self._channels:
            return self._channels

        for i in range(self._channel_count):
            self._channels.append(E36300_Channel(index=i))

        return self._channels

    @computed_field
    def active(self) -> bool:
        return self._ep is not None
