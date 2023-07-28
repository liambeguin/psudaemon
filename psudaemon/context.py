import os

from functools import lru_cache
from pathlib import Path

from pydantic import parse_obj_as
from ruamel.yaml import YAML

from . import psumodels, types


def _read_conffile() -> dict:
    yaml = YAML()
    conf = Path().parent / 'conf/psudaemon.yaml'
    path = Path(os.getenv('PSUDAEMON_CONF', conf.as_posix()))

    with path.open(encoding='utf-8') as f:
        return yaml.load(f.read())


def load_settings() -> types.Settings:
    '''Load settings from file.'''
    data = _read_conffile()
    return types.Settings(**data['settings'])


@lru_cache
def load_units() -> list[psumodels.Unit]:
    '''Load unit configuration from file.'''
    data = _read_conffile()
    return parse_obj_as(list[psumodels.Unit], list(data['units']))