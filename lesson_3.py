from pymongo import MongoClient
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json

client = MongoClient('localhost', 27017)
db = client['hhru']
vac = db.vac


def vacance_info(vacances):
    vacance_data = {}
    vacance_name = vacances.find('a', {"class": "bloko-link"}).getText()
    vacance_link = vacances.find('a', {"class": "bloko-link"}).get('href')
    vacance_data["name"] = vacance_name
    vacance_data["link"] = vacance_link
    vacance_data["source"] = start_url
    try:
        salary = vacances.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"}).getText()
        salary = salary.replace('\u202f', '').split()
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[1])

            salary_currency = salary[2]

        vacance_data['min_salary'] = salary_min
        vacance_data['max_salary'] = salary_max
        vacance_data['currency'] = salary_currency

    except Exception as e:
        vacance_data['Salary'] = None
    return vacance_data


def _more_than_max(min_salary):
    return list(vac.find({'$or': ({'min_salary': {'$gt': min_salary}},
                                  {'max_salary': {'$gt': min_salary}})}
                         )
                )


if __name__ == "__main__":
    user_find = input('Введите название вакансии: ')
    user_page = int(input('Введите номер страницы: '))

    start_url = 'https://hh.ru'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36 '
    }

    params = {
        "area": "1",
        "fromSearchLine": "true",
        "st": "searchVacancy",
        "text": user_find,
        "from": "suggest_post",
        "page": user_page,
    }
    response = requests.get(start_url + '/search/vacancy/', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    next_page = soup.find('a', {'data-qa': 'pager-next'})

    vacance = []
    vacance_list = soup.find_all('div', {'class': 'vacancy-serp-item'})

    while next_page:
        page_url = next_page.get('href')
        new_url = f'{start_url}{page_url}'
        response = requests.get(new_url, headers=headers)
        soup = bs(response.text, 'html.parser')

        next_page = soup.find('a', {'data-qa': 'pager-next'})
        vacance_list = soup.find_all('div', {'class': 'vacancy-serp-item'})

        for vacances in vacance_list:
            vacance.append(vacance_info(vacances))

    # with open("job_hh.json", 'w', encoding="utf-8") as file:
    #     json.dump(vacance, file, indent=2, ensure_ascii=False)

    if vac.count_documents({}) == 0:
        vac.insert_many(vacance)
    else:
        for vacances in vacance:
            if bool(vac.find_one({'link': vacances['link']})):
                vac.update_one({'link': vacances['link']}, {'$set': vacances}, upsert=True)

pprint(_more_than_max(100000))