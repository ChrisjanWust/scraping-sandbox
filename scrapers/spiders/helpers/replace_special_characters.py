SPECIAL_CHARACTERS = {
    "\u2070": "\u00B0",
    "\u2113": "l",
    "‑": "-",
    "ƒ": "f",
    "×": "x"
}


def normalize_special_chars(t_in):
    def normalize_special_chars_str(text):
        for special_char, char in SPECIAL_CHARACTERS.items():
            text = text.replace(special_char, char)
        return text

    assert isinstance(t_in, (str, list, dict))

    if type(t_in)==str:
        return normalize_special_chars_str(t_in)
    elif type(t_in)==list:
        for i, text in enumerate(t_in):
            t_in[i] = normalize_special_chars(text)
        return t_in
    elif type(t_in)==dict:
        for key, value in t_in.items():
            value = t_in.pop(key)
            key = normalize_special_chars_str(key)
            t_in[key] = normalize_special_chars(value)
        return t_in


def test_clean(t_in):
    def test_clean_str(text):
        for special_char in SPECIAL_CHARACTERS:
            assert special_char not in text

    assert isinstance(t_in, (str, list, dict))

    if type(t_in)==str:
        test_clean_str(t_in)
    elif type(t_in)==list:
        for value in t_in:
            test_clean(value)
    elif type(t_in)==dict:
        for key, value in t_in.items():
            test_clean_str(key)
            test_clean(value)


def test():
    data = [
        ['Capacity: 43ℓ', 'Temperature (⁰C): 5'],
        'Capacity: 43ℓ',
        {
            'specs': {
                'Capacity': "43ℓ",
                'Temperature (⁰C)': '5'
            }
        }
    ]

    """
    # Could be used to test `test_clean`
    for value in data:
        test_clean(value)  # should fail
    """

    for value in data:
        value = normalize_special_chars(value)
        test_clean(value)


if __name__ == '__main__':
    test()
