import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from clickhouse_driver import Client
from wordcloud import WordCloud, STOPWORDS


def dependence_wages_city(client, city_name, cities):
    """ Средняя зарплата за последние месяцы """
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
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)}"
            f"GROUP BY date_local")

        df = pd.DataFrame(data, columns=['created_at', 'salary'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['created_at'], y=df['salary'],
                                 mode='lines+markers',
                                 name=f'Средняя зарплата'))

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


def experience_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от опыта"""
    if city_name:
        data = client.execute(
            f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY experience")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary", title=f"Experience, {city_name}", height=800)
        return fig
    else:
        data = client.execute(
            f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)}"
            f"GROUP BY experience")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary", title="Experience", height=800)

    return fig


def schedule_by_salary(client, city_name, cities):
    """Средняя зарплата по графику работы"""
    if not city_name:
        data = client.execute(
            "SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"where city in {tuple(cities)}"
            "GROUP BY schedule"
        )
        print(data)
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(df)
        fig = px.bar(df, x="schedule", y="salary", title="Schedule", height=800)
    else:
        data = client.execute(
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY schedule"
        )
        print(data)
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(df)
        fig = px.bar(df, x="schedule", y="salary", title=f"Schedule, {city_name}", height=800)

    return fig


def employer_by_count_vacancies(client, city_name):
    """Работодатели с большим количеством открытых вакансий"""
    if not city_name:
        data = client.execute(
            'select count(id) as count_vacancies, employer from vacancies '
            'group by employer order by count_vacancies desc limit 15'
        )
    else:
        data = client.execute(
            f"select count(id) as count_vacancies, employer from vacancies "
            f"where city='{city_name}'"
            f"group by employer order by count_vacancies desc limit 15"
        )
    df = pd.DataFrame(data, columns=['count', 'employer'])
    print(df)
    fig = go.Figure(data=[go.Pie(labels=df['employer'], values=df['count'], hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def employer_by_salary(client, city_name, cities):
    """Работодатели с высокой заработной платой"""
    if not city_name:
        data = client.execute(
            f"select count(id) as count_vacancies, employer, round(avg(salary_from + salary_to)) as salary from vacancies "
            f"where city in {tuple(cities)}"
            f"group by employer order by salary desc limit 15"
        )
    else:
        data = client.execute(
            f"select count(id) as count_vacancies, employer, round(avg(salary_from + salary_to)) as salary from vacancies "
            f"where city='{city_name}'"
            f"group by employer order by salary desc limit 15"
        )

    df = pd.DataFrame(data, columns=['count', 'employer', 'salary'])
    df = df.dropna()
    print(df)
    fig = go.Figure(data=[go.Pie(labels=df['employer'], values=df['salary'], hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def popular_city(client):
    data = client.execute(
        'select count(id) as count_vacancies, city from headhunter_salary.vacancies '
        'group by city having count_vacancies>=1000 order by count_vacancies desc')

    df = pd.DataFrame(data, columns=['count', 'city'])
    df['city'].to_csv('cities.csv')


def high_salary(client, city_name):
    """Распределение высокой заработной платы"""
    if not city_name:
        w = f""
    else:
        w = f" and city ='{city_name}'"
    data_100 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 80000 and salary_to < 100000{w}"
    )
    data_150 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 100000 and salary_to < 150000{w}"
    )
    data_200 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 150000 and salary_to < 200000{w}"
    )
    data_250 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 200000 and salary_to < 250000{w}"
    )
    data_300 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 250000 and salary_to >= 250000{w}"
    )
    labels = ['80-100тыс.', '100-150тыс.', '150-200тыс.', '200-250тыс.', '250тыс. и более']
    values = [data_100[0][0], data_150[0][0], data_200[0][0], data_250[0][0], data_300[0][0]]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

# client = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')
# employer_by_salary(client, "Москва")
