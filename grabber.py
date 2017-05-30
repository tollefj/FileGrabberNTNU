# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os,sys,time,platform
import codecs
import warnings  # supressing warnings from BeautifulSoup
import shutil
warnings.filterwarnings("ignore")

def main():
    chrome_driver = os.path.join('/driver','chromedriver')
    print chrome_driver
    _os = platform.system()
    if _os.lower() == 'windows':
        chrome_driver = os.path.join('driver','chromedriver.exe')
    elif _os.lower() == 'linux':
        chrome_driver = os.path.join('driver','chromedriverLinux')
    print _os+' detected. Chromedriver path: '+chrome_driver+'\n'
    print 'Enter your Feide credentials.'
    time.sleep(0.5)
    user_name, user_pw = "tollefej", "Tollef1337"

    print 'Assuming your credentials are correct. Firing up chrome...'
    print '(All your files will be stored in your default download folder)'
    time.sleep(0.3)
    dir_path = os.getcwd()
    #driver = webdriver.Chrome(dir_path + chrome_driver)
    print 'Setting options'
    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "prefs",{
            "download.default_directory": r"/Users/tollef/Desktop/Test_Downloads",
            "download.prompt_for_download":False,
            "download.diractory_upgrade":True,
            "safebrowsing.enabled":True
        }
    )
    driver = webdriver.Chrome(chrome_options = options,executable_path = dir_path + chrome_driver)

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
    courses_url = 'https://ntnu.itslearning.com/Course/AllCourses.aspx'
    driver.get(courses_url)
    all_courses = Select(driver.find_element_by_tag_name('select'))
    # list all courses
    all_courses.select_by_value('All')  # All, Active, Archived
    soup = BeautifulSoup(driver.page_source)
    course_list=[]

    def enc(txt):
        # encode a text to utf-8
        return unicode(txt).encode('latin-1')

    for link in soup.find_all('a', href=True):
        if 'CourseID' in link['href']:
            _course_id = enc(link['href'].split('=')[1])
            _course_name = enc(link.text)
            course_list.append(_course_id)


    # access each course through selenium
    dir_path="/Users/tollef/Desktop/Test_Downloads"
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

        files_were_added = False
        time.sleep(1)
        print 'Exploring new course'
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for link in soup.find_all('a', href=True):
            if 'processfolder' in link['href']:
                # check if this folder has the name 'oving' or 'assignment'
                assignment_name = link.text.lower()
                if check_words(assignment_name,['seminar','vinger','exercise','oppgaver','prosjekt','project']):
                    # open folder and check sub-trees
                    assignment_link = link['href']
                    driver.get(assignment_link)
                    print 'Accessing assignment folder',assignment_link
                    subsoup = BeautifulSoup(driver.page_source,'html.parser')
                    for subfile in subsoup.find_all('a', class_='GridTitle'):
                        driver.get(its_base+subfile['href'])
                        file_soup = BeautifulSoup(driver.page_source, 'html.parser')
                        delivered = file_soup.find_all('div', class_='ccl-filelist')
                        # iterate delivered files and find their links
                        for x in delivered:
                            for deliver_link in x.find_all('a',href=True):
                                if 'DownloadRedirect' in deliver_link['href']:
                                    # download the file
                                    driver.get(deliver_link['href'])
                                    print 'Downloading file'
                                    files_were_added = True
        working_dir = os.path.join(dir_path,course)
        if files_were_added:
            os.makedirs(working_dir)
        # move all the files outside of the folder into working_dir
        for filename in os.listdir(dir_path):
            curfile=os.path.join(dir_path,filename)
            if os.path.isfile(curfile):
                print 'moving file!!! >',filename
                shutil.move(curfile, working_dir)

            else:
                continue

        time.sleep(1)
main()
