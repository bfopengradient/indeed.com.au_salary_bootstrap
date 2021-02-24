 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait 
import pandas as pd
import numpy as np





salaries = []
title = []
location = []
company_name = []
scraped_descriptions = []

#replace url for data analyst if needed.  "https://au.indeed.com/jobs?q=data+analyst&l=Australia"
 
main_url="https://au.indeed.com/jobs?q=data+scientist"
start_from = '&start='
driver = webdriver.Chrome(executable_path="./chromedriver") 

 

for page in range(1, 10):
    
    page = (page - 1) * 10
        
    if page == 0:
                
        url=main_url
        
        driver.get(url)
        
            
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        #Full_job_description using selenium         
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobsearch-SerpJobCard")))
 
        jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
    
        for job in jobs:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jobsearch-SerpJobCard")))
            try:  # click on the job card and add its description to descriptions list
                job.click()
                wait.until(EC.presence_of_element_located((By.ID, "vjs-content")))
                scraped_descriptions.append(driver.find_element_by_id('vjs-content').text)
            except ElementClickInterceptedException:
              # if ElementClickInterceptedException, scroll away and try again
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                job.click()
                scraped_descriptions.append(driver.find_element_by_id("vjs-content").text)                                       
            
            

        #Job title
        jobs_a = soup.find_all(name='a', attrs={'data-tn-element': "jobTitle"})
        for job in jobs_a:
            job_attrs = job.attrs
            title.append(job_attrs["title"])

        #Salaries
        jobs_divs = soup.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
        for div in jobs_divs:
            salary_span = div.find('span', attrs={'class': 'salaryText'})
            if salary_span:
                salaries.append(salary_span.string.strip())
            else:
                salaries.append('Not shown') 


        #Locations
        loc_div = soup.find_all('div', attrs={'class': "recJobLoc"}) 
        for loc in loc_div:
            loc_attrs = loc.attrs
            location.append(loc_attrs["data-rc-loc"])

        #Company_names
        company_span = soup.find_all('span', attrs={'class': "company"})
        for span in company_span:
            company_name.append(span.text.strip())


        
    if page >0: 
        
        url_1 = "%s%s%d" % (main_url,start_from, page) 
        
        driver.get(url_1)
                 
        soup_1 =  BeautifulSoup(driver.page_source, "lxml")
        
        #Full_job_description         
        wait = WebDriverWait(driver, 1)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobsearch-SerpJobCard"))) 
        jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
        for job in jobs:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jobsearch-SerpJobCard")))
            try:  # click on the job card and add its description to descriptions list
                job.click()
                wait.until(EC.presence_of_element_located((By.ID, "vjs-content")))
                scraped_descriptions.append(driver.find_element_by_id('vjs-content').text)
            except ElementClickInterceptedException:
              # if ElementClickInterceptedException, scroll away and try again
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                job.click()
                scraped_descriptions.append(driver.find_element_by_id("vjs-content").text)
                
        
        #Job title
        jobs_a = soup_1.find_all(name='a', attrs={'data-tn-element': "jobTitle"})
        for job in jobs_a:
            job_attrs = job.attrs
            title.append(job_attrs["title"])

        #Salaries
        jobs_divs = soup_1.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
        for div in jobs_divs:
            salary_span = div.find('span', attrs={'class': 'salaryText'})
            if salary_span:
                salaries.append(salary_span.string.strip())
            else:
                salaries.append('Not shown') 

        #Location
        loc_div = soup_1.find_all('div', attrs={'class': "recJobLoc"}) 
        for loc in loc_div:
            loc_attrs = loc.attrs
            location.append(loc_attrs["data-rc-loc"])

        #Company_names
        company_span = soup_1.find_all('span', attrs={'class': "company"})
        for span in company_span:
            company_name.append(span.text.strip())


             
driver.close()


indeed_dict={'title': title,
             'company': company_name,
             'salary': salaries,
             'location': location,
             'job_desc': scraped_descriptions          
            }

 #data science dataframe

indeed_d= pd.DataFrame(indeed_dict)