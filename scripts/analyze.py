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
                                 name=f'Средняя зарплата, {city_name}',
                                 line_shape='spline'))
    else:
        data = client.execute(
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)}"
            f"GROUP BY date_local")

        df = pd.DataFrame(data, columns=['created_at', 'salary'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['created_at'], y=df['salary'],
                                 mode='lines+markers',
                                 name=f'Средняя зарплата',
                                 line_shape='spline'))

    return fig


def word_cloud(client, cities):
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
            f"GROUP BY experience order by salary")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary")
    else:
        data = client.execute(
            f"SELECT experience, round(avg(salary_from + salary_to)) as salary FROM vacancies "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY experience order by salary")
        df = pd.DataFrame(data, columns=['experience', 'salary'])
        df = df.dropna()
        print(df)

        df = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(df, x="experience", y="salary")
        fig.update_traces(marker_color='green')

    return fig


def schedule_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от графика работы"""
    if not city_name:
        data = client.execute(
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY schedule ORDER BY salary"
        )
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        df = df.dropna()
        print(df)

        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        fig = px.bar(df, x="schedule", y="salary")
        fig.update_traces(marker_color='green')
    else:
        data = client.execute(
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY schedule order by salary"
        )
        print(data)
        df = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(df)
        fig = px.bar(df, x="schedule", y="salary", title=f"Schedule, {city_name}")

    return fig


def employment_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от типа занятости"""
    if not city_name:
        data = client.execute(
            f"SELECT employment, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY employment ORDER BY salary"
        )
        df = pd.DataFrame(data, columns=['employment', 'salary'])
        df = df.dropna()
        print(df)

        df = pd.DataFrame(data, columns=['employment', 'salary'])
        fig = px.bar(df, x="employment", y="salary")
        fig.update_traces(marker_color='green')
    else:
        data = client.execute(
            f"SELECT employment, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY employment order by salary"
        )
        print(data)
        df = pd.DataFrame(data, columns=['employment', 'salary'])
        print(df)
        fig = px.bar(df, x="employment", y="salary")

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


def popular_city_salary(client, cities):
    """Средняя заработная плата в городах"""
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


def vacancies_by_count(client, city_name, cities):
    """Наиболее востребованные вакансии"""
    if not city_name:
        data = client.execute(
            f"select count(id) as count_vacancies, name from vacancies "
            f"where city in {tuple(cities)}"
            f"group by name order by count_vacancies desc limit 10"
        )
    else:
        data = client.execute(
            f"select count(id) as count_vacancies, name from vacancies "
            f"where city='{city_name}'"
            f"group by name order by count_vacancies desc limit 10"
        )

    df = pd.DataFrame(data, columns=['count', 'vacancies'])
    print(df)
    fig = go.Figure(data=[go.Pie(labels=df['vacancies'], values=df['count'], hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def vacancies_by_salary(client, city_name, cities):
    """Наиболее оплачиваемые вакансии"""
    if not city_name:
        data = client.execute(
            f"select count(id) as count_vacancies, name, round(avg(salary_from + salary_to)) as salary from vacancies "
            f"where city in {tuple(cities)}"
            f"group by name having count_vacancies > 2 order by salary desc limit 10"
        )
    else:
        data = client.execute(
            f"select count(id) as count_vacancies, name, round(avg(salary_from + salary_to)) as salary from vacancies "
            f"where city='{city_name}'"
            f"group by name having count_vacancies > 2 order by salary desc limit 10"
        )

    df = pd.DataFrame(data, columns=['count', 'vacancies', 'salary'])
    print(df)
    fig = go.Figure(data=[go.Pie(labels=df['vacancies'], values=df['salary'], hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def employment_graph(client, city_name, cities):
    """Изменение зарплаты по месяцам в завимисости от типа занятости"""
    if city_name:
        data = client.execute(
            f"SELECT employment, toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local, employment HAVING salary <= 1000000 order by date_local")

    else:
        data = client.execute(
            f"SELECT employment, toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)} GROUP BY date_local, employment ORDER BY date_local")

    df = pd.DataFrame(data, columns=['employment', 'created_at', 'salary'])
    df = df.dropna()

    df_1 = df.loc[df['employment'] == 'Частичная занятость']
    df_2 = df.loc[df['employment'] == 'Полная занятость']
    df_3 = df.loc[df['employment'] == 'Проектная работа']
    df_4 = df.loc[df['employment'] == 'Волонтерство']
    df_5 = df.loc[df['employment'] == 'Стажировка']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1['created_at'], y=df_1['salary'], name="Частичная занятость",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_2['created_at'], y=df_2['salary'], name="Полная занятость",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_3['created_at'], y=df_3['salary'], name="Проектная работа",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_4['created_at'], y=df_4['salary'], name="Волонтерство",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_5['created_at'], y=df_5['salary'], name="Стажировка",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    return fig


def schedule_graph(client, city_name, cities):
    """Изменение зарплаты по месяцам в завимисости от графика"""
    if city_name:
        data = client.execute(
            f"SELECT schedule, toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local, schedule HAVING salary <= 1000000 order by date_local")

    else:
        data = client.execute(
            f"SELECT schedule, toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)} GROUP BY date_local, schedule ORDER BY date_local")

    df = pd.DataFrame(data, columns=['schedule', 'created_at', 'salary'])
    df = df.dropna()

    df_1 = df.loc[df['schedule'] == 'Полный день']
    df_2 = df.loc[df['schedule'] == 'Сменный график']
    df_3 = df.loc[df['schedule'] == 'Гибкий график']
    df_4 = df.loc[df['schedule'] == 'Удаленная работа']
    df_5 = df.loc[df['schedule'] == 'Вахтовый метод']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_1['created_at'], y=df_1['salary'], name="Полный день",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_2['created_at'], y=df_2['salary'], name="Сменный график",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_3['created_at'], y=df_3['salary'], name="Гибкий график",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_4['created_at'], y=df_4['salary'], name="Удаленная работа",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.add_trace(go.Scatter(x=df_5['created_at'], y=df_5['salary'], name="Вахтовый метод",
                             hoverinfo='text+name',
                             line_shape='spline'))
    fig.update_traces(hoverinfo='text+name', mode='lines+markers')
    return fig

# client = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')
# cities = pd.read_csv('../settings/cities.csv')['city']
# schedule_by_salary(client, "", cities)
