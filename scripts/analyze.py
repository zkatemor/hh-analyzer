"""
Анализ вакансий и представление в диаграммы
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
#from clickhouse_driver import Client
from wordcloud import WordCloud, STOPWORDS


def dependence_wages_city(client, city_name, cities):
    """ Средняя зарплата за последние месяцы """
    if city_name:
        data = client.execute(
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local HAVING salary <= 1000000")

        data_frame = pd.DataFrame(data, columns=['created_at', 'salary'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_frame['created_at'], y=data_frame['salary'],
                                 mode='lines+markers',
                                 name=f'Средняя зарплата, {city_name}',
                                 line_shape='spline'))
    else:
        data = client.execute(
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"where city in {tuple(cities)}"
            f"GROUP BY date_local")

        data_frame = pd.DataFrame(data, columns=['created_at', 'salary'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_frame['created_at'], y=data_frame['salary'],
                                 mode='lines+markers',
                                 name='Средняя зарплата',
                                 line_shape='spline'))

    return fig


def word_cloud(client): # def word_cloud(client, cities):
    """ Облако слов для высокооплачиваемых вакансий """
    data = client.execute(
        "SELECT name, avg(salary_from + salary_to) as salary FROM vacancies "
        "GROUP BY name HAVING salary >= 500000 and salary <= 1000000")

    data_frame = pd.DataFrame(data, columns=['name', 'salary'])
    text = data_frame['name'].values

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
        data_frame = pd.DataFrame(data, columns=['experience', 'salary'])
        fig = px.bar(data_frame, x="experience", y="salary", title=f"Experience, {city_name}")
        #return fig
    else:
        data = client.execute(
            f"SELECT city, experience, round(avg(salary_from + salary_to)) as salary FROM vacancies "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY city, experience order by salary")
        data_frame = pd.DataFrame(data, columns=['city', 'experience', 'salary'])
        print(data_frame)

        df_1 = data_frame.loc[data_frame['experience'] == 'Нет опыта']
        df_2 = data_frame.loc[data_frame['experience'] == 'От 1 года до 3 лет']
        df_3 = data_frame.loc[data_frame['experience'] == 'От 3 до 6 лет']
        df_4 = data_frame.loc[data_frame['experience'] == 'Более 6 лет']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_1['city'],
            x=df_1['salary'],
            name='Нет опыта',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_2['city'],
            x=df_2['salary'],
            name='От 1 года до 3 лет',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_3['city'],
            x=df_3['salary'],
            name='От 3 до 6 лет',
            orientation='h',
            marker=dict(
                color='rgba(255, 99, 71, 0.5)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_4['city'],
            x=df_4['salary'],
            name='Более 6 лет',
            orientation='h',
            marker=dict(
                color='rgba(123, 174, 71, 0.5)'
            )
        ))

        fig.update_layout(barmode='stack')

    return fig


def schedule_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от графика работы"""
    if not city_name:
        data = client.execute(
            f"SELECT city, schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY city, schedule ORDER BY salary"
        )
        data_frame = pd.DataFrame(data, columns=['city', 'schedule', 'salary'])
        data_frame = data_frame.dropna()
        print(data_frame)

        df_1 = data_frame.loc[data_frame['schedule'] == 'Полный день']
        df_2 = data_frame.loc[data_frame['schedule'] == 'Удаленная работа']
        df_3 = data_frame.loc[data_frame['schedule'] == 'Гибкий график']
        df_4 = data_frame.loc[data_frame['schedule'] == 'Сменный график']
        df_5 = data_frame.loc[data_frame['schedule'] == 'Вахтовый метод']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_1['city'],
            x=df_1['salary'],
            name='Полный день',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_2['city'],
            x=df_2['salary'],
            name='Удаленная работа',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_3['city'],
            x=df_3['salary'],
            name='Гибкий график',
            orientation='h',
            marker=dict(
                color='rgba(255, 99, 71, 0.5)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_4['city'],
            x=df_4['salary'],
            name='Сменный график',
            orientation='h',
            marker=dict(
                color='rgba(123, 174, 71, 0.5)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_5['city'],
            x=df_5['salary'],
            name='Вахтовый метод',
            orientation='h',
            marker=dict(
                color='rgba(123, 174, 216, 0.6)'
            )
        ))

        fig.update_layout(barmode='stack')
        # fig = px.bar(df, x="schedule", y="salary", title="Schedule", height=800)
    else:
        data = client.execute(
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY schedule"
        )
        print(data)
        data_frame = pd.DataFrame(data, columns=['schedule', 'salary'])
        print(data_frame)
        fig = px.bar(data_frame, x="schedule", y="salary", title=f"Schedule, {city_name}")

    return fig


