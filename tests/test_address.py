import pytest

from project1.main import redact_address

testdata = [
    ("My address is 2200 Classen blvd, apt 10115, Norman, Oklahoma, 73071. My friend address is 2230 Classen blvd, apt 10115, Norman, Oklahoma, 73071", 
    "My address is █████████████████████████████████████████████████████. My friend address is █████████████████████████████████████████████████████", 
    2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_address(input)
    #print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count