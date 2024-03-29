#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2022, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
""" Provide date and time related properties

"""

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import datetime

# Bokeh imports
from ...util.serialization import convert_date_to_datetime, is_datetime_type, is_timedelta_type
from .bases import Property
from .primitive import bokeh_integer_types
from .singletons import Undefined

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'Date',
    'Datetime',
    'TimeDelta',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Date(Property):
    """ Accept ISO format Date (but not DateTime) values.

    """
    def transform(self, value):
        value = super().transform(value)

        if isinstance(value, datetime.date):
            value = value.isoformat()

        return value

    def validate(self, value, detail=True):
        super().validate(value, detail)

        # datetime.datetime is datetime.date, exclude manually up front
        if isinstance(value, datetime.datetime):
            msg = "" if not detail else "Expected a date value, got a datetime.datetime"
            raise ValueError(msg)

        if isinstance(value, datetime.date):
            return

        try:
            datetime.datetime.fromisoformat(value)
        except Exception:
            msg = "" if not detail else f"Expected an ISO date string, got {value!r}"
            raise ValueError(msg)

class Datetime(Property):
    """ Accept ISO format Datetime values.

    """

    def __init__(self, default=Undefined, help=None) -> None:
        super().__init__(default=default, help=help)

    def transform(self, value):
        value = super().transform(value)

        if isinstance(value, str):
            value = datetime.datetime.fromisoformat(value)

        # Handled by serialization in protocol.py for now, except for Date
        if isinstance(value, datetime.date):
            value = convert_date_to_datetime(value)

        return value

    def validate(self, value, detail=True):
        super().validate(value, detail)

        if is_datetime_type(value):
            return

        if isinstance(value, datetime.date):
            return

        if Datetime.is_timestamp(value):
            return

        if isinstance(value, str):
            try:
                datetime.datetime.fromisoformat(value).date()
                return
            except Exception:
                pass

        msg = "" if not detail else f"Expected a date, datetime object, or timestamp, got {value!r}"
        raise ValueError(msg)

    @staticmethod
    def is_timestamp(value):
        return isinstance(value, (float,) + bokeh_integer_types) and not isinstance(value, bool)

class TimeDelta(Property):
    """ Accept TimeDelta values.

    """

    def __init__(self, default=datetime.timedelta(), help=None) -> None:
        super().__init__(default=default, help=help)

    def transform(self, value):
        value = super().transform(value)
        return value
        # Handled by serialization in protocol.py for now

    def validate(self, value, detail=True):
        super().validate(value, detail)

        if is_timedelta_type(value):
            return

        msg = "" if not detail else f"Expected a timedelta instance, got {value!r}"
        raise ValueError(msg)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
