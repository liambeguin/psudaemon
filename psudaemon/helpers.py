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
    if ch is not None and ch not in units[psu].channel_indices:
        raise HTTPException(status_code=404, detail=f'channel out of range: {ch} not in {units[psu].channel_indices}')

    psu = units[psu]
    ch = psu.channels[ch] if ch is not None else None

    return psu, ch
