import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from clickhouse_driver import Client
from wordcloud import WordCloud, STOPWORDS


def dependence_wages_city(client, city_name):
    """ Средняя зарплата по городам """
    if city_name:
        data = client.execute(
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local HAVING salary <= 1000000")

        df = pd.DataFrame(data, columns=['created_at', 'salary'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['created_at'], y=df['salary'],
                                 mode='lines+markers',
                                 name=f'Средняя зарплата, {city_name}'))
    else:
        data = client.execute(
            "SELECT count(id) as count_vacancies, city, avg(salary_from + salary_to) as salary FROM vacancies "
            "WHERE currency='RUR' GROUP BY city "
            "HAVING salary >= 50000 and count_vacancies>=1000 ORDER BY salary")

        df = pd.DataFrame(data, columns=['count', 'city', 'salary'])
        fig = px.bar(df, x="city", y="salary", title="Salaries by city", height=800)

    return fig


def word_cloud(client):
    """ Облако слов для высокооплачиваемых вакансий """
    data = client.execute(
        f"SELECT name, avg(salary_from + salary_to) as salary FROM vacancies "
        f"GROUP BY name HAVING salary >= 500000 and salary <= 1000000")

    df = pd.DataFrame(data, columns=['name', 'salary'])
    text = df['name'].values

    wordcloud = WordCloud(background_color='white', stopwords=set(STOPWORDS)).generate(str(text))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def experience_by_salary(client, city_name):
    """Средняя зарплата в зависимости от опыта"""
    if city_name:
        data = client.execute(
            f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY experience HAVING salary <= 1000000")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary", title=f"Experience, {city_name}")
        return fig
    else:
        data = client.execute(
            f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
            f"GROUP BY experience HAVING salary <= 1000000")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary", title="Experience")

    return fig


def schedule_by_salary(client, city_name):
    """Средняя зарплата по графику работы"""
    if not city_name:
        data = client.execute(
            "SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            "GROUP BY schedule"
        )
        print(data)
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(df)
        fig = px.bar(df, x="schedule", y="salary", title="Schedule")
    else:
        data = client.execute(
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY schedule"
        )
        print(data)
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(df)
        fig = px.bar(df, x="schedule", y="salary", title=f"Schedule, {city_name}")

    return fig


def popular_city(client):
    data = client.execute(
        'select count(id) as count_vacancies, city from headhunter_salary.vacancies '
        'group by city having count_vacancies>=1000 order by count_vacancies desc')

    df = pd.DataFrame(data, columns=['count', 'city'])
    df['city'].to_csv('cities.csv')
