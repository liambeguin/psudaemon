from __future__ import annotations
from typing import Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from typing_extensions import Annotated

from .. import context, helpers, psumodels


class UnitResp(BaseModel):
    uri: str
    name: str
    model: str
    online: bool


router = APIRouter()


@router.get('/units')
def get_units(units: Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]) -> List[UnitResp]:
    '''List all Power Supply Units in the instance.'''
    return units.values()


@router.get("/units/{name}")
def get_psu(name: str, units: Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]) -> psumodels.Unit:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, name)
    return supply


@router.get("/units/{name}/{channel}")
def get_channel(name: str, channel: int, units: Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]) -> psumodels.Channel:
    '''Show Power Supply Unit instance.'''
    supply, channel = helpers.check_user_input(units, name, channel)
    return channel
