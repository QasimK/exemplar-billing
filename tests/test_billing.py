from datetime import datetime, timedelta
from decimal import Decimal

from billing.billing import get_bill_estimate
from billing.models import BillEstimate, Tariff, UsageEstimate


def test_get_bill_estimate_with_different_time_periods():
    usage_estimate = UsageEstimate(
        billing_date=datetime(2019, 1, 5),
        time_period=timedelta(days=5),
        usage_estimate=Decimal("200"),
        usage_units="units",
    )
    tariff = Tariff(standing_charge=Decimal("23"), unit_charge=Decimal("3"))

    result = get_bill_estimate(usage_estimate, tariff)

    assert result == BillEstimate(
        billing_date=datetime(2019, 1, 5),
        billing_period=timedelta(days=5),
        usage_estimate=Decimal("200"),
        usage_units="units",
        # Standing charge + Unit charge
        price_estimate=Decimal(5 * 23 + 200 * 3),
    )


def test_get_bill_estimate_with_half_day_not_counting_for_standing_charge():
    usage_estimate = UsageEstimate(
        billing_date=datetime(2019, 1, 5),
        time_period=timedelta(days=5, hours=12),
        usage_estimate=Decimal("2"),
        usage_units="units",
    )
    tariff = Tariff(standing_charge=Decimal("5"), unit_charge=Decimal("7"))

    result = get_bill_estimate(usage_estimate, tariff)

    assert result == BillEstimate(
        billing_date=datetime(2019, 1, 5),
        billing_period=timedelta(days=5, hours=12),
        usage_estimate=Decimal("2"),
        usage_units="units",
        price_estimate=Decimal(5 * 5 + 2 * 7),  # 5 days not 5.5 days!
    )
