import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS


def dependence_wages_city(client):
    """ Средняя зарплата по городам """
    data = client.execute(
        "SELECT city, avg(salary_from + salary_to) as salary FROM vacancies "
        "WHERE currency='RUR' GROUP BY city "
        "HAVING salary <= 250000 ORDER BY salary")

    df = pd.DataFrame(data, columns=['city', 'salary'])
    print(df)
    fig = px.bar(df, x="city", y="salary", title="Salaries by city")
    return fig


def salary_by_city(client, city_name):
    """ Средняя зарплата по определенному городу """
    data = client.execute(
        f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
        f"WHERE city='{city_name}' "
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
        f"SELECT name, avg(salary_from + salary_to) as salary FROM vacancies "
        f"GROUP BY name HAVING salary >= 500000 and salary <= 1000000")

    df = pd.DataFrame(data, columns=['name', 'salary'])
    text = df['name'].values

    wordcloud = WordCloud(background_color='white', stopwords=set(STOPWORDS)).generate(str(text))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def experience_by_salary(client):
    """Средняя зарплата в зависимости от опыта"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
        f"GROUP BY experience HAVING salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title="Experience")
    return fig


def experience_by_salary_city(client, city_name):
    """Средняя зарплата в зависимости от опыта по городу"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
        f"WHERE city='{city_name}' "
        f"GROUP BY experience HAVING salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title=f"Experience, {city_name}")
    return fig


def schedule_by_salary(client):
    """Средняя зарплата по графику работы"""
    data = client.execute(
        "SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
        "GROUP BY schedule"
    )
    print(data)
    df = pd.DataFrame(data, columns=['schedule', 'salary'])
    print(df)
    fig = px.bar(df, x="schedule", y="salary", title="Schedule")
    return fig


def schedule_by_salary_city(client, city_name):
    """Средняя зарплата по графику работы в определенном городе"""
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
