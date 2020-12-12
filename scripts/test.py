import paramiko
from sshtunnel import SSHTunnelForwarder
from clickhouse_driver import connect

mypkey = paramiko.RSAKey.from_private_key_file('../settings/aws_key.cer')
sql_hostname = 'localhost'
sql_username = 'default'
sql_password = ''
sql_main_database = 'test'
sql_port = 9000

ssh_host = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
ssh_user = 'ubuntu'
ssh_port = 22

SQL_OPTIMIZE = 'OPTIMIZE TABLE test_table1'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        ssh_password='',
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = connect(host='localhost', user=sql_username,
                   password=sql_password, database=sql_main_database,
                   port=tunnel.local_bind_port)

    cursor = conn.cursor()
    cursor.execute('SHOW TABLES')
    #cursor.execute('SELECT * FROM test_table')

    #cursor.executemany('INSERT INTO test_table (test_column1, test_column2) VALUES',
    #                   [{'test_column1': 25, 'test_column2': 'test25'}])

    cursor.executemany('INSERT INTO test_table1 VALUES', [(55, 'test55')])
    cursor.executemany('INSERT INTO test_table1 VALUES', [(55, 'test55')])
    cursor.executemany('INSERT INTO test_table1 VALUES', [(55, 'test55')])
    cursor.executemany('INSERT INTO test_table1 VALUES', [(544, 'test544')])
    cursor.executemany('INSERT INTO test_table1 VALUES', [(55, 'test55')])
    cursor.executemany('INSERT INTO test_table1 VALUES', [(55, 'test55')])
    cursor.execute(SQL_OPTIMIZE)
    cursor.execute('SELECT * FROM test_table1')
    print(cursor.fetchall())
