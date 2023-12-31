from __future__ import annotations

import logging

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from psudaemon import helpers, psumodels, types


class UnitResp(BaseModel):
    uri: str
    name: str
    model: str
    online: bool


router = APIRouter()
logger = logging.getLogger('uvicorn')


@router.get('/units')
def get_units(units: types.Units) -> List[UnitResp]:
    '''List all power supplies of this instance.'''
    return units.values()


@router.get('/units/{psu}')
def get_psu(psu: str, units: types.Units) -> psumodels.Unit:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply


@router.get('/units/{psu}/channels')
def get_psu_channels(psu: str, units: types.Units) -> Dict[int, psumodels.Channel]:
    '''Return all channels for a given power supply.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply.channels


@router.get('/units/{psu}/{ch}')
def get_psu_channel(psu: str, ch: int, units: types.Units) -> psumodels.Channel:
    '''Return a single channel for a given power supply.'''
    supply, channel = helpers.check_user_input(units, psu, ch)
    return channel


@router.post('/units/{psu}/{ch}')
def post_channel(
    psu: str,
    ch: int,
    units: types.Units,
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
