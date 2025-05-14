import json
from random import randint
from time import time

class Task:
    def __init__(self, priority: int, value: str):
        self.priority = priority
        self.value = value

class QueueManager:
    def __init__(self, file_name = 'queue.json'):
        self.file_name = file_name
        self.queue = self.load_data()

def main():
    pass

if __name__ == '__main__':
    main()