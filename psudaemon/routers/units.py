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


@router.get('/units/{psu}')
def get_psu(psu: str, units: Units) -> psumodels.Unit:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply


@router.get('/units/{psu}/channels')
def get_channel(psu: str, units: Units) -> List[psumodels.Channel]:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply.channels


@router.get('/units/{psu}/{ch}')
def get_channel(psu: str, ch: int, units: Units) -> psumodels.Channel:
    '''Show Power Supply Unit instance.'''
    supply, channel = helpers.check_user_input(units, psu, ch)
    return channel
