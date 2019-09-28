#!/usr/bin/env python3
"""This is an example file which handles input and output to the billing service/package."""
from datetime import datetime
from pathlib import Path

from billing.models import BillEstimate, DataRoot, DualBillEstimate, DualTariff
from billing.shortcuts import get_dual_bill_estimate_for_member_account
from billing.usage import LinearExtrapolationUsageEstimator


def main():
    """Print the estimated bill."""
    data_root = DataRoot.from_json(_read_json("example-data.json"))
    dual_tariff = DualTariff.from_json(_read_json("example-tariff.json"))

    dual_bill_estimate = get_dual_bill_estimate_for_member_account(
        data_root=data_root,
        member_name="member-1",
        account_name="account-1",
        dual_tariff=dual_tariff,
        estimator=LinearExtrapolationUsageEstimator(),
        billing_date=datetime(2019, 4, 1),
    )

    print(_format_dual_bill(dual_bill_estimate))


def _read_json(filename):
    file = (Path(__file__) / ".." / filename).resolve()
    return file.read_text()


# TODO: Testing this is not unimportant!
def _format_dual_bill(dual_bill: DualBillEstimate) -> str:
    """We round to the nearest kWh and pence."""
    if not dual_bill.electricity_bill_estimate and not dual_bill.gas_bill_estimate:
        return "Unable to estimate any bills."

    result = f"Your estimated bill for {dual_bill.billing_date:%d/%m/%Y} is\n\n"

    if dual_bill.electricity_bill_estimate:
        result += "Electricity\n"
        result += "=" * 11 + "\n"
        result += _format_single_bill_estimate(dual_bill.electricity_bill_estimate)

    if dual_bill.electricity_bill_estimate and dual_bill.gas_bill_estimate:
        result += "\n"

    if dual_bill.gas_bill_estimate:
        result += "Gas\n"
        result += "=" * 3 + "\n"
        result += _format_single_bill_estimate(dual_bill.gas_bill_estimate)

    return result


def _format_single_bill_estimate(bill: BillEstimate) -> str:
    """We round to the nearest kWh and pence."""
    from_datetime = bill.billing_date - bill.billing_period
    return (
        f"Usage estimate: {bill.usage_estimate:.0f} {bill.usage_units}\n"
        f"Price estimate: £{bill.price_estimate:.2f}\n"
        f"(Billing Period {from_datetime:%d/%m/%Y} to {bill.billing_date:%d/%m/%Y})\n"
    )


if __name__ == "__main__":
    main()
