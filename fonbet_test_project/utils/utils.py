from datetime import datetime


def get_current_timestamp():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time


def comparison_elements_to_expected_texts(elements: list, expected_texts: list):
    for index, expected_text in enumerate(expected_texts):
        element = elements[index].text
        assert element == expected_text, f"Текст в {index + 1}-м элементе не совпадает"
