import logging
from rich import print
from typing import List, Optional, Dict, Any

from psudaemon import context, types

from fastapi import APIRouter, HTTPException

router = APIRouter()
logger = logging.getLogger('uvicorn')


@router.get('/settings')
def get_settings(units: types.Units) -> Dict[str, Any]:
    '''Show Configuration file.'''
    return context.Conffile().update(units)


@router.post('/settings')
def save_settings(units: types.Units) -> Dict[str, Any]:
    '''Save configuration file, using current PSU state.'''
    conf = context.Conffile()
    new_conf = conf.update(units)
    conf.write(new_conf)
    return new_conf
