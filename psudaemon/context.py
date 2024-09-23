from __future__ import annotations

import os

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, parse_obj_as
from ruamel.yaml import YAML

from . import psumodels


class Settings(BaseModel):
    model_config = ConfigDict(extra='forbid')
    uvicorn: Dict[str, Any] = {}


class Conffile():
    def __init__(self):
        self.yaml = YAML()
        conf = Path().parent / 'conf/psudaemon.yaml'
        self.path = Path(os.getenv('PSUDAEMON_CONF', conf.as_posix()))

    def read(self) -> dict:
        with self.path.open(encoding='utf-8') as f:
            return self.yaml.load(f.read())

    def update(self, units: dict) -> dict:
        conf = self.read()

        new_conf = {}
        new_conf['settings'] = conf['settings']
        new_conf['units'] = []

        for u in units.values():
            channel_data = {}
            for c in u.channels:
                channel_data[c.index] = dict(
                    name=c.name,
                    current_limit=c.current_limit,
                    voltage_limit=c.voltage_limit,
                )

            new_conf['units'].append(dict(
                name=u.name,
                model=u.model,
                uri=u.uri,
                pyvisa_args=u.pyvisa_args,
                channel_data=channel_data,
            ))

        return new_conf

    def write(self, data: dict) -> None:
        with self.path.open('w', encoding='utf-8') as f:
            self.yaml.dump(data, f)


def load_settings() -> Settings:
    '''Load settings from file.'''
    data = Conffile().read()
    return Settings(**data['settings'])


@lru_cache
def load_units() -> Dict[str, psumodels.Unit]:
    '''Load unit configuration from file.'''
    data = Conffile().read()

    # rekey for easy access
    units = {k['name']: k for k in data['units']}

    return parse_obj_as(Dict[str, psumodels.Unit], units)
