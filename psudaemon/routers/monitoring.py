from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from psudaemon import types, psumodels

router = APIRouter()


@router.get('/monitoring/channels')
def get_channels(units: types.Units) -> List[psumodels.common.Channel]:
    '''List all power supply channels of this instance.'''
    ret = []
    for psu in units.values():
        ret.extend(psu.monitoring())

    return ret
