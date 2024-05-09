from __future__ import annotations

from typing import Optional, Tuple, Union

from fastapi import HTTPException

from . import psumodels


def check_user_input(
    units: dict[str, psumodels.Unit],
    psu: str,
    ch: Optional[Union[int, None]] = None) -> Tuple[psumodels.Unit, psumodels.Channel]:
    '''Further validate user inputs.'''
    if psu not in units:
        raise HTTPException(status_code=404, detail='undefined psu')
    if ch is not None and ch not in range(len(units[psu].channels)):
        raise HTTPException(status_code=404, detail=f'channel out of range: {ch} not in range({len(units[psu].channels)})')

    psu = units[psu]

    if ch is None:
        return psu, None

    for chan in psu.channels:
        if ch == chan.index:
            ch = chan
            ch.psu_name = psu.name
            return psu, ch

    # should never reach this
    raise HTTPException(status_code=404, detail=f'channel out of range: {ch} not in range({len(units[psu].channels)})')
