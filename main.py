import requests
import json
from bs4 import BeautifulSoup
import os
import pandas as pd

url = 'https://id.indeed.com/jobs?'
# params = {
#     'q': 'Python Development',
#     'l': 'Jakarta'
# }
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/96.0.4664.45 Safari/537.36'
# }
# res = requests.get(url, params=params, headers=headers)
indeeds = None


def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36'
    }

    res = requests.get(url, params=params, headers=headers)

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


def get_all_items(query, location, start, page):
    params = {
        'q': query,
        'l': location,
        'start': start
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36'
    }

    res = requests.get(url, params=params, headers=headers)

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

    with open(f'json/{query}_in_{location}_page_{page}.json', 'w+') as jsondata:
        json.dump(jobs, jsondata)

    print('json created')
    return jobs


def create_document(dataFrame, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass


    df = pd.DataFrame(dataFrame)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_result/{filename}.xlsx', index=False)

    print(f'File {filename}.csv and {filename}.xlsx successfully created')


def run():
    query = input('Enter your keyword/job title: ')
    location = input('Enter your location: ')

    total = get_total_pages(query, location)
    counter = 0
    final_result = []
    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    try:
        os.mkdir('reports')
    except FileExistsError:
        pass

    with open(f'reports/{query}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)

    print('Data Json Created')

    create_document(final_result, query)

if __name__ == '__main__':
    run()
