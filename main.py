from task_actions import get_given, solve_task
from sql import get_similar_items, find_formula
import text_templates
import image_templates
from Morphy import inf

from random import choice
from flask import Flask, request
import logging
import json


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

FORMULAS = []
error_counter = 0


@app.route("/", methods=["POST"])
def main():
    global FORMULAS
    global error_counter

    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }

    req = request.json
    if req["session"]["new"]:
        response["response"]["text"] = text_templates.first_text
    else:
        user_input = req["request"]["original_utterance"]

        if error_counter == 'button':
            error_counter = 0
            if find_formula(user_input):
                response["response"]["text"] = choice(text_templates.correct_answer)
            else:
                response["response"]["text"] = choice(text_templates.incorrect_answer)
            return json.dumps(response)

        # Если проверка (файл text_templates, help_keywords) пройдёт успешно, пользователю выведут текст help_text
        for i in text_templates.help_keywords:
            if i in user_input.capitalize():
                response["response"]["text"] = text_templates.help_text
                return json.dumps(response)

        # Если проверка (файл text_templates, func_keywords) пройдёт успешно, пользователю выведут текст func_text
        for i in text_templates.func_keywords:
            if i in user_input.capitalize():
                response["response"]["text"] = text_templates.func_text
                return json.dumps(response)

        # Если проверка (файл text_templates, hello_keyword) пройдёт успешно, пользователю выведут текст hello_template
        for i in text_templates.hello_keyword:
            if i in user_input.capitalize():
                response["response"]["text"] = choice(text_templates.hello_template)
                return json.dumps(response)

        for i in text_templates.minigame_keywords:
            if i in inf(user_input.capitalize()):
                response["response"]["text"] = text_templates.minigame_ans
                response["response"]["buttons"] = image_templates.minigame_buttons
                response["response"]["card"] = image_templates.minigame_card
                error_counter = 'button'
                return json.dumps(response)

        if "=" in user_input or "равный" in inf(user_input):
            if FORMULAS:
                response["response"]["text"] = solve_task(get_given(inf(user_input).replace('равный', '=').replace('равно', '=')), FORMULAS)
            else:
                response["response"]["text"] = text_templates.cannot_solve
                error_counter += 1
        else:
            FORMULAS = []
            answer = choice(text_templates.formulas_answer)

            for word in user_input.lower().split():
                for item in get_similar_items(word):
                    for formula in item[1].replace('[', '').replace(']', '').replace("'", "").split(',  '):
                        FORMULAS.append(formula)
                        answer += f"- {formula}\n"

            if answer in text_templates.formulas_answer:
                if error_counter <= 4:
                    answer = choice(text_templates.error_text)
                else:
                    error_counter = 0
                    answer = text_templates.multi_error
                error_counter += 1
            else:
                error_counter = 0

            response["response"]["text"] = answer.replace('**', '^')

    return json.dumps(response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
