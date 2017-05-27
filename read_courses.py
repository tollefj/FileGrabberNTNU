from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import requests
import time
print 'Hi there. Plz trust me and enter your Feide credentials.'
time.sleep(1)
# user_name, user_pw = "tollefej","Tollef1337"
user_name, user_pw = None, None
while user_name is None or user_pw is None:
    user_name = raw_input('User: ')
    user_pw = raw_input('Password: ')
print 'Assuming your credentials are correct, here we go.'
time.sleep(0.3)
dir_path = os.getcwd()
driver = webdriver.Chrome(dir_path + '/chromedriver')
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



# outx = open('source.html','w')
# print driver.page_source
# for i in driver.page_source:
#     outx.write(i.encode('utf-8'))
# outx.close()


# html = driver.page_source
# soup = BeautifulSoup(html,"html.parser")
# for tag in soup.find_all('iconcolumn'):
#     print tag.text
