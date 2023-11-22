from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing_extensions import Annotated

from psudaemon import context, helpers, psumodels

Units = Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]

class UnitResp(BaseModel):
    uri: str
    name: str
    model: str
    online: bool


router = APIRouter()


@router.get('/units')
def get_units(units: Units) -> List[UnitResp]:
    '''List all Power Supply Units in the instance.'''
    return units.values()


@router.get('/units/{name}')
def get_psu(name: str, units: Units) -> psumodels.Unit:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, name)
    return supply


@router.get('/units/{name}/channels')
def get_channel(name: str, units: Units) -> List[psumodels.Channel]:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, name)
    return supply.channels


@router.get('/units/{name}/{channel}')
def get_channel(name: str, channel: int, units: Units) -> psumodels.Channel:
    '''Show Power Supply Unit instance.'''
    supply, channel = helpers.check_user_input(units, name, channel)
    return channel
