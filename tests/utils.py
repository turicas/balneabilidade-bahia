def assert_equal(result, expected):
    """Normalize each row so we can compare"""

    result = [dict(row._asdict()) for row in result]
    expected = [dict(row._asdict()) for row in expected]
    assert result == expected
