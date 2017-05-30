from Tkinter import *
from ttk import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os,sys,time,platform
import codecs
import warnings  # supressing warnings from BeautifulSoup
warnings.filterwarnings("ignore")

class MainWindow(Tk):
    def __init__(self):
        self.main = Tk()
        self.main.title("Filegrabber NTNU")
        self.frame = Frame(self.main, padding=(5,3,5,12))
        self.frame.grid(column=0,row=0,sticky=(N,S,E,W))

        self.user = None
        self.pw = None
        self.confirm = None
        self.register_user = None
        self.register_pw = None
        self.ignored_courses = []
        self.listbox = None

        self.btn_a = None
        self.btn_l = None
        self.btn_load = None
        # for c in range(4):
        #     self.main.grid_columnconfigure(c,weight=1)
        #     self.main.grid_rowconfigure(c,weight=1)

        self.download_lectures = BooleanVar()
        self.download_assignments = BooleanVar()
        self.download_lectures.set(1)

        # main program variables
        self.start = None # the button to start the program
        self.chrome_driver = os.path.join('/driver','chromedriver')
        self.logged_in = False
        self.dir_path = os.getcwd()
        self.ntnu_itslearning_url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=252&AuthState=_9118f881ab74e45cbc23c0cb702b667ae2d11c4019%3Ahttps%3A%2F%2Fidp.feide.no%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Durn%253Amace%253Afeide.no%253Aservices%253Ano.ntnu.ssowrapper%26cookieTime%3D1495838407%26RelayState%3D%252Fsso-wrapper%252Fweb%252Fwrapper%253Ftarget%253Ditslearning'
        self.courses_url = 'https://ntnu.itslearning.com/Course/AllCourses.aspx'

        self.accept_input()
        self.init_ui()
        self.wait_for_confirm()

    def run(self):
        print '>>>Main program running!'

        # access each course through selenium
        def check_words(root,wordlist):
            for w in wordlist:
                if w in root:
                    return True
            return False
        its_base = 'https://ntnu.itslearning.com/'
        base_url = its_base + 'main.aspx?CourseID='
        for course in course_list:
            self.driver.get(base_url + course)
            # locate the assignments
            time.sleep(1)
            print 'Exploring new course'
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for link in soup.find_all('a', href=True):
                if 'processfolder' in link['href']:
                    # check if this folder has the name 'oving' or 'assignment'
                    assignment_name = link.text.lower()
                    if check_words(assignment_name,['seminar','vinger','exercise','oppgaver','prosjekt','project']):
                        # open folder and check sub-trees
                        assignment_link = link['href']
                        self.driver.get(assignment_link)
                        print 'Accessing assignment folder',assignment_link
                        subsoup = BeautifulSoup(self.driver.page_source,'html.parser')
                        for subfile in subsoup.find_all('a', class_='GridTitle'):
                            self.driver.get(its_base+subfile['href'])
                            file_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                            delivered = file_soup.find_all('div', class_='ccl-filelist')
                            # iterate delivered files and find their links
                            for x in delivered:
                                for deliver_link in x.find_all('a',href=True):
                                    if 'DownloadRedirect' in deliver_link['href']:
                                        # download the file
                                        self.driver.get(deliver_link['href'])
                                        print 'Downloading file'

            time.sleep(1)

    def fetch_courses(self):
        print self.chrome_driver
        _os = platform.system()
        if _os.lower() == 'windows':
            self.chrome_driver = os.path.join('driver','chromedriver.exe')
        elif _os.lower() == 'linux':
            self.chrome_driver = os.path.join('driver','chromedriverLinux')
        print _os+' detected. Chromedriver path: '+self.chrome_driver+'\n'
        print 'Assuming your credentials are correct. Firing up chrome...'
        print '(All your files will be stored in your default download folder)'
        self.driver = webdriver.Chrome(self.dir_path + self.chrome_driver)
        self.driver.get(self.ntnu_itslearning_url)

        def find_and_type(id,s,enter=False):
            tmp = self.driver.find_element_by_id(id)
            tmp.clear()
            tmp.send_keys(s)
            if enter:
                tmp.send_keys(Keys.ENTER)

        print 'typing in',self.register_user,'and',self.register_pw
        find_and_type('username',self.register_user)
        find_and_type('password',self.register_pw,True)

        self.driver.get(self.courses_url)
        all_courses = Select(self.driver.find_element_by_tag_name('select'))
        # list all courses
        all_courses.select_by_value('All')  # All, Active, Archived
        soup = BeautifulSoup(self.driver.page_source)
        # course_list=[]
        courses = dict()
        ignored_courses = [] # save ignored courses for conditional checks

        def enc(txt):
            # encode a text to utf-8
            return unicode(txt).encode('latin-1')

        for link in soup.find_all('a', href=True):
            if 'CourseID' in link['href']:
                _course_id = enc(link['href'].split('=')[1])
                _course_name = enc(link.text)
                courses[_course_id] = _course_name

        for c in courses.values():
            #print c.decode('iso-8859-1')
            print c.decode('latin-1')
            self.listbox.insert(END,c.decode('latin-1'))

        self.btn_load.config(state='disabled')
        self.btn_a.config(state='enabled')
        self.btn_l.config(state='enabled')
        self.start.config(state='enabled')


    def populate_courses(self,courses):
        for c in courses:
            self.listbox.insert(c)

    def ignored_subjects(self):
        ignored = list()
        selected = self.listbox.curselection()
        for s in selected:
            ignored.append(self.listbox.get(s))
        print 'ignored following courses...'
        for i in ignored:
            print i


    def clicked_assignments(self):
        print self.download_assignments.get()
        print self.download_lectures.get()
    def clicked_lecturenotes(self):
        print self.download_assignments.get()
        print self.download_lectures.get()
    def accept_input(self):
        f = self.frame
        self.user = Entry(f,text='',width=20)
        self.pw = Entry(f,text='',show='*',width=20)
        self.confirm = Button(f,text='Confirm login information',command=self.get_data)
        #self.lecture_notes = Checkbutton(f,text='Lecture notes',variable=BooleanVar(),command=self.clicked_lecturenotes)

    def init_ui(self):
        Label(self.frame,text="User",width=20).grid(row=0,column=1)
        Label(self.frame,text="Password",width=20).grid(row=1,column=1)
        self.user.grid(row=0,column=2)
        self.pw.grid(row=1,column=2,pady=10)
        self.confirm.grid(row=2,column=1,columnspan=4)

    def wait_for_confirm(self):
        self.main.mainloop()

    def get_data(self):
        self.register_user = self.user.get()
        self.register_pw = self.pw.get()
        if self.register_user=="" or self.register_pw=="":
            # Try again alert
            print 'Invalid login information'
            return
        Label(self.frame,text="Select to IGNORE courses").grid(row=3,column=1,sticky=W,pady=(20,5))

        scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        scrollbar.grid(row=4,column=1,sticky=N)
        self.listbox = Listbox(self.frame,selectmode=MULTIPLE,width=20,height=20,yscrollcommand=scrollbar.set)
        self.listbox.grid(row=4,column=1,columnspan=2,rowspan=20,sticky=W)


        self.btn_load = Button(self.frame,text='Load courses', command=self.fetch_courses).grid(row=4,column=2)

        self.btn_a = Checkbutton(self.frame,text='Assignments',command=self.clicked_assignments,variable=self.download_assignments,onvalue=1,offvalue=0)
        self.btn_a.grid(row=5,column=2)
        self.btn_a.config(state='disabled')

        self.btn_l = Checkbutton(self.frame,text='Lecture notes',command=self.clicked_lecturenotes,variable=self.download_lectures,onvalue=1,offvalue=0)
        self.btn_l.grid(row=6,column=2)
        self.btn_l.config(state='disabled')

        self.start = Button(self.frame,text='Download',command=self.run)
        self.start.grid(row=8,column=2)
        self.start.config(state='disabled')

        self.user.config(state='disabled')
        self.pw.config(state='disabled')
        self.confirm.config(state='disabled',text='Logged in')
        print 'Pressed login'
        self.logged_in = True

MW = MainWindow()
