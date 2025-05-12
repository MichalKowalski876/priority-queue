import json
from time import time

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
        fh = open("queue_test.json")
        queue = json.load(fh)
        return queue

    except FileExistsError:
        with open('queue_test.json', 'w') as fh:
            json.dump([], fh)
            fetch_data()

            # save_data([]) # change in final version

def save_data(data):
    with open('queue.json', 'w') as f:
        json.dump(data, f)


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
    display_data(data)

@timer
def display_data(data):
    print('Index no.     Priority     Value')
    display_space = '            '
    for value in range(len(data)):
        data_dictionary = data[value]
        print(str((value + 1)) + display_space + " " + str(data_dictionary["priority"]) + display_space + str(
            data_dictionary["value"]))

def add_element(user_input):
    pass

def delete_element(user_input):
    pass

def display_elements(user_input):
    pass

def main_menu():
    pass


if __name__ == '__main__':
    display_data(fetch_data())
