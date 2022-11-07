from datetime import datetime

import pandas
from pandas.testing import assert_frame_equal

from tokenomics import csv

from . import DATA


def test_generate() -> None:
    expected_csv = pandas.read_csv(DATA + "/tokenomics.csv")
    expected_csv["Date"] = pandas.to_datetime(expected_csv["Date"])

    assert_frame_equal(
        csv.generate(0, 8, 5, datetime(2022, 10, 12), 1575000),
        expected_csv,
    )
