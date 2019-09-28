from datetime import datetime
from pathlib import Path

import pytest

from billing.models import Account, DataRoot, Member, Reading


class TestAccount:
    def test_validate_with_duplicate_timestamps_raises(self):
        account = Account(
            name="",
            electricity_readings=[
                Reading(cumulative=12000, timestamp=datetime(2019, 1, 1), units="kwh"),
                Reading(cumulative=13500, timestamp=datetime(2019, 1, 1), units="kwh"),
            ],
            gas_readings=[],
        )

        with pytest.raises(AssertionError):
            account.validate()

    def test_validate_with_more_than_one_units_raises(self):
        account = Account(
            name="",
            electricity_readings=[
                Reading(cumulative=12000, timestamp=datetime(2019, 1, 1), units="kwh"),
                Reading(cumulative=13500, timestamp=datetime(2019, 2, 1), units="wh"),
            ],
            gas_readings=[],
        )

        with pytest.raises(AssertionError):
            account.validate()


class TestRoot:
    def test_from_json(self):
        input_json = (
            (Path(__file__) / ".." / "data" / "sample-usage.json").resolve().read_text()
        )
        result = DataRoot.from_json(input_json)

        expected = DataRoot(
            members=[
                Member(
                    name="member-1",
                    accounts=[
                        Account(
                            name="account-1",
                            electricity_readings=[
                                Reading(
                                    cumulative=12000,
                                    timestamp=datetime(2019, 1, 1),
                                    units="kwh",
                                ),
                                Reading(
                                    cumulative=13500,
                                    timestamp=datetime(2019, 2, 1),
                                    units="kwh",
                                ),
                                Reading(
                                    cumulative=16000,
                                    timestamp=datetime(2019, 3, 1),
                                    units="kwh",
                                ),
                            ],
                            gas_readings=[],
                        )
                    ],
                )
            ]
        )
        assert result == expected
