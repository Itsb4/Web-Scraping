import openpyxl
import requests
from bs4 import BeautifulSoup

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Indeed Jobs Details'
sheet.append(['Title', 'Company', 'Salary', 'Summary'])

try:
    def extract(page):
        source = requests.get(
            'https://in.indeed.com/jobs?q=web+developer&l=Pune%2C+Maharashtra&start={page}')
        source.raise_for_status()

        soup = BeautifulSoup(source.content, 'html.parser')
        return soup

except Exception as e:
    print(e)


def transform(soup):
    divs = soup.find_all('div', class_='job_seen_beacon')
    for item in divs:
        title = item.find('h2', class_='jobTitle').text.strip()
        company = item.find('span', class_='companyName').text.strip()
        try:
            salary = item.find('div', class_='attribute_snippet').text.strip()
        except:
            salary = 'Not Mentioned'
        summary = item.find(
            'tr', class_='underShelfFooter').text.strip().replace('\n', ' ')
        sheet.append([title, company, salary, summary])
    return


joblist = []
for i in range(0, 40, 10):
    print(f'Getting Page, {i}')
    c = extract(0)
    transform(c)

excel.save('Indeed Jobs List1.xlsx')
