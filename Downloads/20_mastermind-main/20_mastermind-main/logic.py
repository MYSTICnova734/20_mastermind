def feedback(code, guess):

    # Exact matches are resolved first; those positions are then used up so
    # duplicate symbols can't consume the same code occurrence again.
    exact = 0
    remaining_code = []
    remaining_guess = []
    for c, g in zip(code, guess):
        if c == g:
            exact += 1
        else:
            remaining_code.append(c)
            remaining_guess.append(g)

    # Partial matches come only from the leftover symbols, each code
    # position being counted at most once.
    partial = 0
    for g in remaining_guess:
        if g in remaining_code:
            remaining_code.remove(g)
            partial += 1
    return exact, partial