from text_templates import solve_error_text
from random import choice
from sql import letter_exchange


def get_given(user_text):
    given = {}
    for item in user_text.split(', '):
        formula = item.split('=')
        given.update({formula[0]: formula[1]})
    return given


def solve_task(given, formulas):
    print(given)
    answer = choice(solve_error_text)
    try:
        for key in given:
            given[letter_exchange(key)] = given.pop(key)
    except:
        pass
    for formula in formulas:
        formula = formula.split('=')[1]
        for key, value in given.items():
            formula = formula.replace(key, f"*{str(value)}")
            formula = formula.replace('+*', '+').replace('-*', '-').replace('/*', '/').replace('***', '**')
            formula = formula.replace('(*', '(').replace('^', '**')

            if formula[:1] == '*':
                formula = formula[1:]

            try:
                answer = eval(formula)
                return answer
            except SyntaxError:
                pass
            except NameError:
                pass
    return answer
