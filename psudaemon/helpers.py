from __future__ import annotations

from typing import Optional, Tuple, Union

from fastapi import HTTPException

from . import psumodels


def check_user_input(
    units: dict[str, psumodels.Unit],
    psu: str,
    ch: Optional[Union[int, None]] = None) -> Tuple[psumodels.Unit, psumodels.common.Channel]:
    '''Further validate user inputs.'''
    if psu not in units:
        raise HTTPException(status_code=404, detail='undefined psu')

    psu = units[psu]
    chan = psu.get_channel(ch)

    if ch is not None and chan is None:
        raise HTTPException(status_code=404, detail=f'psu {psu.name} has no channel {ch}')

    return psu, chan