def employment_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от типа занятости"""
    if not city_name:
        data = client.execute(
            f"SELECT city, employment, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"where city in {tuple(cities[:30])}"
            f"GROUP BY city, employment ORDER BY salary"
        )
        data_frame = pd.DataFrame(data, columns=['city', 'employment', 'salary'])
        data_frame = data_frame.dropna()
        print(data_frame)

        df_1 = data_frame.loc[data_frame['employment'] == 'Частичная занятость']
        df_2 = data_frame.loc[data_frame['employment'] == 'Полная занятость']
        df_3 = data_frame.loc[data_frame['employment'] == 'Проектная работа']
        df_4 = data_frame.loc[data_frame['employment'] == 'Волонтерство']
        df_5 = data_frame.loc[data_frame['employment'] == 'Стажировка']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_1['city'],
            x=df_1['salary'],
            name='Частичная занятость',
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_2['city'],
            x=df_2['salary'],
            name='Полная занятость',
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_3['city'],
            x=df_3['salary'],
            name='Проектная работа',
            orientation='h',
            marker=dict(
                color='rgba(255, 99, 71, 0.5)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_4['city'],
            x=df_4['salary'],
            name='Волонтерство',
            orientation='h',
            marker=dict(
                color='rgba(123, 174, 71, 0.5)'
            )
        ))

        fig.add_trace(go.Bar(
            y=df_5['city'],
            x=df_5['salary'],
            name='Стажировка',
            orientation='h',
            marker=dict(
                color='rgba(123, 174, 216, 0.6)'
            )
        ))

        fig.update_layout(barmode='stack')
        # fig = px.bar(df, x="schedule", y="salary", title="Schedule", height=800)
    else:
        data = client.execute(
            f"SELECT employment, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY employment"
        )
        print(data)
        data_frame = pd.DataFrame(data, columns=['employment', 'salary'])
        print(data_frame)
        fig = px.bar(data_frame, x="employment", y="salary")

    return fig

############

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
    data_frame = pd.DataFrame(data, columns=['count', 'employer'])
    print(data_frame)
    fig = go.Figure(data=[go.Pie(labels=data_frame['employer'], values=data_frame['count'], hole=.3)])
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

    data_frame = pd.DataFrame(data, columns=['count', 'employer', 'salary'])
    data_frame = data_frame.dropna()
    print(data_frame)
    fig = go.Figure(data=[go.Pie(labels=data_frame['employer'], values=data_frame['salary'], hole=.3)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def popular_city_salary(client): #def popular_city_salary(client, cities):
    """Средняя заработная плата в городах"""
    data = client.execute(
        'select count(id) as count_vacancies, city from headhunter_salary.vacancies '
        'group by city having count_vacancies>=1000 order by count_vacancies desc')

    data_frame = pd.DataFrame(data, columns=['count', 'city'])
    data_frame['city'].to_csv('cities.csv')


def high_salary(client, city_name):
    """Распределение высокой заработной платы"""
    if not city_name:
        city = "" #f""
    else:
        city = f" and city ='{city_name}'"
    data_100 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 80000 and salary_to < 100000{city}"
    )
    data_150 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 100000 and salary_to < 150000{city}"
    )
    data_200 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 150000 and salary_to < 200000{city}"
    )
    data_250 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 200000 and salary_to < 250000{city}"
    )
    data_300 = client.execute(
        f"select count(id) as count_vacancies FROM vacancies "
        f"WHERE currency='RUR' and salary_from >= 250000 and salary_to >= 250000{city}"
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

    data_frame = pd.DataFrame(data, columns=['count', 'vacancies'])
    print(data_frame)
    fig = go.Figure(data=[go.Pie(labels=data_frame['vacancies'], values=data_frame['count'], hole=.3)])
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

    data_frame = pd.DataFrame(data, columns=['count', 'vacancies', 'salary'])
    print(data_frame)
    fig = go.Figure(data=[go.Pie(labels=data_frame['vacancies'], values=data_frame['salary'], hole=.3)])
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

    data_frame = pd.DataFrame(data, columns=['employment', 'created_at', 'salary'])
    data_frame = data_frame.dropna()

    df_1 = data_frame.loc[data_frame['employment'] == 'Частичная занятость']
    df_2 = data_frame.loc[data_frame['employment'] == 'Полная занятость']
    df_3 = data_frame.loc[data_frame['employment'] == 'Проектная работа']
    df_4 = data_frame.loc[data_frame['employment'] == 'Волонтерство']
    df_5 = data_frame.loc[data_frame['employment'] == 'Стажировка']

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

# client = Client(host='localhost', user='default', password='', port='9000', database='headhunter_salary')
# cities = pd.read_csv('../settings/cities.csv')['city']
# schedule_by_salary(client, "", cities)
