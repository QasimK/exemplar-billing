from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from billing.models import Reading, UsageEstimate
from billing.usage.base import UsageEstimatorError
from billing.usage.linear import LinearExtrapolationUsageEstimator


class TestLinearExtrapolationUsageEstimator:
    @pytest.fixture
    def estimator(self):
        return LinearExtrapolationUsageEstimator()

    @pytest.fixture
    def readings(self):
        return [
            Reading(cumulative=1000, timestamp=datetime(2019, 1, 1), units=""),
            Reading(cumulative=1200, timestamp=datetime(2019, 1, 3), units=""),
        ]

    @pytest.mark.parametrize(
        "billing_date, expected_estimate",
        [
            (datetime(2019, 1, 5), Decimal("399.9999999999999999999999999")),
            (datetime(2019, 1, 2), Decimal("99.99999999999999999999999996")),
        ],
    )
    def test_estimate_usage_with_different_billing_dates(
        self, estimator, readings, billing_date, expected_estimate
    ):
        assert estimator.estimate_usage(readings, billing_date) == UsageEstimate(
            billing_date=billing_date,
            time_period=billing_date - readings[0].timestamp,
            # TODO: This is annoying - checking to 2 decimal places would be enough!
            usage_estimate=expected_estimate,
            usage_units="",
        )

    def test_estimate_usage_does_not_allow_historic_billing_dates(
        self, estimator, readings
    ):
        with pytest.raises(
            UsageEstimatorError, match="date must be after the first reading"
        ):
            estimator.estimate_usage(readings, datetime(2018, 1, 1))

    def test_estimate_usage_uses_latest_two_readings(self, estimator):
        readings = [
            Reading(cumulative=1300, timestamp=datetime(2019, 1, 6), units=""),
            Reading(cumulative=1000, timestamp=datetime(2019, 1, 3), units=""),
            Reading(cumulative=999, timestamp=datetime(2019, 1, 1), units=""),
        ]
        billing_date = datetime(2019, 1, 10)

        estimator.estimate_usage(readings, billing_date) == UsageEstimate(
            billing_date=billing_date,
            time_period=timedelta(days=7),
            usage_estimate=Decimal("1000"),
            usage_units="",
        )
