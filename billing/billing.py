"""Calculate the bill (i.e £££)."""

from datetime import timedelta
from decimal import Decimal

from billing.models import BillEstimate, Tariff, UsageEstimate


def get_bill_estimate(usage_estimate: UsageEstimate, tariff: Tariff) -> BillEstimate:
    return BillEstimate(
        billing_date=usage_estimate.billing_date,
        billing_period=usage_estimate.time_period,
        usage_estimate=usage_estimate.usage_estimate,
        usage_units=usage_estimate.usage_units,
        price_estimate=_calculate_price(
            usage_estimate.time_period,
            usage_estimate.usage_estimate,
            tariff.standing_charge,
            tariff.unit_charge,
        ),
    )


def _calculate_price(
    time_period: timedelta,
    usage: Decimal,
    standing_charge: Decimal,
    unit_charge: Decimal,
) -> Decimal:
    standing_price = _timedelta_to_floored_days(time_period) * standing_charge
    unit_price = usage * unit_charge
    return standing_price + unit_price


def _timedelta_to_floored_days(period) -> int:
    """Return the number of days rounded down."""
    return int(period.total_seconds() // (60 * 60 * 24))
