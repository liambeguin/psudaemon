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
