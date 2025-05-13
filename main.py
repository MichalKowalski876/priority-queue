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
        with open("queue_test.json", 'r') as fh:
            content = fh.read()
            queue = json.loads(content)
            return queue
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        with open('queue_test.json', 'w') as fh:
            json.dump([], fh)
            return None

            # save_data([]) # change in final version


def save_data(data):
    with open('queue.json', 'w') as fh:
        json.dump(data, fh)


def queue_sort(data):
    swap = False
    data_length = len(data)
    for index in range(data_length):
        for pri_val in range(0, data_length - index - 1):
            if data[pri_val]["priority"] > data[pri_val + 1]["priority"]:
                data[pri_val]["priority"], data[pri_val + 1]["priority"] = data[pri_val + 1]["priority"], data[pri_val][
                    "priority"]
                swap = True
        if not swap:
            break

    save_data(data)


def display_data(data):
    print('Index no.     Priority     Value')
    display_space = '            '
    for value in range(len(data)):
        data_dictionary = data[value]
        print(str((value + 1)) + display_space + " " + str(data_dictionary["priority"]) + display_space + str(
            data_dictionary["value"]))

    print('')


def add_element():
    print('priority 1-25: 1 highest - 25 lowest')
    while True:
        priority = input('input priority of element: ')
        try:
            priority = int(priority)
            break
        except ValueError:
            print('\nMust be a number in range 1 - 25')

    value = input('input value of element: ')
    data = fetch_data()
    new_element = [{"priority": priority, "value": value}]
    data.extend(new_element)
    queue_sort(data)


def delete_element():
    pass


def search_elements():
    data = fetch_data()
    search_query = input("Search query: ")
    result = []

    print("search results: ")
    try:  # index search
        result.append(data[int(search_query)])
    except (TypeError, ValueError):
        pass

    try:  # priority search
        if 0 < int(search_query) < 26:
            for element in data:
                if int(search_query) == element['priority']:
                    result.append(element)
    except (TypeError, ValueError):
        pass

    for element in data: # value search
        if search_query == element['value']:
            result.append(element)

    display_data(result)


def main_menu():
    while True:
        action = input("Choose an action:\n"
                       "1. Add element to queue\n"
                       "2. Delete an element from queue\n"
                       "3. Search for element in queue\n"
                       "4. Display all elements in queue\n"
                       "5. Stop the program\n")

        print("")
        if action == "1":
            add_element()
        elif action == "2":
            delete_element()
        elif action == "3":
            search_elements()
        elif action == "4":
            display_data(fetch_data())
        elif action == "5":
            break
        else:
            print("invalid option")


if __name__ == '__main__':
    main_menu()
