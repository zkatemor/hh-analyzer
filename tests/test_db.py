import unittest

import paramiko
import sshtunnel
import logging
import analyze_test
from clickhouse_driver import Client

mypkey = paramiko.RSAKey.from_private_key_file('settings/aws_key.pem')
SQL_HOSTNAME = 'localhost'
SQL_USERNAME = 'default'
SQL_PASSWORD = ''
SQL_MAIN_DATABASE = 'hh_analyze'
SQL_LOCAL_DATABASE = 'headhunter_salary'
SQL_PORT = 9000

SSH_HOST = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
SSH_USER = 'ubuntu'
SSH_PORT = 22

def open_ssh_tunnel():
    """ SSH tunnel """
    global TUNNEL
    sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    TUNNEL = sshtunnel.SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        ssh_pkey=mypkey,
        ssh_password='',
        remote_bind_address=(SQL_HOSTNAME, SQL_PORT)
    )
    return TUNNEL


def open_remote_db():
    """ remote database """
    #open_ssh_tunnel()
    global CLIENT
    CLIENT = Client(host='localhost',
                    user=SQL_USERNAME,
                    password=SQL_PASSWORD,
                    database=SQL_MAIN_DATABASE,
                    port=TUNNEL.local_bind_port)
    return CLIENT

def open_local_db():
    """ open local database """
    global CLIENT
    CLIENT = Client(host='localhost',
                    user=SQL_USERNAME,
                    password=SQL_PASSWORD,
                    database=SQL_LOCAL_DATABASE,
                    port=SQL_PORT)
    return CLIENT

class TestApplication(unittest.TestCase):

    open_ssh_tunnel()
    TUNNEL.start()
    global client
    client = open_remote_db()

    def test_dependence_wages_city(self):
        testMaxSalary = analyze_test.dependence_wages_city(client, 'Санкт-Петербург', analyze_test.cities)
        self.assertEqual(testMaxSalary, [(155173.91304347827,)])

    def test_word_cloud(self):
        testMaxSalary = analyze_test.word_cloud(client)
        self.assertEqual(testMaxSalary, 'Юрист по работе с тендерами')

    def test_experience_by_salary(self):
        testMaxSalary = analyze_test.experience_by_salary(client, 'Санкт-Петербург', analyze_test.cities)
        self.assertEqual(testMaxSalary, [(148597.67180460042,)])

    def test_schedule_by_salary(self):
        testMaxSalary = analyze_test.schedule_by_salary(client, 'Санкт-Петербург', analyze_test.cities)
        self.assertEqual(testMaxSalary, 155405.06072874495)

    def test_employment_by_salary(self):
        testMaxSalary = analyze_test.employment_by_salary(client, 'Санкт-Петербург', analyze_test.cities)
        self.assertEqual(testMaxSalary, 'Частичная занятость')

    def test_employer_by_count_vacancies(self):
        testMaxSalary = analyze_test.employer_by_count_vacancies(client, 'Санкт-Петербург')
        self.assertEqual(testMaxSalary, 'ЭКСПРЕСС')

    def test_employer_by_salary(self):
        testMaxSalary = analyze_test.employer_by_salary(client, 'Санкт-Петербург', analyze_test.cities)
        self.assertEqual(testMaxSalary, 'Эстейт Маркет')

    def test_popular_city_salary(self):
        testMaxSalary = analyze_test.popular_city_salary(client)
        self.assertEqual(testMaxSalary, 94)


if __name__ == '__main__':
    unittest.main()