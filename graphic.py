import pandas as pd
import plotly.graph_objects as go

from connect import open_ssh_tunnel, open_remote_db


class Graphic:
    def __init__(self):
        self.server = open_ssh_tunnel()
        self.server.start()
        self.client = open_remote_db()

    def salary_by_city(self, city_name):
        """ Средняя зарплата по определенному городу """
        data = self.client.execute(
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local  HAVING salary <= 1000000")

        df = pd.DataFrame(data, columns=['created_at', 'salary'])
        print(df)
        return df
