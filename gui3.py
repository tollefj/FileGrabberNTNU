from Tkinter import *
from ttk import *

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

        for c in range(4):
            self.main.grid_columnconfigure(c,weight=1)
            self.main.grid_rowconfigure(c,weight=1)

        self.start = None # the button to start the program

        self.accept_input()
        self.init_ui()
        self.wait_for_confirm()

    def run(self):
        print '>>>Main program running!'

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

    def create_list(self):
        self.listbox = Listbox(self.frame,selectmode=MULTIPLE,width=15,height=15)

    def accept_input(self):
        f = self.frame
        self.user = Entry(f,text='',width=20)
        self.pw = Entry(f,text='',show='*',width=20)
        self.confirm = Button(f,text='Confirm login information',command=self.get_data)
        self.start = Button(f,text='Download',command=self.run)

    def init_ui(self):
        Label(self.frame,text="User",width=20).grid(row=0,column=1)
        Label(self.frame,text="Password",width=20).grid(row=1,column=1)
        self.user.grid(row=0,column=2)
        self.pw.grid(row=1,column=2,pady=10)
        self.confirm.grid(row=2,column=1,columnspan=4)
        self.create_list()

    def wait_for_confirm(self):
        self.main.mainloop()

    def get_data(self):
        Label(self.frame,text="Courses",width=15).grid(row=3,column=0,columnspan=2,sticky=W)
        self.listbox.grid(row=4,column=1,sticky=W,pady=10)
        self.register_user = self.user.get()
        self.register_pw = self.pw.get()
        self.user.config(state='disabled')
        self.pw.config(state='disabled')
        self.confirm.config(state='disabled',text='Logged in')
        print self.register_user, self.register_pw

MW = MainWindow()
