import pytest

from project1.main import redact_phones

testdata = [
    ("My Phone no. is +1(469)604-6217, +919553340279", "My Phone no. is ███████████████, █████████████", 2),
    ("I got a new phone number +1(569)6046217, +919247282039","I got a new phone number ██████████████, █████████████",2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = redact_phones(input)
    #print(actual_text)

    assert actual_text == expected_text
    assert len(word_list) == expected_count