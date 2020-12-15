from clickhouse_driver import Client
import pandas as pd
import plotly.express as px

client = Client(host='localhost', user='default', password='', port='9000', database='hh_analyze')


def dependence_wages_city():
    """ Зарплаты по городам """
    data = client.execute(
        "SELECT city, avg(salary_from + salary_to) as salary FROM vacancies GROUP BY city HAVING salary <= 250000 and currency='RUR' ORDER BY salary")

    df = pd.DataFrame(data, columns=['city', 'salary'])
    print(df)
    fig = px.bar(df, x="city", y="salary", title="Salaries by city")
    fig.show()


dependence_wages_city()
