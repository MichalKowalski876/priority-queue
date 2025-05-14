import json
from time import time
from random import randint


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f'{func.__name__} took {end_time - start_time:.6f} seconds')
        return result

    return wrapper


def fetch_data():
    try:
        with open('queue.json', 'r') as fh:
            content = fh.read()
            queue = json.loads(content)
            return queue
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        with open('queue.json', 'w') as fh:
            json.dump([], fh)
    return fetch_data()


def save_data(data):
    with open('queue.json', 'w') as fh:
        json.dump(data, fh)


def queue_sort(data):
    swap = False
    data_length = len(data)
    for index in range(data_length):
        for pri_val in range(0, data_length - index - 1):
            if data[pri_val]['priority'] > data[pri_val + 1]['priority']:
                data[pri_val]['priority'], data[pri_val + 1]['priority'] = data[pri_val + 1]['priority'], data[pri_val][
                    'priority']
                swap = True
        if not swap:
            break
    save_data(data)


def display_data(data, display_search=False):
    print('Index no.     Priority     Value')
    display_space = '            '
    if display_search:
        data_compare = fetch_data()
        for element in range(len(data_compare)):
            for search_element in data:
                if data_compare[element] == search_element:
                    print(
                        str(element + 1) + display_space + ' ' + str(search_element['priority']) + display_space + str(
                            search_element['value']))
    else:
        for value in range(len(data)):
            data_dictionary = data[value]
            print(str(value + 1) + display_space + ' ' + str(data_dictionary['priority']) + display_space + str(
                data_dictionary['value']))


def add_elements(data):
    while True:
        variant = input('1. Add custom element\n'
                        '2. Add random elements\n'
                        '3. Return to main menu\n')
        print('')
        if variant == '1':
            priority = int(input('input priority of element: '))
            value = input('input value of element: ')
            new_element = [{'priority': priority, 'value': value}]
            add_elements_logic(data, new_element)
        elif variant == '2':
            amount = int(input('How many elements do you want to add?: '))
            new_randoms = [{'priority': randint(1, 25), 'value': f'task {randint(1, 999)}'} for _ in range(amount)]
            add_elements_logic(data, new_randoms)
        elif variant == '3':
            return
        else:
            print('Invalid option')


def add_elements_logic(data, new_elements):
    data.extend(new_elements)
    queue_sort(data)


def delete_elements(data):
    while True:
        variant = input('1. Delete single entry by index\n'
                        '2. Delete group by priority\n'
                        '3. Delete group by value\n'
                        '4. Return to main menu\n')
        print('')
        if variant == '1':
            try:
                idx = int(input('Index to delete: ')) - 1
                delete_by_index(data, idx)
            except (ValueError, IndexError):
                print('Invalid index.')
        elif variant == '2':
            try:
                prio = int(input('Priority to delete: '))
                delete_by_priority(data, prio)
            except ValueError:
                print('Invalid priority.')
        elif variant == '3':
            val = input('Value to delete: ')
            delete_by_value(data, val)
        elif variant == '4':
            return


@timer
def delete_by_index(data, index):
    del data[index]
    queue_sort(data)


@timer
def delete_by_priority(data, priority):
    for i in range(len(data) - 1, -1, -1):
        if data[i]['priority'] == priority:
            del data[i]
    queue_sort(data)


@timer
def delete_by_value(data, value):
    for i in range(len(data) - 1, -1, -1):
        if data[i]['value'] == value:
            del data[i]
    queue_sort(data)

@timer
def search_elements(data):
    search_query = input('Search query(!exit to return to main menu): ')
    if search_query != '!exit':
        print('Search results: ')
        search_logic(data, search_query)


@timer
def search_logic(data, query):
    result = []
    try:
        result.append(data[int(query) - 1])
    except (ValueError, IndexError):
        pass
    try:
        if 0 < int(query) < 26:
            result += [x for x in data if x['priority'] == int(query)]
    except ValueError:
        pass
    result += [x for x in data if x['value'] == query]
    display_data(result, True)


def main_menu():
    while True:
        action = input('Choose an action:\n'
                       '1. Add element to queue\n'
                       '2. Delete an element from queue\n'
                       '3. Search for element in queue\n'
                       '4. Display all elements in queue\n'
                       '5. Stop the program\n')
        print('')
        if action == '1':
            add_elements(fetch_data())
        elif action == '2':
            delete_elements(fetch_data())
        elif action == '3':
            search_elements(fetch_data())
        elif action == '4':
            display_data(fetch_data())
        elif action == '5':
            break
        else:
            print('Invalid option')


if __name__ == '__main__':
    main_menu()
