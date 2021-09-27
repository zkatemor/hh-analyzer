"""
Веб-приложение
"""
import logging
#import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import paramiko
import sshtunnel
from clickhouse_driver import Client

from scripts.analyze import experience_by_salary, dependence_wages_city, schedule_by_salary, \
    employer_by_count_vacancies, employer_by_salary, high_salary, vacancies_by_count, vacancies_by_salary, \
    employment_graph, employment_by_salary


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

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

cities = pd.read_csv('settings/cities.csv')['city']

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
                  'Изменение зарплаты по месяцам в завимисости от типа занятости'
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
    """ display values """
    open_ssh_tunnel()
    TUNNEL.start()
    open_remote_db()
    #open_local_db()

    if task == 'Средняя зарплата за последние месяцы':
        fig = dependence_wages_city(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от опыта':
        fig = experience_by_salary(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от графика работы':
        fig = schedule_by_salary(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Работодатели с большим количеством открытых вакансий':
        fig = employer_by_count_vacancies(client=CLIENT, city_name=city)
    elif task == 'Работодатели с высокой заработной платой':
        fig = employer_by_salary(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Распределение высокой заработной платы':
        fig = high_salary(client=CLIENT, city_name=city)
    elif task == 'Наиболее востребованные вакансии':
        fig = vacancies_by_count(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Наиболее оплачиваемые вакансии':
        fig = vacancies_by_salary(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Изменение зарплаты по месяцам в завимисости от типа занятости':
        fig = employment_graph(client=CLIENT, city_name=city, cities=cities)
    elif task == 'Средняя зарплата в зависимости от типа занятости':
        fig = employment_by_salary(client=CLIENT, city_name=city, cities=cities)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
