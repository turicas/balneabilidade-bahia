import pathlib

import rows

from sc_extrai_boletim import extract_table
from tests.utils import assert_equal
from settings import TEST_DATA_PATH


DATA_PATH = TEST_DATA_PATH / "SC"


def test_extract_table_1():
    expected = rows.import_from_csv(DATA_PATH / "expected_1.csv")
    result = rows.import_from_dicts(extract_table(DATA_PATH / "example_1.pdf"))
    assert_equal(result, expected)


def test_extract_table_2():
    expected = rows.import_from_csv(DATA_PATH / "expected_2.csv")
    result = rows.import_from_dicts(
        extract_table(DATA_PATH / "example_2.pdf")[: len(expected)]
    )
    assert_equal(result, expected)


def test_extract_table_3():
    expected = rows.import_from_csv(DATA_PATH / "expected_3.csv")
    result = rows.import_from_dicts(extract_table(DATA_PATH / "example_3.pdf"))
    assert_equal(result, expected)
