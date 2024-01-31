def pretty_bool(value: bool, add_word=True) -> str:
    if value:
        return 'Есть ✅' if add_word else '✅'
    return 'Нет ⛔️' if add_word else '⛔️'
