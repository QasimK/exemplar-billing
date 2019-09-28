"""Main Business Logic to calculate estimated bill."""

from datetime import datetime, timedelta
from decimal import Decimal
from operator import attrgetter
from typing import List, Tuple

from billing.models import Reading, UsageEstimate
from billing.usage.base import BaseUsageEstimator, UsageEstimatorError


class LinearExtrapolationUsageEstimator(BaseUsageEstimator):
    """Extend out the line between the latest readings to the billing date.

    |       *
    |
    |     *
    |    /
    |   /
    |  *
    |________

    This estimate uses the number of seconds between time periods.
    It might not make much sense for very short time periods, like on the same day!
    """

    def estimate_usage(
        self, readings: List[Reading], billing_date: datetime
    ) -> UsageEstimate:
        return UsageEstimate(
            billing_date=billing_date,
            time_period=billing_period(readings, billing_date),
            usage_estimate=estimated_usage(readings, billing_date),
            usage_units=usage_units(readings),
        )


def estimated_usage(readings: List[Reading], billing_date: datetime):
    return per_second_increase(readings) * int(
        billing_period(readings, billing_date).total_seconds()
    )


def per_second_increase(readings: List[Reading]) -> Decimal:
    return Decimal(usage_difference(readings)) / time_difference_in_seconds(readings)


def billing_period(readings: List[Reading], billing_date: datetime):
    initial, _ = latest_two_readings(readings)
    time_period = billing_date - initial.timestamp
    if time_period < timedelta(seconds=0):
        raise UsageEstimatorError("Billing date must be after the first reading.")

    return time_period


def usage_difference(readings: List[Reading]) -> int:
    initial, final = latest_two_readings(readings)
    diff = final.cumulative - initial.cumulative
    if diff < 0:
        raise UsageEstimatorError("Reading decreased")

    return diff


def time_difference_in_seconds(readings: List[Reading]) -> int:
    """Return the difference in time to the nearest second."""
    initial, final = latest_two_readings(readings)
    seconds = (final.timestamp - initial.timestamp).total_seconds()
    if seconds == 0:
        raise UsageEstimatorError("Two readings taken at the exact same second")

    return int(seconds)


def latest_two_readings(readings: List[Reading]) -> Tuple[Reading, Reading]:
    if len(readings) < 2:
        raise UsageEstimatorError("Need at least two readings")
    return sorted(readings, key=attrgetter("timestamp"))[-2:]


def usage_units(readings):
    units = set(reading.units for reading in readings)
    if len(units) > 1:
        raise UsageEstimate("All readings must have the same units")

    return units.pop()
