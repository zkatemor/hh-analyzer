import pandas as pd

cities = pd.read_csv('settings/cities.csv')['city']

def dependence_wages_city(client, city_name, cities):
    """ Средняя зарплата за последние месяцы """
    if city_name:
        data = client.execute(
            f"SELECT max(salary) as val from("
            f"SELECT toDate(created_at) as date_local, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY date_local HAVING salary <= 1000000)")

        return data


def word_cloud(client): # def word_cloud(client, cities):
    """ Облако слов для высокооплачиваемых вакансий """
    data = client.execute(
        f"SELECT max(name) as val from("
        "SELECT name, avg(salary_from + salary_to) as salary FROM vacancies "
        "GROUP BY name HAVING salary >= 500000 and salary <= 1000000)")

    return data[0][0]


def experience_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от опыта"""
    if city_name:
        data = (client.execute(
            f"SELECT max(salary) as val from("
            f"SELECT experience, avg(salary_from + salary_to) as salary FROM vacancies "
            f"WHERE city='{city_name}' "
            f"GROUP BY experience having experience ='От 3 до 6 лет')"))
        value = data

        return value


def schedule_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от графика работы"""
    if city_name:
        data = client.execute(
            f"SELECT max(salary) as val from("
            f"SELECT schedule, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY schedule)"
        )

    return data[0][0]


def employment_by_salary(client, city_name, cities):
    """Средняя зарплата в зависимости от типа занятости"""
    if city_name:
        data = client.execute(
            f"SELECT max(employment) as val from("
            f"SELECT employment, avg(salary_from + salary_to) as salary FROM vacancies  "
            f"WHERE city='{city_name}' "
            f"GROUP BY employment)"
        )

    return data[0][0]


def employer_by_count_vacancies(client, city_name):
    """Работодатели с большим количеством открытых вакансий"""
    if city_name:
        data = client.execute(
            f"SELECT max(employer) as val from("
            f"select count(id) as count_vacancies, employer from vacancies "
            f"where city='{city_name}'"
            f"group by employer order by count_vacancies desc limit 15)"
        )

    return data[0][0]

def employer_by_salary(client, city_name, cities):
    """Работодатели с высокой заработной платой"""
    if city_name:
        data = client.execute(
            f"SELECT max(employer) as val from("
            f"select count(id) as count_vacancies, employer, round(avg(salary_from + salary_to)) as salary from vacancies "
            f"where city='{city_name}'"
            f"group by employer order by salary desc limit 15)"
        )

    return data[0][0]


def popular_city_salary(client): #def popular_city_salary(client, cities):
    """Средняя заработная плата в городах"""
    data = client.execute(
        'select count(city) from ('
        'select count(id) as count_vacancies, city from vacancies '
        'group by city having count_vacancies>=1000 order by count_vacancies desc)')

    return data[0][0]
