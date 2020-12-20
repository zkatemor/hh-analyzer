import logging
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import paramiko
import sshtunnel
from clickhouse_driver import Client

from scripts.analyze import salary_by_city, experience_by_salary, dependence_wages_city, experience_by_salary_city

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

mypkey = paramiko.RSAKey.from_private_key_file('settings/aws_key.cer')
sql_hostname = 'localhost'
sql_username = 'default'
sql_password = ''
sql_main_database = 'hh_analyze'
sql_port = 9000

ssh_host = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
ssh_user = 'ubuntu'
ssh_port = 22


def open_ssh_tunnel():
    global tunnel
    sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    tunnel = sshtunnel.SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_pkey=mypkey,
        ssh_password='',
        remote_bind_address=(sql_hostname, sql_port)
    )
    return tunnel


def open_remote_db():
    global client
    client = Client(host='localhost',
                    user=sql_username,
                    password=sql_password,
                    database=sql_main_database,
                    port=tunnel.local_bind_port)
    return client


app.layout = html.Div([
    html.H2('Job Analysis at Headhunter'),
    dcc.Dropdown(
        id='city',
        options=[{'label': i, 'value': i} for i in
                 ['Москва', 'Воронеж', 'Санкт-Петербург']],
        value='Москва'
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in
                 ['Средняя зарплата по городам',
                  'Средняя зарплата по определенному городу',
                  'Средняя зарплата в зависимости от опыта',
                  'Средняя зарплата в зависимости от опыта по городу'
                  ]],
        value='Средняя зарплата по городам'
    ),
    dcc.Graph(id="graph"),
])


@app.callback(dash.dependencies.Output('graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value'),
               dash.dependencies.Input('city', 'value')])
def display_value(task, city):
    open_ssh_tunnel()
    tunnel.start()
    open_remote_db()

    if task == 'Средняя зарплата по городам':
        fig = dependence_wages_city(client=client)
    elif task == 'Средняя зарплата по определенному городу':
        fig = salary_by_city(client=client, city_name=city)
    elif task == 'Средняя зарплата в зависимости от опыта':
        fig = experience_by_salary(client=client)
    elif task == 'Средняя зарплата в зависимости от опыта по городу':
        fig = experience_by_salary_city(client=client, city_name=city)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
