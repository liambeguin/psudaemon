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

    @property
    def channels(self) -> List[common.Channel]:
        if self.commands.get_channels is None:
            raise HTTPException(status_code=501, detail=f'get_channels() command not defined for {self.name}')

        try:
            p = self._run(self.commands.get_channels)
            return [common.Channel(**ch, **self.flatten_psu_idn()) for ch in json.loads(p.stdout)]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail='unable to parse monitoring output')
