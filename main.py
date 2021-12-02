import requests
from bs4 import BeautifulSoup
import os

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

    for item in contents:
        title = item.find('h2', 'jobTitle').text
        location = item.find('div', 'companyLocation').text
        print(title)
        print(location)


if __name__ == '__main__':
    get_all_items()
