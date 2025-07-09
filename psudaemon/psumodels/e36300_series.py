import logging
import threading
import os

from typing import Any, Dict, List, Literal, Union

import pyvisa

from pydantic import computed_field

from . import common

model_string = (
    'E36300',
    'Keysight Technologies,E36312A',
    'Keysight Technologies,E36313A',
)


class Endpoint:
    def __init__(self, ep):
        self._lock = threading.Lock()
        self._ep = ep
        self._uri = ep.resource_name
        self._rm = pyvisa.ResourceManager()
        self._reconnect_attempted = False

    def _reconnect(self):
        try:
            self._ep.close()
        except Exception:
            pass

        try:
            self._ep = self._rm.open_resource(self._uri)
            self._reconnect_attempted = False
            logging.warning(f"[psudaemon] Reconnected to VISA device: {self._uri}")
        except Exception as e:
            logging.error(f"[psudaemon] VISA reconnection failed: {e}")
            logging.warning("[psudaemon] Crashing service to trigger systemd restart...")
            os._exit(1)  

    def write(self, *args, **kwargs):
        with self._lock:
            try:
                self._ep.write(*args, **kwargs)
            except Exception as e:
                logging.error(f"[psudaemon] VISA write failed: {e}")
                if not self._reconnect_attempted:
                    self._reconnect_attempted = True
                    self._reconnect()
                    return self.write(*args, **kwargs)
                raise

    def query(self, *args, **kwargs):
        with self._lock:
            try:
                return self._ep.query(*args, **kwargs)
            except Exception as e:
                logging.error(f"[psudaemon] VISA query failed: {e}")
                if not self._reconnect_attempted:
                    self._reconnect_attempted = True
                    self._reconnect()
                    return self.query(*args, **kwargs)
                raise


class E36300_Channel(common.Channel):
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

    _channels: List[E36300_Channel] = []
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
            try:
                name = self.channel_data[i].name
            except Exception:
                name=f'CH{i}'

            self._channels.append(E36300_Channel(
                index=i,
                name=name,
                psu_name=self.name,
                _ep=self._ep,
            ))

        return self._channels

    @computed_field
    def online(self) -> bool:
        return self._ep is not None
