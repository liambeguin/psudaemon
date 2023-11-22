from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from typing_extensions import Annotated

from .. import context, types
from .. import psumodels


class UnitResp(BaseModel):
    uri: str
    name: str
    model: str
    enabled: bool


router = APIRouter()


@router.get('/units')
def get_units(units: Annotated[List[psumodels.Unit], Depends(context.load_units)]) -> List[UnitResp]:
    '''List all Power Supply Units in the instance.'''
    return units
