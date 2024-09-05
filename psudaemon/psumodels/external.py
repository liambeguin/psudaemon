import json
import subprocess

from typing import List, Literal, Optional

from fastapi import HTTPException
from pydantic import BaseModel, Field, computed_field

from . import common

model_string = ('external')


class Commands(BaseModel):
    ping: Optional[str]=Field(description="command to make ping the external PSU to make sure it's online", default=None)
    get_channels: Optional[str]=Field(description='command to get all channels', default=None)


class ExternalChannel(common.Channel):
    raw: dict=Field(exclude=True)

    @computed_field
    def current(self) -> float:
        return self.raw['current']

    @computed_field
    def state(self) -> bool:
        return self.raw['state']

    @computed_field
    def voltage(self) -> float:
        return self.raw['voltage']


class ExternalPSU(common.PSU):
    model: Literal[model_string]
    commands: Commands

    def _run(self, cmd: str) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, shell=True, capture_output=True, check=False)

    @computed_field
    def online(self) -> bool:
        if self.commands.ping is None:
            return True

        return self._run(self.commands.ping).returncode

    @computed_field
    def channels(self) -> List[ExternalChannel]:
        if self.commands.get_channels is None:
            raise HTTPException(status_code=501, detail=f'get_channels() command not defined for {self.name}')

        try:
            p = self._run(self.commands.get_channels)
            return [ExternalChannel(raw=ch, **ch, **self.flatten_psu_idn()) for ch in json.loads(p.stdout)]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'unable to parse monitoring output: {p}')
