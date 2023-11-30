from __future__ import annotations

from typing import Dict

from fastapi import Depends
from typing_extensions import Annotated

from psudaemon import context, psumodels

Units = Annotated[Dict[str, psumodels.Unit], Depends(context.load_units)]
