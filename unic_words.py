def unic_counter(some_string: str) -> dict:
    result = {}
    for word in some_string.split():
        word = word.lower().strip('.,?!').strip()
        result[word] = result.get(word, 0) + 1

    return result


dialog_s_artemom = "привет пока, как дела, как ты, привет ты как дела у? Тут так там все ок привет как ты, пока куда я ты что?"
print(unic_counter(dialog_s_artemom))
