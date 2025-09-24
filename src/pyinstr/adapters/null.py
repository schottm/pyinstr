"""
This file is part of PyINSTR.

:copyright: 2025 by Marco Schott.
:license: MIT, see LICENSE for more details.
"""

import logging
from typing import Any, override

from pyinstr import Adapter

logger = logging.getLogger(__name__)


class NullAdapter(Adapter):
    @override
    def read(self) -> str:
        logger.info('Reading from instrument.')
        return ''

    @override
    def write(self, command: str) -> None:
        logger.info(f'Writing "{command}" to instrument.')
        pass

    @override
    def apply(self, options: dict[str, Any]) -> None:
        pass
