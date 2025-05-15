import json
from time import time
from random import randint


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f'{func.__name__} took {end_time - start_time:.6f} seconds\n')
        return result
    return wrapper


class PriorityQueue:
    def __init__(self, filename='queue.json'):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as fh:
                return json.load(fh)
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            self.save_data([])
            return []

    def save_data(self, data=None):
        if data is not None:
            self.data = data
        with open(self.filename, 'w') as fh:
            json.dump(self.data, fh)

    def sort_queue(self):
        swap = False
        data_length = len(self.data)
        for index in range(data_length):
            for pri_val in range(0, data_length - index - 1):
                if self.data[pri_val]['priority'] > self.data[pri_val + 1]['priority']:
                    self.data[pri_val]['priority'], self.data[pri_val + 1]['priority'] = \
                        self.data[pri_val + 1]['priority'], self.data[pri_val]['priority']
                    swap = True
            if not swap:
                break
        self.save_data()

    @timer
    def display(self, items=None):
        if items is None:
            items = self.data
        print('{:<7} {:<9} {}'.format('Index', 'Priority', 'Value'))
        for idx, item in enumerate(items, start=1):
            print('{:<7} {:<9} {}'.format(idx, item['priority'], item['value']))
        print()

    @timer
    def add(self, new_elements):
        self.data.extend(new_elements)
        self.sort_queue()

    def add_elements(self):
        while True:
            variant = input('1. Add custom element\n'
                            '2. Add random elements\n'
                            '3. Return to main menu\n\n')
            if variant == '1':
                priority = int(input('Input priority of element: '))
                value = input('Input value of element: ')
                self.add([{'priority': priority, 'value': value}])
            elif variant == '2':
                amount = int(input('How many elements do you want to add?: '))
                new_randoms = [{'priority': randint(1, 25), 'value': f'task {randint(1, 999)}'} for _ in range(amount)]
                self.add(new_randoms)
            elif variant == '3':
                return
            else:
                print('Invalid option\n')

    @timer
    def delete_by_index(self, index):
        try:
            del self.data[index]
            self.sort_queue()
        except IndexError:
            print('Invalid index.')

    @timer
    def delete_by_priority(self, priority):
        self.data = [item for item in self.data if item['priority'] != priority]
        self.sort_queue()

    @timer
    def delete_by_value(self, value):
        self.data = [item for item in self.data if item['value'] != value]
        self.sort_queue()

    def delete_elements(self):
        while True:
            variant = input('1. Delete single entry by index\n'
                            '2. Delete group by priority\n'
                            '3. Delete group by value\n'
                            '4. Return to main menu\n\n')
            if variant == '1':
                idx = int(input('Index to delete: ')) - 1
                self.delete_by_index(idx)
            elif variant == '2':
                prio = int(input('Priority to delete: '))
                self.delete_by_priority(prio)
            elif variant == '3':
                val = input('Value to delete: ')
                self.delete_by_value(val)
            elif variant == '4':
                return
            else:
                print('Invalid option\n')

    def search_elements(self):
        query = input('Search query (!exit to return to main menu): ')
        if query != '!exit':
            self.search(query)

    @timer
    def search(self, query):
        results = []
        try:
            results.append(self.data[int(query) - 1])
        except (ValueError, IndexError):
            pass
        try:
            results += [x for x in self.data if x['priority'] == int(query)]
        except ValueError:
            pass
        results += [x for x in self.data if x['value'] == query]
        print('Search results:')
        self.display(results)


def main_menu():
    queue = PriorityQueue()
    while True:
        action = input('Choose an action:\n'
                       '1. Add element to queue\n'
                       '2. Delete an element from queue\n'
                       '3. Search for element in queue\n'
                       '4. Display all elements in queue\n'
                       '5. Stop the program\n\n')
        if action == '1':
            queue.add_elements()
        elif action == '2':
            queue.delete_elements()
        elif action == '3':
            queue.search_elements()
        elif action == '4':
            queue.display()
        elif action == '5':
            break
        else:
            print('Invalid option\n')


if __name__ == '__main__':
    main_menu()
