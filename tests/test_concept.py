import pytest

from project1.main import redact_concept

testdata = [
    ("My dog has 2 kids. My name is Asha. My school is closed today", "██████████████████ My name is Asha. █████████████████████████", 2),
    ("I hate kids. I love Santa","████████████ I love Santa",1)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_concept(input,concepts=['kid','school','movie'])
    #print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count