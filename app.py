import logging
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import paramiko
import sshtunnel
from clickhouse_driver import Client

from scripts.analyze import experience_by_salary, dependence_wages_city, schedule_by_salary, \
    employer_by_count_vacancies, employer_by_salary, high_salary, vacancies_by_count, vacancies_by_salary, \
    employment_graph, employment_by_salary, schedule_graph

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

mypkey = paramiko.RSAKey.from_private_key_file('settings/aws_key.cer')
sql_hostname = 'localhost'
sql_username = 'default'
sql_password = ''
sql_main_database = 'hh_analyze'
sql_local_database = 'headhunter_salary'
sql_port = 9000

ssh_host = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
ssh_user = 'ubuntu'
ssh_port = 22

cities = pd.read_csv('settings/cities.csv')['city']


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


def open_local_db():
    global client
    client = Client(host='localhost',
                    user=sql_username,
                    password=sql_password,
                    database=sql_local_database,
                    port=sql_port)
    return client


app.layout = html.Div([
    html.H2('Job Analysis at Headhunter'),
    dcc.Dropdown(
        id='city',
        options=[{'label': i, 'value': i} for i in
                 cities],
        value=''
    ),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in
                 ['Средняя зарплата за последние месяцы',
                  'Средняя зарплата в зависимости от опыта',
                  'Средняя зарплата в зависимости от графика работы',
                  'Средняя зарплата в зависимости от типа занятости',
                  'Работодатели с большим количеством открытых вакансий',
                  'Работодатели с высокой заработной платой',
                  'Распределение высокой заработной платы',
                  'Наиболее востребованные вакансии',
                  'Наиболее оплачиваемые вакансии',
                  'Изменение зарплаты по месяцам в завимисости от типа занятости',
                  'Изменение зарплаты по месяцам в завимисости от графика работы'
                  ]],
        value='Средняя зарплата за последние месяцы',
        clearable=False
    ),
    dcc.Graph(id="graph", style={'height': '80vh'}),
],
    style={'display': 'inline-block', 'width': '100%', 'height': '100%'})


@app.callback(dash.dependencies.Output('graph', 'figure'),
              [dash.dependencies.Input('dropdown', 'value'),
               dash.dependencies.Input('city', 'value')])
def display_value(task, city):
    open_ssh_tunnel()
    tunnel.start()
    open_remote_db()
    # open_local_db()

    if task == 'Средняя зарплата за последние месяцы':
        fig = dependence_wages_city(client=client, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от опыта':
        fig = experience_by_salary(client=client, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от графика работы':
        fig = schedule_by_salary(client=client, city_name=city, cities=cities)
    elif task == 'Работодатели с большим количеством открытых вакансий':
        fig = employer_by_count_vacancies(client=client, city_name=city)
    elif task == 'Работодатели с высокой заработной платой':
        fig = employer_by_salary(client=client, city_name=city, cities=cities)
    elif task == 'Распределение высокой заработной платы':
        fig = high_salary(client=client, city_name=city)
    elif task == 'Наиболее востребованные вакансии':
        fig = vacancies_by_count(client=client, city_name=city, cities=cities)
    elif task == 'Наиболее оплачиваемые вакансии':
        fig = vacancies_by_salary(client=client, city_name=city, cities=cities)
    elif task == 'Изменение зарплаты по месяцам в завимисости от типа занятости':
        fig = employment_graph(client=client, city_name=city, cities=cities)
    elif task == 'Изменение зарплаты по месяцам в завимисости от графика работы':
        fig = schedule_graph(client=client, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от типа занятости':
        fig = employment_by_salary(client=client, city_name=city, cities=cities)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
