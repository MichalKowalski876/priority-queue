import json
from random import randint


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
    print('{:<7} {:<9} {}'.format('Index', 'Priority', 'Value'))
    display_space = '            '
    if display_search:
        data_compare = fetch_data()
        print('{:<7} {:<9} {}'.format('Index', 'Priority', 'Value'))
        for idx, search_element in enumerate(data, start=1):
            if search_element in data_compare:
                print('{:<7} {:<9} {}'.format(idx, search_element['priority'], search_element['value']))
    else:
        print('{:<7} {:<9} {}'.format('Index', 'Priority', 'Value'))
        for idx, item in enumerate(data, start=1):
            print('{:<7} {:<9} {}'.format(idx, item['priority'], item['value']))
        print('')


def add_elements(data):
    while True:
        variant = input('1. Add custom element\n'
                        '2. Add random elements\n'
                        '3. Return to main menu\n')
        print('')

        if variant == '1':  # custom element
            print('priority 1-25: 1 highest - 25 lowest')
            while True:
                priority = input('input priority of element: ')
                try:
                    priority = int(priority)
                    break
                except ValueError:
                    print('\nMust be a number in range 1 - 25')

            value = input('input value of element: ')

            new_element = [{'priority': priority, 'value': value}]
            data.extend(new_element)
            queue_sort(data)

        elif variant == '2':  # random elements
            try:
                amount = int(input('How many elements do you want to add?: '))
                for radom_entry in range(amount):
                    priority = randint(1, 25)
                    value = 'task ' + str(randint(1, 999))
                    new_random_element = {'priority': priority, 'value': value}
                    data.append(new_random_element)
                queue_sort(data)
                break
            except ValueError:
                print('Input a number')
        elif variant == '3':
            main_menu()
        else:
            print('Invalid option')

        queue_sort(data)
        break


def delete_elements(data):
    while True:
        variant = input('1. Delete single entry by index\n'
                        '2. Delete group by priority\n'
                        '3. Delete group by value\n'
                        '4. Return to main menu\n')
        print('')

        if variant == '1':
            index_number = input('Input index of an element: ')
            try:
                del data[int(index_number) - 1]
            except ValueError:
                print('Input a number')
            except IndexError:
                print(f'No element under {index_number}')

        elif variant == '2':
            delete_priority = input('Input priority group: ')
            try:
                for element in range(len(data) - 1, -1, -1):
                    if data[element]['priority'] == int(delete_priority):
                        del data[element]

                queue_sort(data)
            except ValueError:
                print('Input a number')

        elif variant == '3':
            delete_value = input('Input value to delete: ')
            for element in range(len(data) - 1, -1, -1):
                if data[element]['value'] == delete_value:
                    del data[element]

            queue_sort(data)

        elif variant == '4':
            main_menu()
        main_menu()


def search_elements(data):
    search_query = input('Search query(!exit to return to main menu): ')
    result = []
    if search_query != '!exit':
        print('search results: ')
        try:  # index & priority search
            result.append(data[int(search_query) - 1])
            if 0 < int(search_query) < 26:
                for element in data:
                    if int(search_query) == element['priority']:
                        result.append(element)

        except (TypeError, ValueError, IndexError):
            pass

        for element in data:  # value search
            if search_query == element['value']:
                result.append(element)

        display_data(result, True)
    else:
        main_menu()


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
