import json

def fetch_data():
    fh = open("queue_test.json")
    queue = json.load(fh)

    return queue

def save_data(data):
    with open('queue.json', 'w') as f:
        json.dump(data, f)

def display_data(data):
    print('Index no.     Priority     Value')
    display_space = '            '
    for value in range(len(data)):
        data_dictionary = data[value]
        print(str((value + 1)) + display_space + " " + str(data_dictionary["priority"]) + display_space + str(data_dictionary["value"]) + display_space)


if __name__ == '__main__':
    save_data(fetch_data())
