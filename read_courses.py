# -*- coding: latin-1 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os,sys,time

print 'Hi there. Plz trust me and enter your Feide credentials.'
time.sleep(0.5)
user_name, user_pw = None, None
while user_name is None or user_pw is None:
    user_name = raw_input('User: ')
    user_pw = raw_input('Password: ')
print 'Assuming your credentials are correct. Firing up chrome...'
time.sleep(0.3)
dir_path = os.getcwd()
driver = webdriver.Chrome(dir_path + '/chromedriver.exe')
ntnu_itslearning_url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=252&AuthState=_9118f881ab74e45cbc23c0cb702b667ae2d11c4019%3Ahttps%3A%2F%2Fidp.feide.no%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Durn%253Amace%253Afeide.no%253Aservices%253Ano.ntnu.ssowrapper%26cookieTime%3D1495838407%26RelayState%3D%252Fsso-wrapper%252Fweb%252Fwrapper%253Ftarget%253Ditslearning'
driver.get(ntnu_itslearning_url)

def find_and_type(id,s,enter=False):
    tmp = driver.find_element_by_id(id)
    tmp.clear()
    tmp.send_keys(s)
    if enter:
        tmp.send_keys(Keys.ENTER)

find_and_type('username',user_name)
find_and_type('password',user_pw,True)

# open the course api directly
courses_url = 'https://ntnu.itslearning.com/Course/AllCourses.aspx'
driver.get(courses_url)
all_courses = Select(driver.find_element_by_tag_name('select'))
# list all courses by the student
all_courses.select_by_value('All')
html = driver.page_source
soup = BeautifulSoup(html,'lxml')
# print soup.findAll('a', href=re.compile('^/main.aspx?CourseID='))
course_list=[]
for link in soup.find_all('a', href=True):
    if 'CourseID' in link['href']:
        course_list.append(link['href'].split('=')[1].encode('utf-8'))
print 'Found',len(course_list),'courses'
print course_list
# access each course through selenium
def check_words(root,wordlist):
    for w in wordlist:
        if w in root:
            return True
    return False
its_base = 'https://ntnu.itslearning.com/'
base_url = its_base + 'main.aspx?CourseID='
for course in course_list:
    driver.get(base_url + course)
    # locate the assignments
    time.sleep(1)
    print 'Exploring new course'
    soup = BeautifulSoup(driver.page_source, 'lxml')
    for link in soup.find_all('a', href=True):
        if 'processfolder' in link['href']:
            # check if this folder has the name 'oving' or 'assignment'
            assignment_name = link.text.lower()
            # print assignment_name
            if check_words(assignment_name,['seminar','øvinger'.decode('utf-8'),'exercise','oppgaver','prosjekt','project']):
                # print 'Entering folder...',assignment_name
                # open folder and check sub-trees
                assignment_link = link['href']
                driver.get(assignment_link)
                print 'Accessing assignment folder',assignment_link
                subsoup = BeautifulSoup(driver.page_source,'lxml')
                for subfile in subsoup.find_all('a', class_='GridTitle'):
                    # print subfile.text
                    driver.get(its_base+subfile['href'])
                    file_soup = BeautifulSoup(driver.page_source, 'lxml')
                    delivered = file_soup.find_all('div', class_='ccl-filelist')
                    # iterate delivered files and find their links
                    for x in delivered:
                        for deliver_link in x.find_all('a',href=True):
                            if 'DownloadRedirect' in deliver_link['href']:
                                # download this file
                                driver.get(deliver_link['href'])
                                print 'Downloading file'

    time.sleep(1)
