import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    # BeautifulSoup이 지원하는 .get_text()는 해당 soup안에 있는 텍스트를 추출할 수 있다.
    # ()안에 strip = True라고 치면 공백 삭제
    return int(last_page)


def extract_job(html):
    title = html.find("h2", {"class", "mb4"}).find("a")["title"]
    company, location = html.find("h3", {"class", "mb4"}).find_all(
        "span", recursive=False)
    # reculsive = False 를 사용하면  span안에 있는 span은 안가져오게 된다.
    company = company.get_text(strip=True)
    location = location.get_text(strip=True).strip("-").strip("\r").strip("\n")
    job_id = html['data-jobid']
    return {"title": title, "company": company, "location": location, "apply_link": f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class", "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
