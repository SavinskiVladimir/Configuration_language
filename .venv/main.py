import yaml
import sys
import re

def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        # загрузка данных из yaml файла, содержащего код конфигурационного языка
        return yaml.safe_load(file) # возвращается словарь


def convert_to_custom_language(data):
    output = [] # список для формирования выводимого результата работы
    for key, value in data.items(): # проход по списку, содержащему данные о yaml файле
        if isinstance(value, list): # если обрабатываемый объект имеет тип список
            # перевод списка в массив согласно описанию из постановки
            array_values = '; '.join(map(str, value))
            output.append(f"{key}: [{array_values}]")
        elif isinstance(value, dict): # если обрабатываемый объект имеет тип словарь
            # рекурсивный перевод словаря
            output.append(f"{key}: {{ {convert_to_custom_language(value)} }}")
        elif isinstance(value, str) and value.startswith("#"): # если обрабатываемый объект является строкой, начинающейся с "#"
            # обработка однострочного комментария
            output.append(f"* {value[1:].strip()}")
        elif isinstance(value, str) and key == 'multi_line_comment': # если обрабатываемый объект пара, где ключ - объявление многострочного комментария
            # обработка многострочного комментария
            comment_content = value.strip()
            output.append(f"{{{{!\n{comment_content}\n}}}}")
        elif re.match(r'^[a-zA-Z]+$', key): # если объект пара, где ключ является объявлением идентификатора
            # если значение содержит вычисление выражения
            if isinstance(value, str) and re.match(r'^[0-9\s\+\-\*/]+$', value):
                # вычисление значения выражения
                evaluated_value = eval(value)
                # запись определения значения
                output.append(f"(define ${key}$ {evaluated_value});")
            else:
                # запись определения значения
                output.append(f"(define {key} {value});")
        else:
            # запись значений типа "строка: строка"
            output.append(f"{key}: {value}")

    # формирование выходной строки через конкатенацию значений в списке через перенос на следующую строку
    return "\n".join(output)

def main():
    file_path = sys.argv[1] # получение пути к yaml файлу из параметров командной строки
    try:
        data = parse_yaml(file_path) # получение данных из yaml файла
        output = convert_to_custom_language(data) # обработка содержимого файла
        print(output) # вывод сформированного кода на реализуемом коонфигурационном языке в консоль
    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()