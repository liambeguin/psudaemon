from  typing import Dict, Tuple
from . import psumodels


def check_user_input(
    units: Dict[str, psumodels.Unit],
    psu: str,
    ch: int=None) -> Tuple[psumodels.Unit, psumodels.Channel]:

    if psu not in units.keys():
        raise HTTPException(status_code=404, detail='undefined psu')
    if ch is not None and ch > units[psu]._channel_count:
        raise HTTPException(status_code=404, detail='channel out of range')

    psu = units[psu]
    ch = psu.channels[ch] if ch is not None else None

    return psu, ch
