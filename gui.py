# -*- coding: utf-8 -*-
from Tkinter import *
from ttk import *
import tkFileDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import os,sys,time,platform,shutil
import codecs
from slugify import slugify
import warnings  # supressing warnings from BeautifulSoup
warnings.filterwarnings("ignore")

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.main = self
        self.main.title("Filegrabber NTNU")
        self.frame = Frame(self.main, padding=(5,3,5,12))
        self.frame.grid(column=0,row=0,sticky=(N,S,E,W))

        self.user_label = None
        self.pw_label = None
        self.user = None
        self.pw = None
        self.confirm = None
        self.register_user = None
        self.register_pw = None
        self.user_data = [self.user_label,self.user,self.pw_label,self.pw]
        self.listbox = None
        self.course_label = None

        self.btn_a = None
        self.btn_l = None
        self.btn_load = None
        # for c in range(4):
        #     self.main.grid_columnconfigure(c,weight=1)
        #     self.main.grid_rowconfigure(c,weight=1)

        self.download_lectures = BooleanVar()
        self.download_assignments = BooleanVar()
        self.download_assignments.set(1)

        # main program variables
        self.start = None # the button to start the program
        self.chrome_driver = os.path.join('/driver','chromedriver')
        self.logged_in = False
        self.dir_path = os.getcwd() # used to obtain the chromedriver
        self.ntnu_itslearning_url = 'https://idp.feide.no/simplesaml/module.php/feide/login.php?asLen=252&AuthState=_9118f881ab74e45cbc23c0cb702b667ae2d11c4019%3Ahttps%3A%2F%2Fidp.feide.no%2Fsimplesaml%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Durn%253Amace%253Afeide.no%253Aservices%253Ano.ntnu.ssowrapper%26cookieTime%3D1495838407%26RelayState%3D%252Fsso-wrapper%252Fweb%252Fwrapper%253Ftarget%253Ditslearning'
        self.courses_url = 'https://ntnu.itslearning.com/Course/AllCourses.aspx'
        self.its_base = 'https://ntnu.itslearning.com/'
        self.courses = dict()
        self.ignored_courses = [] # save ignored self.courses for conditional checks
        self.download_path = None

        #self.run_tests()

        self.accept_input()
        self.init_ui()
        self.wait_for_confirm()

    def new_soup(self,url):
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source)

    def enc(self,txt):
        # encode a text to utf-8
        #return unicode(txt).encode('latin-1')
        return slugify(unicode(txt))

    def run_tests(self):
        x = 'øvingsopplegg før 2017'
        print self.enc(x)

    def run(self):
        # get the keywords for lectures or assignments
        assignment_words = []
        if self.download_assignments.get():
            assignment_words.extend(['seminar','vinger','exercise','oppgaver','prosjekt','project'])
        lecture_words = []
        if self.download_lectures.get():
            lecture_words.extend(['forelesning','litteratur','foil','lecture','pensum','slides','curriculum'])
        for selected_course in self.listbox.curselection():
            self.ignored_courses.append(self.enc(self.listbox.get(selected_course)))
            print 'ignored',self.listbox.get(selected_course)
        # print self.ignored_courses

        def verify_assignment(root):
            for w in assignment_words:
                if w in root:
                    return True
            return False

        def verify_lecture(root):
            for w in lecture_words:
                if w in root:
                    return True
            return False

        def find_on_page(soup_source,tag,id=None):
            if id:
                return soup_source.find_all(tag,class_=id)
            else:
                return soup_source.find_all(tag,href=True)

        def add_file(w,c):
            _tmp = os.path.join(w,c)
            if not os.path.isdir(_tmp):
                os.makedirs(_tmp)
            else:
                print 'folder already exists'
            for filename in os.listdir(self.download_path):
                curfile = os.path.join(self.download_path, filename)
                if os.path.isfile(curfile) and '.DS' not in filename:
                    shutil.move(curfile,_tmp)

        for course,courseName in self.courses.items():
            if self.enc(courseName) in self.ignored_courses:
                print self.enc(courseName),'is an ignored course, skipping...'
                continue
            # create a folder - delete it later if no files were added
            working_dir = os.path.join(self.download_path,courseName.split(" ",1)[0])
            if not os.path.isdir(working_dir):
                os.makedirs(working_dir)
            lecture_folder = os.path.join(working_dir,'Lectures')
            if not os.path.isdir(lecture_folder):
                os.makedirs(lecture_folder)
            assignments_were_added = False
            lectures_were_added = False
            time.sleep(1)
            update_driver(self.its_base + 'main.aspx?CourseID=' + course)
            # locate the assignments
            print 'Exploring new course'

            for folder in find_on_page(self.new_soup(link['href']),'a'):
                dl_assignment = verify_assignment(folder.text.lower())
                dl_lecture = verify_lecture(folder.text.lower())
                if 'processfolder' in folder['href']:
                    print '> Yay, an assignment <'
                    for subfile in find_on_page(self.new_soup(link['href']),'a','GridTitle'):
                        subname = self.enc(subfile['title']).title()
                        update(self.its_base+subfile['href'])
                        foldersoup = self.new_soup(self.its_base+subfile['href'])

                        if dl_assignment:
                            # find the source of uploaded files
                            delivered = find_on_page(foldersoup,'div','ccl-filelist')
                            assignments_were_added = False
                            for d in delivered:
                                # check if the items can be downloaded
                                for dlink in d.find_all('a',href=True):
                                    if 'DownloadRedirect' in dlink['href']:
                                        # download the file
                                        self.driver.get(dlink['href'])
                                        assignments_were_added = True
                                time.sleep(0.5)
                            # update the folder tree
                            if assignments_were_added:
                                add_file(working_dir,subname)
                        if dl_lecture:
                            if 'animasjon' in subname: # fix for TDT4120
                                continue
                            lectures_were_added = False
                            for l in find_on_page(foldersoup,'a'):
                                if '/file/download' in l['href']:
                                    self.driver.get(self.its_base + l['href'][3:])
                                    print 'Downloading lecture'
                                    lectures_were_added = True
                            time.sleep(0.5)
                            if lectures_were_added:
                                for filename in os.listdir(self.download_path):
                                    curfile=os.path.join(self.download_path,filename)
                                    if os.path.isfile(curfile) and '.DS' not in filename:
                                        shutil.move(curfile,lecture_folder)


            # move all the files outside of the folder into working_dir
            if not assignments_were_added and not lectures_were_added:
                print 'Did not find any files for course '+courseName+', deleting folder'
                # os.rmdir(working_dir)
                shutil.rmtree(working_dir)
                time.sleep(0.1)

            # if lectures_were_added:
            #
            # elif lectures_:
            #     for filename in os.listdir(self.download_path):
            #         curfile=os.path.join(self.download_path,filename)
            #         if os.path.isfile(curfile) and '.DS' not in filename:
            #             print 'moving file!!! >',filename
            #             shutil.move(curfile, working_dir)
            #             time.sleep(0.1)
            #         else:
            #             continue


        self.driver.close()
        self.driver.quit()

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
        print 'Setting options in chrome'
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",{
                "download.default_directory": self.download_path,
                "download.prompt_for_download":False,
                "download.directory_upgrade":True,
                "safebrowsing.enabled":True,
                "plugins.always_open_pdf_externally": True,
                "download.target":"_blank"
            }
        )
        self.driver = webdriver.Chrome(chrome_options = options, executable_path = self.dir_path + self.chrome_driver)
        self.driver.get(self.ntnu_itslearning_url)

        def find_and_type(id,s,enter=False):
            tmp = self.driver.find_element_by_id(id)
            tmp.clear()
            tmp.send_keys(s)
            if enter:
                tmp.send_keys(Keys.ENTER)

        find_and_type('username',self.register_user)
        find_and_type('password',self.register_pw,True)

        soup = self.new_soup(self.courses_url)
        all_courses = Select(self.driver.find_element_by_tag_name('select'))
        # list all courses
        all_courses.select_by_value('All')  # All, Active, Archived
        # course_list=[]


        for link in soup.find_all('a', href=True):
            if 'CourseID' in link['href']:
                _course_id = self.enc(link['href'].split('=')[1])
                _course_name = self.enc(link.text)
                self.courses[_course_id] = _course_name

        for c in self.courses.values():
            #print c.decode('iso-8859-1')
            print self.enc(c)
            self.listbox.insert(END,c.decode('latin-1'))
        self.course_label.config(text="Select courses to IGNORE")
        self.start.config(state='enabled')
        self.btn_a.config(state='enabled')
        self.btn_l.config(state='enabled')


    def populate_courses(self,courses):
        for c in courses:
            self.listbox.insert(c)

    def clicked_assignments(self):
        print self.download_assignments.get()
        print self.download_lectures.get()
    def clicked_lecturenotes(self):
        print self.download_assignments.get()
        print self.download_lectures.get()
    def accept_input(self):
        f = self.frame
        self.user_label = Label(f,text="User",width=20)
        self.pw_label = Label(f,text="Password",width=20)
        self.user = Entry(f,text='',width=20)
        self.pw = Entry(f,text='',show='*',width=20)
        self.confirm = Button(f,text='Confirm login information',command=self.get_data)
        #self.lecture_notes = Checkbutton(f,text='Lecture notes',variable=BooleanVar(),command=self.clicked_lecturenotes)

    def init_ui(self):
        self.user_label.grid(row=0,column=1)
        self.pw_label.grid(row=1,column=1)
        self.user.grid(row=0,column=2)
        self.pw.grid(row=1,column=2,pady=10)
        self.confirm.grid(row=2,column=1,columnspan=4,pady=(5,10))

        self.course_label = Label(self.frame, text=self.download_path)
        self.listbox = Listbox(self.frame,selectmode=MULTIPLE,width=25,height=20)
        self.btn_load = Button(self.frame,text='Load courses', command=self.fetch_courses,state='disabled')
        self.btn_a = Checkbutton(self.frame,text='Assignments',command=self.clicked_assignments,variable=self.download_assignments,onvalue=1,offvalue=0,state='disabled')
        self.btn_l = Checkbutton(self.frame,text='Lecture notes',command=self.clicked_lecturenotes,variable=self.download_lectures,onvalue=1,offvalue=0,state='disabled')
        self.start = Button(self.frame,text='Download',command=self.run,state='disabled')

    def init_ui_download(self):
        #self.course_label = Label(self.frame,text="Click 'Load courses' and select what to download. Downloading lecture notes will download a huge amount of data")

        self.listbox.grid(row=4,column=1,columnspan=2,rowspan=20,sticky=W)
        self.btn_load.grid(row=4,column=3)
        self.btn_a.grid(row=5,column=3)
        self.btn_l.grid(row=6,column=3)
        self.start.grid(row=19,column=3)


    def wait_for_confirm(self):
        self.main.mainloop()

    def select_folder(self):
        currdir = os.getcwd()
        newdir = tkFileDialog.askdirectory(parent=self.main,initialdir=currdir,title='Select a download folder')
        if len(newdir)>0:
            print 'Selected',newdir
            newdir = os.path.join(newdir,'ItsLearningFiles')
            if not os.path.isdir(newdir):
                os.makedirs(newdir)
            self.download_path = newdir
            self.btn_load.config(state='enabled')
            self.course_label = Label(self.frame,text=self.download_path)
            self.course_label.grid(row=3,column=1,sticky=W,columnspan=3,pady=(5,5))
            #self.confirm.grid_forget()

            # self.confirm.grid_forget()
            # Label(self.frame,text="Downloading to "+newdir).grid(row=1,column=1,columnspan=4)
        else:
            print 'error, try again.'

    def get_data(self):
        self.init_ui_download()
        self.confirm.config(text='Select download folder',command=self.select_folder)
        self.register_user = self.user.get()
        self.register_pw = self.pw.get()
        if self.register_user=="" or self.register_pw=="":
            # Try again alert
            print 'Invalid login information'
            return
        print 'Pressed login'
        self.logged_in = True
        self.user.grid_forget()
        self.user_label.grid_forget()
        self.pw_label.grid_forget()
        self.pw.grid_forget()



        # show a button to choose download directory
        # choose_dir = Button(self.frame,text='Select folder',command=self.select_folder)
        # choose_dir.grid(row=3,column=1,sticky=S)




MW = MainWindow()
