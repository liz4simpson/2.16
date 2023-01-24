#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import sys


def get_train():
    """
    Запросить данные о поезде.
    """
    name = input("Пункт назначения: ")
    number = input("Номер поезда: ")
    time_str = input("Время отправления: (hh:mm) ")
    time = datetime.datetime.strptime(time_str, '%H:%M').time()

    # Создать словарь.
    return {
        'name': name,
        'number': number,
        'time': time,
    }


def display_train(trains):
    """
    Отобразить список поездов.
    """
    # Проверить, что список поездов не пуст.
    if trains:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "№",
                "Пункт назначения",
                "Номер поезда",
                "Время отправления"
            )
        )
        print(line)

        # Вывести данные о всех поездах.
        for idx, train in enumerate(trains, 1):
            time = train.get('time', '')
            print(
                '| {:>4} | {:<30} | {:<20} | {}{:>12} |'.format(
                    idx,
                    train.get('name', ''),
                    train.get('number', ''),
                    time,
                    ' ' * 5
                )
            )
            print(line)

    else:
        print('Список поездов пуст')


def select_train(trains, p_n):
    """
    Выбрать поезд с заданным пунктом назначения.
    """
    # Сформировать список поездок.
    result = []
    for train in trains:
        if train.get('name') == p_n:
            result.append(train)
    # Вернуть список выбранных поездов
    return result


def save_train(file_name, staff):
    """
    Сохранить все поезда в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=str)


def load_train(file_name):
    """
    Загрузить все поезда из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def help():
    # Вывод справки о работе с программой.
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select найти информацию о поезде по пункту назначения")
    print("help - отобразить справку;")
    print("save - сохранить список студентов;")
    print("load - загрузить список студентов;")
    print("exit - завершить работу с программой.")


def main():
    """
    Главная функция программы.
    """
    # Список поездов.
    trains = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о поездке.
            train = get_train()

            # Добавить словарь в список.
            trains.append(train)
            if len(trains) > 1:
                # Сортировка
                trains.sort(key=lambda item: item.get('time', ''))

        elif command == 'list':
            # Отобразить все поезда.
            display_train(trains)

        elif command.startswith('select'):
            parts = command.split(' ', maxsplit=1)
            # Получить требуемый пункт назначения.
            p_n = str(parts[1])
            # Выбрать поезда с заданным пунктом назначения.
            selected = select_train(trains, p_n)
            # Отобразить выбранные поезда
            display_train(selected)

        elif command == 'help':
            # Вывести справку о работе с программой.
            help()
        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_train(file_name, trains)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            trains = load_train(file_name)
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
