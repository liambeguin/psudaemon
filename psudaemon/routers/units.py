from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from typing_extensions import Annotated

from .. import context, types



class UnitResp(BaseModel):
    uri: str
    name: str
    model: str
    active: bool


router = APIRouter()


@router.get('/units')
def get_units(units: Annotated[list[types.Unit], Depends(context.load_units)]) -> list[UnitResp]:
    '''List all Power Supply Units in the instance.'''
    return units
