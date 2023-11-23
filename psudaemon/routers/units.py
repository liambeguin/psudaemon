from __future__ import annotations

import logging

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated

from psudaemon import context, helpers, psumodels

Units = Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]


router = APIRouter()
logger = logging.getLogger('uvicorn')


@router.get('/units')
def get_units(units: Units) -> List[Dict[str, Any]]:
    '''List all power supplies of this instance.'''
    ret = []
    for psu in units.values():
        for channel in psu.channels.values():
            c = channel.model_dump()
            c.update({
                'psu': psu.name,
                'online': psu.online,
                'idn': psu.idn,
            })
            ret.append(c)

    return ret


@router.get('/units/{psu}')
def get_psu(psu: str, units: Units) -> psumodels.Unit:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply


@router.get('/units/{psu}/channels')
def get_psu_channels(psu: str, units: Units) -> Dict[int, psumodels.Channel]:
    '''Return all channels for a given power supply.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply.channels


@router.get('/units/{psu}/{ch}')
def get_psu_channel(psu: str, ch: int, units: Units) -> psumodels.Channel:
    '''Return a single channel for a given power supply.'''
    supply, channel = helpers.check_user_input(units, psu, ch)
    return channel


@router.post('/units/{psu}/{ch}')
def post_channel(
    psu: str,
    ch: int,
    units: Units,
    state: Optional[bool] = None,
    current_limit: Optional[float] = None,
    voltage_limit: Optional[float] = None) -> psumodels.Channel:
    '''Configure a single channel for a given power supply.'''

    supply, channel = helpers.check_user_input(units, psu, ch)

    if current_limit is not None:
        was = channel.current_limit
        channel.current_limit = current_limit
        logger.info(f'setting {psu}/{ch} current limit to {current_limit} (was: {was})')

    if voltage_limit is not None:
        was = channel.voltage_limit
        channel.voltage_limit = voltage_limit
        logger.info(f'setting {psu}/{ch} voltage limit to {voltage_limit} (was: {was})')

    if state is not None:
        was = channel.state
        channel.state = state
        logger.info(f'setting {psu}/{ch} state to {state} (was: {was})')

    return supply.channels[ch]
