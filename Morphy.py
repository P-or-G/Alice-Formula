from pymorphy2 import MorphAnalyzer


morph = MorphAnalyzer()


def inf(text):
    lst = text.replace('.', '').replace('!', '').replace('?', '').replace('_', '')
    lst = lst.replace('\n', ' ').replace('[', '').replace(']', '').split()
    lst_end = []

    for word in lst:
        lst_end.append(morph.parse(word)[0].normal_form)
    infinitive_string = ' '.join(lst_end)
    return infinitive_string
