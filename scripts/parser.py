"""
Выборка вакансий
"""
import json
import zipfile
from pathlib import Path

DOWNLOADS_PATH = str(Path.home() / "Downloads")

VACANCY = None
DATA = None

with zipfile.ZipFile(DOWNLOADS_PATH + "/archive-2020-12-15_15-26-42.zip", "r") as z:
    for filename in z.namelist():
        print(filename)
        with z.open(filename) as f:
            DATA = f.read()
            VACANCY = json.loads(DATA)
            vacancies = []

            for i in enumerate(VACANCY): #for i in range(0, len(VACANCY)):
                if 'name' in VACANCY[i] and VACANCY[i]['salary'] is not None:
                    vacancies_tmp = {
                        'id': VACANCY[i]['id'],
                        'name': VACANCY[i]['name'],
                        'salary_from': VACANCY[i]['salary']['from'],
                        'salary_to': VACANCY[i]['salary']['to'],
                        'salary_gross': VACANCY[i]['salary']['gross'],
                        'currency': VACANCY[i]['salary']['currency'],
                        'experience': VACANCY[i]['experience']['name'],
                        'schedule': VACANCY[i]['schedule']['name'],
                        'employment': VACANCY[i]['employment']['name'],
                        'key_skills': VACANCY[i]['key_skills'],
                        'employer': VACANCY[i]['employer']['name'],
                        'city': VACANCY[i]['area']['name'],
                        'area_url': VACANCY[i]['area']['url'],
                        'area_id': VACANCY[i]['area']['id'],
                        'area_name': VACANCY[i]['area']['name'],
                        'created_at': VACANCY[i]['created_at']
                    }
                    vacancies.append(vacancies_tmp)
                    print(vacancies_tmp)

            with open(f'/home/rfnz/Projects/hh-analyzer/vacan_3/new{filename[filename.find("/") + 1:]}', 'w') as outfile:
                json.dump(vacancies, outfile)
