from __future__ import annotations

from typing import List

from fastapi import APIRouter

from psudaemon import types

router = APIRouter()


@router.get('/monitoring/channels')
def get_channels(units: types.Units) -> List[types.ChannelModel]:
    '''List all power supply channels of this instance.'''
    ret = []
    for psu in units.values():
        ret.extend(psu.monitoring())

    return ret
