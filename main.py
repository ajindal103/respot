import csv
import string
import json
import random
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from tkinter import filedialog
from pyresparser import ResumeParser
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from flask import Flask, redirect, render_template, session, request
from selenium.common.exceptions import NoSuchElementException
from recommendSkills import *

app = Flask(__name__)
res = ''.join(random.choices(string.ascii_lowercase +
              string.digits + string.punctuation, k=26))
app.secret_key = res


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload')
def upload():
    resumeU = filedialog.askopenfilename(title="Select Resume")
    if resumeU == '':
        return redirect('/')
    session["resumeU"] = resumeU
    return redirect('/')


@app.route('/analyse')
def analyse():
    resumeA = session.get("resumeU", None)
    if resumeA == None:
        return redirect('/')

    headerList = ['jobTitle', 'jobLocation', 'jobLink']
    with open("jobs_desc.csv", 'w') as f:
        dw = csv.DictWriter(f, delimiter=',', fieldnames=headerList)
        dw.writeheader()

    data = ResumeParser(resumeA).get_extracted_data()

    recommended_skills = recommendSkills(data)
    
    i = 0
    random.shuffle(data['skills'])
    for skill in data['skills']:
        if (i > 4):
            break
        jobFetcher(skill, 5)
        i = i+1

    total_experience = data['total_experience']
    if total_experience > 3:
        exp = 'You are an experienced candidate!'
    elif total_experience < 1:
        exp = 'You are a beginner!'
    else:
        exp = 'You are at intermediate level!'

    with open('jobs_desc.csv', 'r', encoding="utf8") as f:
        jobs = [dict(item) for item in csv.DictReader(f)]
    return render_template('jobs.html', data=jobs, resumeData=data, exp=exp, recommended_skills = recommended_skills)


@app.route('/skillsInput', methods=['POST'])
def skills_input():
    skills = request.form['skills']
    if skills == '':
        return redirect('/')
    headerList = ['jobTitle', 'jobLocation', 'jobLink']
    with open("jobs_desc.csv", 'w') as f:
        dw = csv.DictWriter(f, delimiter=',', fieldnames=headerList)
        dw.writeheader()
    jobFetcher(skills, 15)
    with open('jobs_desc.csv', 'r', encoding="utf8") as f:
        jobs = [dict(item) for item in csv.DictReader(f)]
    return render_template('skillJobs.html', data=jobs)


def openbrowser(driver, key):
    driver.wait = WebDriverWait(driver, 5)
    driver.maximize_window()
    keys = key.split()
    txt1 = ''
    txt2 = ''
    for k in keys:
        txt1 += (k+'%2520')
        txt2 += (k+'-')
    driver.get("https://www.glassdoor.co.in/Job/{}jobs-SRCH_KO0,{}.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={}&typedLocation=&context=Jobs&dropdown=0".format(
        txt2, len(txt2)-1, txt1[:-5]))
    return driver


def geturl(driver, count, key):
    url = []
    soup1 = BeautifulSoup(driver.page_source, "lxml")
    main = soup1.find_all("li", {"class": "react-job-listing"})
    num = 1
    for m in main:
        if (num > count):
            break
        num = num+1
        try:
            jli = 'https://www.glassdoor.co.in{}'.format(m.find('a')['href'])
            jt = m.find('div', class_="job-title")
            if jt is None:
                jt = key + ' Engineer/Developer/Manager'
            else:
                jt = jt.text
            jl = m.find('div', class_="location")
            if jl is None:
                jl = m.find(
                    'span', class_="css-3g3psg pr-xxsm css-iii9i8 e1rrn5ka0").text
            else:
                jl = jl.text
            i = dict(jobTitle=jt, jobLocation=jl, jobLink=jli)
            url.append(i)
        except NoSuchElementException:
            pass
    return url


def jobFetcher(skill, count):
    ser = Service(r"C:\chromedriver.exe")
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(service=ser)
    x = openbrowser(driver, key=skill)
    with open('skills_job.json', 'w') as f:
        json.dump(geturl(x, count, key=skill), f, indent=4)
        driver.quit()
    with open('skills_job.json', 'r') as f:
        jobs = json.load(f)
    data = {}
    i = 1
    jd_df = pd.DataFrame()
    for j in tqdm(jobs):
        data[i] = j
        i += 1
    jd_df = pd.DataFrame(data)
    jd = jd_df.transpose()
    jd.to_csv('jobs_desc.csv', mode='a', index=False, header=False)


if __name__ == "__main__":
    app.run(debug=True)
