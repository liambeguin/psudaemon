from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from psudaemon import types

router = APIRouter()


@router.get('/monitoring/channels')
def get_channels(units: types.Units) -> List[Dict[str, Any]]:
    '''List all power supply channels of this instance.'''
    ret = []
    for psu in units.values():
        for channel in psu.channels.values():
            c = channel.model_dump()
            c.update({
                'name': psu.name,
                'online': psu.online,
                'idn': psu.idn,
            })
            ret.append(c)

    return ret
