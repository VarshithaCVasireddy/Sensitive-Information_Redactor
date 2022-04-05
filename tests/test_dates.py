import pytest

from project1.main import redact_dates

testdata = [
    ("Today date is 4/3/2021, my birthday is on November 16th 1997", "Today date is ████████, my birthday is on ██████████████████", 2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_dates(input)
    #print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count