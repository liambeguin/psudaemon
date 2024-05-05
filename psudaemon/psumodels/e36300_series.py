import logging
import threading

from typing import Any, Dict, List, Literal, Union

import pyvisa

from pydantic import BaseModel, computed_field

from . import common

model_string = ('Keysight Technologies,E36313A', 'E36300')


class Endpoint:
    def __init__(self, ep):
        self.ep = ep
        self.lock = threading.Lock()

    def write(self, *args, **kwargs):
        self.lock.acquire()
        self.ep.write(*args, **kwargs)
        self.lock.release()

    def query(self, *args, **kwargs):
        self.lock.acquire()
        ret = self.ep.query(*args, **kwargs)
        self.lock.release()

        return ret


class E36300_Channel(BaseModel):
    index: int
    name: str
    psu: str
    model: Literal[model_string]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._ep = kwargs.get('_ep', None)

    @computed_field
    def current(self) -> float:
        return float(self._ep.query(f'meas:curr? (@{self.index})'))

    @computed_field
    def current_limit(self) -> float:
        return float(self._ep.query(f'curr? (@{self.index})'))

    @current_limit.setter
    def current_limit(self, current: Union[int, float]) -> Union[int, float]:
        self._ep.write(f'curr {current}, (@{self.index})')
        return current

    @computed_field
    def state(self) -> bool:
        return bool(int(self._ep.query(f'outp? (@{self.index})')))

    @state.setter
    def state(self, state: Union[bool]) -> bool:
        s = int(bool(state))
        self._ep.write(f'outp {s}, (@{self.index})')
        return s

    @computed_field
    def voltage(self) -> float:
        return float(self._ep.query(f'meas:volt? (@{self.index})'))

    @computed_field
    def voltage_limit(self) -> float:
        return float(self._ep.query(f'volt? (@{self.index})'))

    @voltage_limit.setter
    def voltage_limit(self, volt: Union[int, float]) -> Union[int, float]:
        self._ep.write(f'volt {volt}, (@{self.index})')
        return volt


class E36300_PSU(common.PSU):
    uri: str
    name: str
    model: Literal[model_string]
    visabackend: str = '@py'
    pyvisa_args: Dict[str, Any] = {}
    channel_indices: List[int] = [1, 2, 3]

    _channels: Dict[int, E36300_Channel] = {}
    _ep: Endpoint = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        try:
            self._ep = Endpoint(pyvisa.ResourceManager(
                self.visabackend).open_resource(
                    self.uri,
                    **self.pyvisa_args,
                ),
            )
        except OSError:
            logging.warning(f'unable to open {self.uri}')
            return

        idn = self._ep.query('*IDN?').strip()
        assert self.model in idn, f'got {idn}'

        f = ['manufacturer', 'model', 'serial', 'revision']
        self.idn = common.PSUIdn(**{f[i]: val for i, val in enumerate(idn.split(','))})

    @computed_field
    def channels(self) -> List[E36300_Channel]:
        if self._channels:
            return self._channels

        for i in self.channel_indices:
            self._channels[i] = E36300_Channel(
                index=i,
                name=f'CH{i}',
                psu=self.name,
                model=self.model,
                _ep=self._ep,
            )

        return self._channels

    @computed_field
    def online(self) -> bool:
        return self._ep is not None
