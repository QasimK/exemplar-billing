from datetime import datetime, timedelta
from decimal import Decimal

from billing.models import (Account, BillEstimate, DataRoot, DualBillEstimate,
                            DualTariff, Member, Reading, Tariff, UsageEstimate)
from billing.shortcuts import get_dual_bill_estimate_for_member_account
from billing.usage.base import BaseUsageEstimator


def test_get_dual_bill_estimate_for_member_account_with_one_set_of_readings_only():
    data_root = DataRoot(
        members=[
            Member(
                name="member",
                accounts=[
                    Account(
                        name="account",
                        electricity_readings=[
                            Reading(
                                cumulative=0,
                                timestamp=datetime(2019, 4, 1),
                                units="kWh",
                            ),
                            Reading(
                                cumulative=1,
                                timestamp=datetime(2019, 4, 2),
                                units="kWh",
                            ),
                        ],
                        gas_readings=[],
                    )
                ],
            )
        ]
    )
    dual_tariff = DualTariff(
        electricity_tariff=Tariff(
            standing_charge=Decimal("100"), unit_charge=Decimal("1")
        ),
        gas_tariff=None,
    )
    billing_date = datetime(2019, 4, 7)

    result = get_dual_bill_estimate_for_member_account(
        data_root=data_root,
        member_name="member",
        account_name="account",
        dual_tariff=dual_tariff,
        estimator=_TestEstimator(),
        billing_date=billing_date,
    )

    assert result == DualBillEstimate(
        billing_date=billing_date,
        electricity_bill_estimate=BillEstimate(
            billing_date=datetime(2010, 1, 1),
            billing_period=timedelta(days=1),
            usage_estimate=Decimal("1"),
            usage_units="Fake",
            price_estimate=Decimal("101"),
        ),
        gas_bill_estimate=None,
    )


class _TestEstimator(BaseUsageEstimator):
    USAGE_ESTIMATE = UsageEstimate(
        billing_date=datetime(2010, 1, 1),
        time_period=timedelta(days=1),
        usage_estimate=Decimal("1"),
        usage_units="Fake",
    )

    def estimate_usage(self, *args, **kwargs):
        return self.USAGE_ESTIMATE
