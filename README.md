# Bill Estimator

The main focus for this was to demonstrate good architecture practices rather than
handling every edge-case!

## Sample execution

No installation required:

```
$ python3.7 example.py
Your estimated bill for 01/04/2019 is

Electricity
===========
Usage estimate: 5268 kwh
Price estimate: £65232.80
(Billing Period 01/02/2019 to 01/04/2019)

Gas
===
Usage estimate: 14549 m³
Price estimate: £76004.95
(Billing Period 01/09/2018 to 01/04/2019)
```

This uses `example-tariff.json` and `example-data.json`.


## Development

Run tests from scratch:

```
$ pip install --user pipx
$ pipx install poetry
$ poetry run pytest
```


## Major TODOs

* The billing period is tied to when the readings were taken - you can only
specify the end billing date.
* Handle validation on models (in particular Account) better, and generally how
exceptions are handled (currently no handling).
