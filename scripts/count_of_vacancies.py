"""
Счетчик вакансий
"""
import json
import os

COUNT = 0

for i in range(1, 4):
    list_files = os.listdir(path=f'../vacancies_{i}/')
    print(list_files)

    for file_name in list_files:
        with open(f'../vacancies_{i}/' + file_name) as json_file:
            data = json.load(json_file)
            COUNT += len(data)

print(COUNT)
