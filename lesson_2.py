import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import json


def Vacance_info(vacances):
    vacance_data = {}
    vacance_name = vacances.find('a', {"class": "bloko-link"}).getText()
    vacance_link = vacances.find('a', {"class": "bloko-link"}).get('href')
    vacance_data["Название вакансии"] = vacance_name
    vacance_data["Ссылка на вакансию"] = vacance_link
    vacance_data["Источник"] = start_url
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

        vacance_data['Мин зарплата'] = salary_min
        vacance_data['Макс зарплата'] = salary_max
        vacance_data['Валюта'] = salary_currency

    except Exception as e:
        vacance_data['Зарплата'] = None
    return vacance_data


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
            vacance.append(Vacance_info(vacances))

    with open("job_hh.json", 'w', encoding="utf-8") as file:
        json.dump(vacance, file, indent=2, ensure_ascii=False)


