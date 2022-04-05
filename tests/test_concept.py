import pytest

from project1.main import redact_concept

testdata = [
    ("My dog has 2 kids. My school is closed today. I went to movie yesterday", "██████████████████ ██████████████████████████ █████████████████████████", 3)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_concept(input,concepts=['kids','school','movie'])
    print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count