"""This script scraps data from LinkedIn and returns the list"""
import math
import requests
from bs4 import BeautifulSoup


def scrapper(target_url, target_job_url):
    """"""
    l, k = [], []
    o = {}
    for i in range(0,math.ceil(30/25)):

        res = requests.get(target_url.format(i))
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")

        for x, ele in enumerate(alljobs_on_this_page):
            jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            l.append(jobid)

    

    for j, ele in enumerate(l):

        resp = requests.get(target_job_url.format(l[j]))
        soup=BeautifulSoup(resp.text,'html.parser')

        o["job_id"] = l[j]

        try:
            o["company_name"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except AttributeError:
            o["company_name"]=None

        try:
            o["job_title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except AttributeError:
            o["job_title"]=None

        try:
            o["seniority_level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
        except AttributeError:
            o["seniority_level"]=None

        try:
            o["job_location"] = soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
        except AttributeError:
            o["job_location"]=None

        # o["job_desc"] = soup.find("div",{"class":"show-more-less-html__markup show-more-less-html__markup--clamp-after-5"}).text
        o["posted_time"] = soup.find("span",{"class":"posted-time-ago__text topcard__flavor--metadata"})
        k.append(o)
        o={}

    return k
