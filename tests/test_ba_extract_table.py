import pathlib

import rows

from ba_extrai_boletim import extract_table


DATA_PATH = pathlib.Path(__file__).parent / "data/BA"


def assert_equal(result, expected):
    """Normalize each row so we can compare"""

    result = [dict(row._asdict()) for row in result]
    expected = [dict(row._asdict()) for row in expected]
    assert result == expected


def test_extract_table_1():
    expected = rows.import_from_csv(DATA_PATH / "expected_1.csv")
    result = rows.import_from_dicts(extract_table(DATA_PATH / "example_1.pdf"))
    assert_equal(result, expected)


def test_extract_table_2():
    expected = []
    result = rows.import_from_dicts(
        extract_table(DATA_PATH / "example_2.pdf")[: len(expected)]
    )
    assert_equal(result, expected)


def test_extract_table_3():
    expected = rows.import_from_csv(DATA_PATH / "expected_3.csv")
    result = rows.import_from_dicts(extract_table(DATA_PATH / "example_3.pdf"))
    assert_equal(result, expected)
