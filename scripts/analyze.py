import paramiko
from clickhouse_driver import Client
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sshtunnel import SSHTunnelForwarder
from wordcloud import WordCloud, STOPWORDS

#client = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')

#mypkey = paramiko.RSAKey.from_private_key_file('../settings/aws_key.cer')
#sql_hostname = 'localhost'
#sql_username = 'default'
#sql_password = ''
#sql_main_database = 'hh_analyze'
#sql_port = 9000

#ssh_host = 'ec2-3-20-222-181.us-east-2.compute.amazonaws.com'
#ssh_user = 'ubuntu'
#ssh_port = 22


def dependence_wages_city(client):
    """ Средняя зарплата по городам """
    data = client.execute(
        "SELECT city, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY city HAVING salary <= 250000 and currency='RUR' ORDER BY salary")

    df = pd.DataFrame(data, columns=['city', 'salary'])
    print(df)
    fig = px.bar(df, x="city", y="salary", title="Salaries by city")
    fig.show()


def salary_by_city(client, city_name):
    """ Средняя зарплата по определенному городу """
    data = client.execute(
        f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies WHERE city='{city_name}' "
        f"GROUP BY date_local  HAVING salary <= 1000000")

    df = pd.DataFrame(data, columns=['created_at', 'salary'])
    # df = df.groupby(df['created_at'].dt.strftime('%B'))['salary'].mean().reset_index()
    print(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['created_at'], y=df['salary'],
                             mode='lines+markers',
                             name=f'Средняя зарплата, {city_name}'))
    return fig


def word_cloud(client):
    """ Облако слов для высокооплачиваемых вакансий """
    data = client.execute(
        f"SELECT name, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY name HAVING salary >= 500000 and salary <= 1000000")

    df = pd.DataFrame(data, columns=['name', 'salary'])
    text = df['name'].values

    wordcloud = WordCloud(background_color='white', stopwords=set(STOPWORDS)).generate(str(text))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def experience_by_salary(client):
    """Средняя зарплата в зависимости от опыта"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY experience HAVING salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title="Experience")
    fig.show()


def experience_by_salary_city(client, city_name):
    """Средняя зарплата в зависимости от опыта по городу"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY experience HAVING city='{city_name}' and salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title=f"Experience, {city_name}")
    fig.show()


def schedule_by_salary(client):
    data = client.execute(
        "SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  GROUP BY schedule"
    )
    print(data)
    df = pd.DataFrame(data, columns=['schedule', 'salary'])
    print(df)
    fig = px.bar(df, x="schedule", y="salary", title="Schedule")
    fig.show()


def schedule_by_salary_city(client, city_name):
    data = client.execute(
        f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  GROUP BY schedule HAVING city='{city_name}'"
    )
    print(data)
    df = pd.DataFrame(data, columns=['schedule', 'salary'])
    print(df)
    fig = px.bar(df, x="schedule", y="salary", title=f"Schedule, {city_name}")
    fig.show()


#with SSHTunnelForwarder(
#        (ssh_host, ssh_port),
#        ssh_username=ssh_user,
#        ssh_pkey=mypkey,
#        ssh_password='',
#        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
#    client = Client(host='localhost', user=sql_username,
#                    password=sql_password, database=sql_main_database,
#                    port=tunnel.local_bind_port)

# salary_by_city(client, 'Ярославль')
# dependence_wages_city(client)
# word_cloud(client)
# experience_by_salary(client)
# experience_by_salary_city(client, 'Москва')
# schedule_by_salary(client)
