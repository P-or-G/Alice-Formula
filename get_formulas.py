import requests
from bs4 import BeautifulSoup
from sql import insert_item, create_table


def get_formulas_table():
    url = "https://intmag24.ru/dlya-shkolnikov/vse-formuly-po-fizike/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    formulas_table = soup.find('table').find('tbody').find_all('tr')
    return formulas_table


def get_formulas_list(formulas_table):
    formulas = []

    for cell in formulas_table:
        name = cell.select_one('td[style*="border: 1px solid grey; width: 30.8864%;"]')
        formula = cell.select_one('td[style*="border: 1px solid grey; width: 9.03223%;"]')

        if formula and name is not None:
            formula_sup = formula.find('sup')
            name_sub = name.find('sub')

            formula = formula.text.replace('\n', '').replace('\xa0', '').replace('∙', '').replace('√', '')
            name = name.text.replace('\n', '').replace('\xa0', '').replace('(', '').replace(')', '')
            if formula_sup:
                formula = formula.replace(formula_sup.text, f"**{formula_sup.text}")
            if name_sub:
                name = name.replace(name_sub.text, '')
            formula = formula.replace('/**', '/')

            formulas.append({name: formula.split(',')})
    return formulas


if __name__ == '__main__':
    create_table()

    formulas_table = get_formulas_table()
    formulas_list = get_formulas_list(formulas_table)

    for formula in formulas_list:
        for key, value in formula.items():
            will_insrt = (key, str(value))
            try:
                insert_item(will_insrt)
            except:
                print(f"{will_insrt} не было добавлено")
