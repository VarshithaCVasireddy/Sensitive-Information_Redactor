import pytest

from project1.main import redact_genders

testdata = [
    ("He is my friend", "██ is my friend", 1)
    
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_genders(input)
    #print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count