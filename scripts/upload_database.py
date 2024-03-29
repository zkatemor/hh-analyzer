import json
import os
from clickhouse_driver import Client
from datetime import datetime

client = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')
client.execute("SELECT * from vacancies")

for v in range(1, 4):
    list_files = os.listdir(path=f'../vacan_{v}/')
    print(list_files)

    for file_name in list_files:
        with open(f'../vacan_{v}/' + file_name) as json_file:
            vacancy = json.load(json_file)

            for i in range(0, len(vacancy)):
                try:
                    try:
                        salary_to = float(vacancy[i]['salary_to'])
                    except TypeError as E:
                        salary_to = "cast(Null as Nullable(Float64))"

                    try:
                        salary_from = float(vacancy[i]['salary_from'])
                    except TypeError as E:
                        salary_from = "cast(Null as Nullable(Float64))"

                    created_at = vacancy[i]['created_at']
                    created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                    employer_name = vacancy[i]['employer'].replace("'", "").replace('"', '')

                    vacancies_short_list = [vacancy[i]['id'], vacancy[i]['name'], vacancy[i]['salary_from'], vacancy[i]['salary_to'],
                                            vacancy[i]['currency'], vacancy[i]['experience'],
                                            vacancy[i]['schedule'],
                                            created_at, employer_name, vacancy[i]['employment'],
                                            vacancy[i]['city'], vacancy[i]['area_url'], vacancy[i]['area_id'],
                                            vacancy[i]['area_name']
                                            ]
                    # for index, item in enumerate(vacancies_short_list):
                    #    if item is None:
                    #        vacancies_short_list[index] = ""
                    tuple_to_insert = tuple(vacancies_short_list)
                    print(tuple_to_insert)
                    client.execute('INSERT INTO vacancies VALUES', [tuple_to_insert])
                except Exception as e:
                    print(str(e))
