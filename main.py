import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd

url = 'https://id.indeed.com/jobs?'
params = {
    'q': 'python developer',
    'l': 'Jakarta'
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36'
}
res = requests.get(url, params=params, headers=headers)
indeeds = None


def get_total_pages():
    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+') as outfile:
        outfile.write(res.text)
        outfile.close()

    total_pages = []
    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('ul', 'pagination-list')
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)

    total_pages = int(max(total_pages))
    return total_pages


def get_all_items():
    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.find_all('div', 'job_seen_beacon')

    jobs = []
    for item in contents:
        title = item.find('h2', 'jobTitle').text
        company = item.find('span', 'companyName').text
        location = item.find('div', 'companyLocation').text

        try:
            salary = item.find('div', 'salary-snippet').text
            link = 'https://id.indeed.com' + item.find('a')['href']
        except:
            salary = 'Salary not defined'
            link = 'Link not available'

        data = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'link': link
        }
        jobs.append(data)

    try:
        os.mkdir('json')
    except FileExistsError:
        pass

    with open('json/jobs.json', 'w+') as jsondata:
        json.dump(jobs, jsondata)

    print('json created')

    df = pd.DataFrame(jobs)
    df.to_csv('indeed_data.csv', index=False)
    df.to_excel('indeed_data.xlsx', index=False)

    print('csv and excel created')


if __name__ == '__main__':
    get_all_items()
    # get_total_pages()
