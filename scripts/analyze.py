from clickhouse_driver import Client
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

client = Client(host='localhost', user='default', password='', port='9000', database='hh_analyze')


def dependence_wages_city():
    """ Средняя зарплата по городам """
    data = client.execute(
        "SELECT city, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY city HAVING salary <= 250000 and currency='RUR' ORDER BY salary")

    df = pd.DataFrame(data, columns=['city', 'salary'])
    print(df)
    fig = px.bar(df, x="city", y="salary", title="Salaries by city")
    fig.show()


def salary_by_city(city_name):
    """ Средняя зарплата по определенному городу """
    data = client.execute(
        f"SELECT created_at, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY created_at HAVING city='{city_name}' and salary <= 1000000")

    df = pd.DataFrame(data, columns=['created_at', 'salary'])
    df = df.groupby(df['created_at'].dt.strftime('%B'))['salary'].mean().reset_index()
    print(df)
    fig = px.bar(df, x="created_at", y="salary", title=f'Средняя зарплата, {city_name}')
    fig.show()


def word_cloud():
    """ Облако слов для высокооплачиваемых вакансий """
    data = client.execute(
        f"SELECT name, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY name HAVING salary >= 500000 and salary <= 1000000")

    df = pd.DataFrame(data, columns=['name', 'salary'])
    text = df['name'].values

    wordcloud = WordCloud(background_color='white', stopwords=set(STOPWORDS)).generate(str(text))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


def experience_by_salary():
    """Средняя зарплата в зависимости от опыта"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY experience HAVING salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title="Experience")
    fig.show()


def experience_by_salary_city(city_name):
    """Средняя зарплата в зависимости от опыта по городу"""
    data = client.execute(
        f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY experience HAVING city='{city_name}' and salary <= 1000000")
    print(data)
    df = pd.DataFrame(data, columns=['experience', 'salary'])
    print(df)
    fig = px.bar(df, x="experience", y="salary", title=f"Experience, {city_name}")
    fig.show()


def schedule_by_salary():
    data = client.execute(
        "SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  GROUP BY schedule"
    )
    print(data)
    df = pd.DataFrame(data, columns=['schedule', 'salary'])
    print(df)
    fig = px.bar(df, x="schedule", y="salary", title="Schedule")
    fig.show()


def schedule_by_salary_city(city_name):
    data = client.execute(
        f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  GROUP BY schedule HAVING city='{city_name}'"
    )
    print(data)
    df = pd.DataFrame(data, columns=['schedule', 'salary'])
    print(df)
    fig = px.bar(df, x="schedule", y="salary", title=f"Schedule, {city_name}")
    fig.show()


# dependence_wages_city()
# salary_by_city('Воронеж')
# word_cloud()
# experience_by_salary()
# experience_by_salary_city('Москва')
# schedule_by_salary()
schedule_by_salary_city('Воронеж')
