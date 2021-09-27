"""
Загрузка вакансий в базу данных на удаленный сервер
"""
import json
import os
from datetime import datetime
import paramiko
from sshtunnel import SSHTunnelForwarder
from clickhouse_driver import Client
from scripts.upload_database import vacancies_short_list

mypkey = paramiko.RSAKey.from_private_key_file('../settings/aws_key.pem')
SQL_HOSTNAME = 'localhost'
SQL_USERNAME = 'default'
SQL_PASSWORD = ''
SQL_MAIN_DATABASE = 'hh_analyze'
SQL_PORT = 9000

SSH_HOST = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
SSH_USER = 'ubuntu'
SSH_PORT = 22

with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_pkey=mypkey,
        ssh_password='',
        remote_bind_address=(SQL_HOSTNAME, SQL_PORT)) as TUNNEL:
    CLIENT = Client(host='localhost', user=SQL_USERNAME,
                    password=SQL_PASSWORD, database=SQL_MAIN_DATABASE,
                    port=TUNNEL.local_bind_port)

    for v in range(1, 4):
        list_files = os.listdir(path=f'../vacancies_{v}/')
        print(list_files)

        for file_name in list_files:
            with open(f'../vacancies_{v}/' + file_name) as json_file:
                vacancy = json.load(json_file)
                # print(vacancy)

                #for i in range(0, len(vacancy)):
                for i in enumerate(vacancy):
                    #try:
                    try:
                        SALARY_GROSS = int(vacancy[i]['salary_gross'])
                    except TypeError as err:
                        SALARY_GROSS = "cast(Null as Nullable(UInt8))"

                    try:
                        SALARY_TO = float(vacancy[i]['salary_to'])
                    except TypeError as err:
                        SALARY_TO = "cast(Null as Nullable(Float64))"

                    try:
                        SALARY_FROM = float(vacancy[i]['salary_from'])
                    except TypeError as err:
                        SALARY_FROM = "cast(Null as Nullable(Float64))"

                    created_at = vacancy[i]['created_at']
                    created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S%z')
                    employer_name = vacancy[i]['employer'].replace("'", "").replace('"', '')

                    #vacancies_short_list = [vacancy[i]['name'], vacancy[i]['salary_from'], vacancy[i]['salary_to'],
                    #                        vacancy[i]['currency'],
                    #                        SALARY_GROSS, vacancy[i]['experience'],
                    #                        vacancy[i]['schedule'],
                    #                        created_at, employer_name, vacancy[i]['employment'],
                    #                        vacancy[i]['city'], vacancy[i]['area_url'], vacancy[i]['area_id'],
                    #                        vacancy[i]['area_name']
                    #                        ]
                    # for index, item in enumerate(vacancies_short_list):
                    #    if item is None:
                    #        vacancies_short_list[index] = ""
                    tuple_to_insert = tuple(vacancies_short_list)
                    print(tuple_to_insert)
                    CLIENT.execute('INSERT INTO vacancies VALUES', [tuple_to_insert])
                    #except Exception as err_:
                    print(str(err))
