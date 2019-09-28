from datetime import datetime

from billing.billing import get_bill_estimate
from billing.models import DataRoot, DualBillEstimate, DualTariff
from billing.usage.base import BaseUsageEstimator


def get_dual_bill_estimate_for_member_account(
    data_root: DataRoot,
    member_name: str,
    account_name: str,
    dual_tariff: DualTariff,
    estimator: BaseUsageEstimator,
    billing_date: datetime,
) -> DualBillEstimate:
    account = data_root.get_member(member_name).get_account(account_name)
    electricity_bill_estimate = None
    if account.electricity_readings:
        electricity_usage_estimate = estimator.estimate_usage(
            account.electricity_readings, billing_date
        )
        electricity_bill_estimate = get_bill_estimate(
            electricity_usage_estimate, dual_tariff.electricity_tariff
        )

    gas_bill_estimate = None
    if account.gas_readings:
        gas_usage_estimate = estimator.estimate_usage(
            account.gas_readings, billing_date
        )
        gas_bill_estimate = get_bill_estimate(
            gas_usage_estimate, dual_tariff.gas_tariff
        )

    return DualBillEstimate(
        billing_date=billing_date,
        electricity_bill_estimate=electricity_bill_estimate,
        gas_bill_estimate=gas_bill_estimate,
    )
