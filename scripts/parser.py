import json
import zipfile
from pathlib import Path

downloads_path = str(Path.home() / "Downloads")

vacancy = None
data = None

with zipfile.ZipFile(downloads_path + "/40M_41M_full.zip", "r") as z:
    for filename in z.namelist():
        print(filename)
        with z.open(filename) as f:
            data = f.read()
            vacancy = json.loads(data)
            vacancies = []

            for i in range(0, len(vacancy)):
                if 'name' in vacancy[i] and vacancy[i]['salary'] is not None:
                    vacancies_tmp = {
                        'name': vacancy[i]['name'],
                        'salary_from': vacancy[i]['salary']['from'],
                        'salary_to': vacancy[i]['salary']['to'],
                        'salary_gross': vacancy[i]['salary']['gross'],
                        'currency': vacancy[i]['salary']['currency'],
                        'experience': vacancy[i]['experience']['name'],
                        'schedule': vacancy[i]['schedule']['name'],
                        'employment': vacancy[i]['employment']['name'],
                        'key_skills': vacancy[i]['key_skills'],
                        'employer': vacancy[i]['employer']['name'],
                        'city': vacancy[i]['area']['name'],
                        'area_url': vacancy[i]['area']['url'],
                        'area_id': vacancy[i]['area']['id'],
                        'area_name': vacancy[i]['area']['name'],
                        'created_at': vacancy[i]['created_at']
                    }
                    vacancies.append(vacancies_tmp)
                    print(vacancies_tmp)

            with open(f'vacancies_1/new{filename[filename.find("/") + 1:]}', 'w') as outfile:
                json.dump(vacancies, outfile)
