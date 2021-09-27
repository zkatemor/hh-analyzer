import unittest

import paramiko
import sshtunnel
import logging
import scripts.analyze
import analyze_test
import pandas as pd
from clickhouse_driver import Client

cities = pd.read_csv('../settings/cities.csv')['city']

mypkey = paramiko.RSAKey.from_private_key_file('../settings/aws_key.pem')
SQL_HOSTNAME = 'localhost'
SQL_USERNAME = 'default'
SQL_PASSWORD = ''
SQL_MAIN_DATABASE = 'hh_analyze'
SQL_LOCAL_DATABASE = 'headhunter_salary'
SQL_PORT = 9000

SSH_HOST = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
SSH_USER = 'ubuntu'
SSH_PORT = 22

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

    def test_db_max_salary(self):
        client = open_local_db()
        testMaxSalary = analyze_test.experience_by_salary(client, 'Санкт-Петербург', cities)
        self.assertEqual(testMaxSalary, 148597.67180460042, "Test cities error")

    # def open_ssh_tunnel(self):
    #     """ SSH tunnel """
    #     global TUNNEL
    #     sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    #     TUNNEL = sshtunnel.SSHTunnelForwarder(
    #         (app.SSH_HOST, SSH_PORT),
    #         ssh_username=SSH_USER,
    #         ssh_pkey=mypkey,
    #         ssh_password='',
    #         remote_bind_address=(SQL_HOSTNAME, SQL_PORT)
    #     )
    #     return TUNNEL
    #
    # def test_connection_db(self):
    #     # CLIENT = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')
    #     # try:
    #     #     CLIENT.execute("SELECT * from vacancies")
    #     # except TypeError as err_db:
    #     #     self.fail("Connection failed")
    #     #     self.assertIsNone(db_connection)
    #
    #     """ remote database """
    #     global CLIENT
    #     try:
    #         CLIENT = Client(host='localhost',
    #                     user=SQL_USERNAME,
    #                      password=SQL_PASSWORD,
    #                      database=SQL_MAIN_DATABASE,
    #                      port=TUNNEL.local_bind_port)
    #     except TypeError as err_db:
    #         self.fail("Connection failed")
    #         self.assertIsNone(db_connection)

if __name__ == '__main__':
    unittest.main()