import pytest

from project1.main import redact_names

testdata = [
    ("My name is Gandhi. Nicholson teaches us a subject", "My name is ██████. █████████ teaches us a subject", 2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_names(input)
    print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count
