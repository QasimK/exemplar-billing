import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

###
# As the data would be loaded from external storage, the from_dict methods
# are just for this example.
#
# I don't like them.
###


@dataclass
class Reading:
    cumulative: int
    timestamp: datetime
    units: str

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            cumulative=dict_["cumulative"],
            timestamp=datetime.fromisoformat(dict_["timestamp"]),
            units=dict_["units"],
        )


@dataclass
class Account:
    name: str
    electricity_readings: List[Reading]
    gas_readings: List[Reading]

    # TODO: Better validation design (ValidationError, Factory/Builder method, separate ValidAccount?)
    def validate(self):
        self._validate_readings(self.electricity_readings)
        self._validate_readings(self.gas_readings)

    def _validate_readings(self, readings):
        self._validate_no_duplicated_timestamp(readings)
        self._validate_single_units(readings)

    @staticmethod
    def _validate_no_duplicated_timestamp(readings):
        # TODO: raise ValidationError Exception
        assert len(set(reading.timestamp for reading in readings)) == len(readings)

    @staticmethod
    def _validate_single_units(readings):
        # This is obviously not terrible, but rest of system does not handle conversions
        assert len(set(reading.units for reading in readings)) <= 1

    @classmethod
    def from_dict(cls, key, value):
        account = cls(
            name=key,
            electricity_readings=[
                Reading.from_dict(dict_) for dict_ in value.get("electricity", [])
            ],
            gas_readings=[Reading.from_dict(dict_) for dict_ in value.get("gas", [])],
        )
        account.validate()
        return account


@dataclass
class Member:
    name: str
    accounts: List[Account]

    def get_account(self, name):
        # TODO: This is suboptimal for large lists
        return next(account for account in self.accounts if account.name == name)

    @classmethod
    def from_dict(cls, key, value):
        return cls(
            name=key,
            accounts=[
                Account.from_dict(key=account_key, value=account_value)
                for account_key, account_value in value.items()
            ],
        )


# TODO: Need a better name than DataRoot :)
@dataclass
class DataRoot:
    members: Member

    def get_member(self, name):
        # TODO: This is suboptimal for large lists
        return next(member for member in self.members if member.name == name)

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            members=[
                Member.from_dict(key=member_key, value=member_value)
                for member_key, member_value in dict_.items()
            ]
        )

    @classmethod
    def from_json(cls, json_str):
        dict_ = json.loads(json_str)
        return cls.from_dict(dict_)


@dataclass
class UsageEstimate:
    billing_date: datetime
    time_period: timedelta
    usage_estimate: Decimal
    usage_units: str


@dataclass
class BillEstimate:
    billing_date: datetime
    billing_period: timedelta
    usage_estimate: Decimal
    usage_units: str
    price_estimate: Decimal


@dataclass
class DualBillEstimate:
    billing_date: datetime
    electricity_bill_estimate: Optional[BillEstimate]
    gas_bill_estimate: Optional[BillEstimate]


@dataclass
class Tariff:
    standing_charge: Decimal
    unit_charge: Decimal

    @classmethod
    def from_json(cls, json_str):
        dict_ = json.loads(json_str)
        return cls.from_dict(dict_)

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            standing_charge=Decimal(dict_["standing_charge"]),
            unit_charge=Decimal(dict_["unit_charge"]),
        )


@dataclass
class DualTariff:
    electricity_tariff: Tariff
    gas_tariff: Tariff

    @classmethod
    def from_json(cls, json_str):
        dict_ = json.loads(json_str)
        return cls.from_dict(dict_)

    @classmethod
    def from_dict(cls, dict_):
        return cls(
            electricity_tariff=Tariff.from_dict(dict_["electricity"]),
            gas_tariff=Tariff.from_dict(dict_["gas"]),
        )
