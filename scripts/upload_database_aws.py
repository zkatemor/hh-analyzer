import json
import os
import paramiko
from sshtunnel import SSHTunnelForwarder
from clickhouse_driver import Client
from datetime import datetime

mypkey = paramiko.RSAKey.from_private_key_file('../settings/aws_key.cer')
sql_hostname = 'localhost'
sql_username = 'default'
sql_password = ''
sql_main_database = 'hh_analyze'
sql_port = 9000

ssh_host = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
ssh_user = 'ubuntu'
ssh_port = 22

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        ssh_password='',
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    client = Client(host='localhost', user=sql_username,
                    password=sql_password, database=sql_main_database,
                    port=tunnel.local_bind_port)

    for v in range(1, 4):
        list_files = os.listdir(path=f'../vacancies_{v}/')
        print(list_files)

        for file_name in list_files:
            with open(f'../vacancies_{v}/' + file_name) as json_file:
                vacancy = json.load(json_file)
                # print(vacancy)

                for i in range(0, len(vacancy)):
                    try:
                        try:
                            salary_gross = int(vacancy[i]['salary_gross'])
                        except TypeError as E:
                            salary_gross = "cast(Null as Nullable(UInt8))"

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

                        vacancies_short_list = [vacancy[i]['name'], vacancy[i]['salary_from'], vacancy[i]['salary_to'],
                                                vacancy[i]['currency'],
                                                salary_gross, vacancy[i]['experience'],
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
