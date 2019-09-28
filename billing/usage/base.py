"""Main Business Logic to calculate estimated bill."""

from datetime import datetime
from typing import List

from billing.models import Reading, UsageEstimate


class BaseUsageEstimator:
    """Do not use directly."""

    def estimate_usage(
        self, readings: List[Reading], billing_date: datetime
    ) -> UsageEstimate:
        raise NotImplementedError()


class UsageEstimatorError(Exception):
    pass
