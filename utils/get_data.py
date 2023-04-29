"""This script scraps data from LinkedIn and returns the list"""
import math
import requests
from bs4 import BeautifulSoup
from utils.techfinder import TechFinder

JD_PER_PAGE = 25
ITERATION_OVER_PAGES = 30

def scrapper(target_url: str, target_job_url: str) -> list:
    """Scraps the data from LinkedIn API
    Inputs: URLs for jobs and jobs' contents
    Returns: list of jobs and their metadata
    """
    job_ids, ultimate_result = [], []
    result_dict = {}
    for i in range(0,math.ceil(ITERATION_OVER_PAGES/JD_PER_PAGE)):

        res = requests.get(target_url.format(i), timeout=10)
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")

        for x, ele in enumerate(alljobs_on_this_page):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).\
                get('data-entity-urn').split(":")[3]
            job_ids.append(jobid)

    for j, ele in enumerate(job_ids):

        resp = requests.get(target_job_url.format(job_ids[j]), timeout=10)
        soup=BeautifulSoup(resp.text,'html.parser')

        result_dict["job_id"] = job_ids[j]

        try:
            result_dict["company_name"]=soup.find("div",{"class":"top-card-layout__card"}).\
                find("a").find("img").get('alt')
        except AttributeError:
            result_dict["company_name"]=None

        try:
            result_dict["job_title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).\
                find("a").text.strip()
        except AttributeError:
            result_dict["job_title"]=None

        try:
            result_dict["seniority_level"]=soup.\
                find("ul",{"class":"description__job-criteria-list"}).\
                find("li").text.replace("Seniority level","").strip()
        except AttributeError:
            result_dict["seniority_level"]=None

        try:
            result_dict["job_location"] = soup.\
                find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).\
                text.strip()
        except AttributeError:
            result_dict["job_location"]=None

        try:
            result_dict["posted_time"] = \
            soup.find("span",{"class":"posted-time-ago__text topcard__flavor--metadata"}).\
                get_text(strip=True)
        except AttributeError:
            result_dict["posted_time"]=None

        try:
            job_desc = soup.find("div",
            {"class":"show-more-less-html__markup show-more-less-html__markup--clamp-after-5"}).\
                get_text(strip=True)
            result_dict["job_description"] = job_desc
        except AttributeError:
            continue

        if job_desc:
            finder = TechFinder()
            detected_techs = finder.tech_stack_finder(job_desc)
            result_dict["tech_stack"] = ",".join(detected_techs)

        ultimate_result.append(result_dict)
        result_dict={}

    return ultimate_result
