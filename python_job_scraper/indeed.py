import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?as_and=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')

    pages = []

    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find("h2", {"class", "title"}).find("a")["title"]
    # 이런식으로 []을 쓰면 해당 a 안에 있는 attribute인 title을 가져올수 있다.
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company.find("a").string)
    else:
        company = str(company.string)
    company = company.strip()
    # str.strip()을 사용하면 해당 str양옆에 있는 공백을 없앨 수 있다.
    # str.strip("f") 이렇게 사용하면 str안에 있는 f를 전부 제거해준다.
    location = html.find("div", {"class", "recJobLoc"})["data-rc-loc"]
    job_id = html.find("h2", {"class": "title"}).find("a")["href"]
    return{'title': title, 'company': company, 'location': location, 'link': f"https://kr.indeed.com{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
