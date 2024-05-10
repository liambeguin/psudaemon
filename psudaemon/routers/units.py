from __future__ import annotations

import logging

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from psudaemon import helpers, types

router = APIRouter()
logger = logging.getLogger('uvicorn')


@router.get('/units')
def get_units(units: types.Units) -> List[types.PSUModel]:
    '''List all power supplies of this instance.'''
    return units.values()


@router.get('/units/{psu}')
def get_psu(psu: str, units: types.Units) -> types.PSUModel:
    '''Show Power Supply Unit instance.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply


@router.get('/units/{psu}/channels')
def get_psu_channels(psu: str, units: types.Units) -> List[types.ChannelModel]:
    '''Return all channels for a given power supply.'''
    supply, _ = helpers.check_user_input(units, psu)
    return supply.channels


@router.get('/units/{psu}/{ch}')
def get_psu_channel(psu: str, ch: int, units: types.Units) -> types.ChannelModel:
    '''Return a single channel for a given power supply.'''
    supply, channel = helpers.check_user_input(units, psu, ch)
    return channel


@router.post('/units/{psu}/{ch}')
def post_channel(
    psu: str,
    ch: int,
    units: types.Units,
    state: Optional[bool] = None,
    name: Optional[str] = None,
    current_limit: Optional[float] = None,
    voltage_limit: Optional[float] = None) -> types.ChannelModel:
    '''Configure a single channel for a given power supply.'''
    supply, channel = helpers.check_user_input(units, psu, ch)

    if current_limit is not None:
        was = channel.current_limit
        try:
            channel.current_limit = current_limit
        except AttributeError:
            raise HTTPException(status_code=501, detail='unable to set channel current_limit')
        logger.info(f'setting {psu}/{ch} current limit to {current_limit} (was: {was})')

    if voltage_limit is not None:
        was = channel.voltage_limit
        try:
            channel.voltage_limit = voltage_limit
        except AttributeError:
            raise HTTPException(status_code=501, detail='unable to set channel voltage_limit')
        logger.info(f'setting {psu}/{ch} voltage limit to {voltage_limit} (was: {was})')

    if state is not None:
        was = channel.state
        try:
            channel.state = state
        except AttributeError:
            raise HTTPException(status_code=501, detail='unable to set channel state')
        logger.info(f'setting {psu}/{ch} state to {state} (was: {was})')

    if name is not None:
        was = channel.name
        try:
            channel.name = name
        except AttributeError:
            raise HTTPException(status_code=501, detail='unable to set channel name')
        logger.info(f'setting {psu}/{ch} name to {name} (was: {was})')

    # readback
    supply, channel = helpers.check_user_input(units, psu, ch)
    return channel
