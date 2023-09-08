from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

URL_TEMPLATE = "https://www.work.ua/jobs-kyiv/"
FILE_NAME = "../pythonProject2/test.csv"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def parse(url=URL_TEMPLATE):
    data = []
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    soup = bs(r.text, "html.parser")
    div_id = soup.find("div", id=("pjax-job-list"))
    div_cardhover = div_id.find_all("div", class_=("card-hover"))

    for card in div_cardhover:
        vacancies_names = card.find_all("h2")

        for name in vacancies_names:
            vacancy_title = name.a.get_text(strip=True)
            vacancy_url = 'https://www.work.ua' + name.a["href"]

        job_description = card.find_all("p", class_=("text-muted"))
        job_description_text = [desc.get_text(strip=True) for desc in job_description]
        description = [desc.replace("\u2060", "") for desc in job_description_text]

        salary_container = card.find("b", string=re.compile(r'\d+[\s–]+\d+\s*грн'))
        if salary_container:
            salary_text = salary_container.get_text(strip=True)
            salary = ' '.join(salary_text.split())
        else:
            salary = None

        data.append({
            "Назва вакансії": vacancy_title,
            "Посилання": vacancy_url,
            "Короткий опис": description,
            "Зар.плата": salary
        })

    return data

df = pd.DataFrame(data=parse())
df['Короткий опис'] = df['Короткий опис'].apply(lambda x: '\n'.join(x))  # Объединяем описания в одну строку с
# символами перевода строки
df.to_csv(FILE_NAME, index=False)  # Записываем DataFrame в CSV-файл без индексов

