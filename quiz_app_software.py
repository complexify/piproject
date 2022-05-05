from tkinter import *
from unittest import result
import speech_recognition as sr
from googletrans import Translator, constants
from random import shuffle
import json
import os
# CONSTANTS
# picking random languages
r = sr.Recognizer()
recording = True
miclist = sr.Microphone.list_microphone_names()
miclist1 = []
for i in miclist:
    miclist1.append(i)
class Assignments(Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master, bg = "#ffffff")
        self.files = os.listdir(os.getcwd()+ f"/exams")
        self.FILE = f"exam{len(self.files)+1}.json"
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.SetupAssignments()

    def SetupAssignments(self):
        filecolumn = 2
        assignments = Label(self, text = " Your Assignments:",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w",width = 100)
        assignments.grid(row = 1, column = 0, columnspan = 5, sticky=W, ipady = 12)
        back = Button(self, text = "Back",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"), command = self.goback, width = 10, relief= FLAT)
        back.grid(row = 1, column = 5, sticky=W, ipady = 6)
        for file in self.files:
            examtitle = Label(self, text = file.split(".")[0],bg = "#ffffff",fg="#003087", font=('Helvetica', 16), width = 10)
            examtitle.grid(row = filecolumn, column = 0,columnspan = 5,ipady = 6, sticky=W)
            key = file.split(".")[0][4:]
            if (key not in AppBuilder.results.keys()):
                exambutton = Button(self, text = "Attempt",bg = "#CB333B",fg="#ffffff", font=('Helvetica', 16, "bold"), width = 10, command = lambda file=file: self.taketest(file), relief= FLAT)
                exambutton.grid(row = filecolumn, column = 4, pady=5, ipady = 6, sticky=W)
            else:
                exambutton = Button(self, text = "Review",bg = "#CB333B",fg="#ffffff", font=('Helvetica', 16, "bold"), command = lambda key=key: self.review(key), relief= FLAT)
                exambutton.grid(row = filecolumn, column = 4,padx=5, pady=5, sticky=W)
            filecolumn += 1
        self.pack()
    
    def goback(self):
        self.pack_forget()
        Dashboard.__init__(self, self.master)

    def review(self, key):
        theresults1 = f"exam{key}"
        theresults = AppBuilder.results[key]
        self.pack_forget()
        Overview.__init__(self, self.master, theresults, theresults1)


    def taketest(self, file):
        exam = self.loadJSON(f"exams/{file}")
        self.pack_forget()
        examNumber = file.split(".")[0][4:]
        Quiz.__init__(self, self.master, exam, examNumber)

    def loadJSON(self, file):
        with open(file) as f:
            exam = json.load(f)
            print(exam)
            return exam

class Settings(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "#ffffff")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.SetupSettings()
        self.languages = constants.LANGUAGES
        self.langs = list(self.languages.values())
        shuffle(self.langs)
        self.langs = self.langs[:4]
        # self.createQuiz("what", self.langs)

    def SetupSettings(self):
        
        settingstab = Label(self, text = " Settings",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w", width = 58)
        settingstab.grid(row = 1, column = 0, columnspan = 5, sticky=W, ipady = 12)
        back1 = Button(self, text = "Back",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"), command = self.goback, width = 10, relief= FLAT)
        back1.grid(row = 1, column = 5, sticky=W, ipady = 6)
        inputbutton2 = Label(self, text = "Exam Maker:",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, 'bold'), width = 10)
        inputbutton2.grid(row = 2, column = 0,columnspan = 3, ipady = 6,  padx=10, pady=10, sticky=W)
        inputbutton = Label(self, text = "Select Input:",bg = "#ffffff",fg="#003087", font=('Helvetica', 16), width = 10)
        inputbutton.grid(row = 3, column = 0,columnspan = 3, ipady = 6,  padx=10, pady=10, sticky=W)
        clicked = StringVar(self)
        clicked.set(" select microphone ")
        def change_dropdown(*args):
            global mic
            num = miclist1.index(clicked.get())
            mic = sr.Microphone(device_index=num)
            print(mic)
            return mic
        clicked.trace('w', change_dropdown)
        drop = OptionMenu(self, clicked , *miclist1)
        drop.grid(row = 3, column = 3,ipady = 6, sticky=W, padx=10, pady=10)
        inputbutton1 = Button(self, text = "Record",bg = "#003087",fg="#ffffff", font=('Helvetica', 16), width = 10,relief= FLAT, command = self.evalaudio)
        inputbutton1.grid(row = 3, column = 4,ipady = 6,  padx=10, pady=10, sticky=W)
        self.pack()

    def evalaudio(self):
        while recording:
            with mic as input:
                r.adjust_for_ambient_noise(input)
                testaudio = r.listen(input)
            try:
                inputedaudio = r.recognize_google(testaudio)
                testtext = inputedaudio
                print(testtext)
                self.createQuiz(testtext, self.langs)
                break
            except sr.UnknownValueError:
                print("Please repeat that, we couldn't understand what you just said!")

    def goback(self):
        self.pack_forget()
        Dashboard.__init__(self, self.master)
        
    def createQuiz(self, text, langs):
        translator = Translator()
        exam = []
        selections = [{"language": lang, "translation-result": translator.translate(text, dest = lang).text} for lang in langs]
        for lang in langs:
            temp = {}
            temp["question"] = f"What is the following phrase in {lang}: '{text}'"
            temp["selections"] = selections
            cnt = 0 # counter
            for select in selections:
                cnt += 1
                if (select["language"] == lang):
                    temp["correct-index"] = cnt
            exam.append(temp)
        self.saveJSON(exam)

    def saveJSON(self, exam):
        FOLDER = "exams"
        files = os.listdir(os.getcwd()+ f"/{FOLDER}")
        FILE = f"exams/exam{len(files)+1}.json"
        with open(FILE, "w", encoding="utf-8") as write_file:
            json.dump(exam, write_file, indent=4)

class Quiz(Frame):
    def __init__(self, master, exam, examNumber):
        Frame.__init__(self, master, bg = "#ffffff")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.exam = exam
        self.examNumber = examNumber
        self.counter = 0
        self.correct = 0
        self.isSelected = IntVar()
        self.SetupQuiz()
    
    def SetupQuiz(self):
        self.questionDisplay(self.exam[self.counter])
        quizmode = Label(self, text = " Menu Functionality Limited",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w", width = 58)
        quizmode.grid(row = 1, column = 0, columnspan = 5, sticky=W, ipady = 12)
        nextButton = Button(self, text="Next",command=self.nextButtonAction, width=10,bg="#2c2f33",fg="white",font=("ariel",16,"bold"), relief= FLAT)
        nextButton.grid(row=8, column=0)
        self.pack()

    def questionDisplay(self, question):
        questionLabel = Label(self, text = question["question"], bg = "#ffffff",fg="#000000",  width=60, font=("ariel", 16, "bold"), anchor="w")
        questionLabel.grid(row=2, column=0)

        #radio
        val = 0
        optionrow = 3
        while val < len(question["selections"]):
            option = Radiobutton(self, text=question["selections"][val]["translation-result"], variable=self.isSelected, bg = "#ffffff", value=val + 1,anchor="w", font=("ariel", 14))
            option.grid(row=optionrow, column = 0, padx=5, pady=5, sticky=W)
            val += 1
            optionrow +=1
   
    def nextButtonAction(self):
        self.counter += 1
        if self.isSelected.get() == self.exam[self.counter-1]["correct-index"]:
            self.correct += 1
        if self.counter < len(self.exam):
            self.isSelected.set(0)
            self.SetupQuiz()
        else:
            AppBuilder.results[self.examNumber] = self.correct/len(self.exam)*100
            
            self.pack_forget()
            Dashboard.__init__(self, self.master)

class Overview(Frame):
    def __init__(self, master, theresults, theresults1):
        Frame.__init__(self, master, bg = "#ffffff")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.theresults = theresults
        self.theresults1 = theresults1
        self.SetupOverview()

    def SetupOverview(self):
        overviewtab = Label(self, text = " Overview",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w", width = 58)
        overviewtab.grid(row = 1, column = 0, columnspan = 5, sticky=W, ipady = 12)
        back1 = Button(self, text = "Back",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"), command = self.goback, width = 10, relief= FLAT)
        back1.grid(row = 1, column = 5, sticky=W, ipady = 6)
        examstaken = Label(self, text = f"{self.theresults1}",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, 'bold'), width = 10)
        examstaken.grid(row = 2, column = 1, ipady = 6,  padx=10, pady=10, sticky=E+W+N+S)
        examstaken1 = Label(self, text = f"Grade:{self.theresults}",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, 'bold'), width = 10)
        examstaken1.grid(row = 2, column = 2, ipady = 6,  padx=10, pady=10, sticky=E+W+N+S)
        self.pack()
    
    def goback(self):
        self.pack_forget()
        Dashboard.__init__(self, self.master)

class Grades(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "#ffffff")
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.theresults = False
        self.SetupGrades()

    def SetupGrades(self):
        gradesrow = 4
        gradescolumn = 1
        add = 0
        addcount = 0
        gradestab = Label(self, text = " Grades",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w", width = 58)
        gradestab.grid(row = 1, column = 0, columnspan = 5, sticky=W, ipady = 12)
        back1 = Button(self, text = "Back",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"), command = self.goback, width = 10, relief= FLAT)
        back1.grid(row = 1, column = 5, sticky=W, ipady = 6)
        if AppBuilder.results:
            gradechart = Label(self, text = f"Exam Title:",bg = "#CB333B",fg="#000000", font=('Helvetica', 16, 'bold'), width = 8)
            gradechart.grid(row = 3, column = 1, ipady = 5,  padx=10, pady=10, sticky=E+W+N+S)
            gradepchart = Label(self, text = f"Grade Scored:",bg = "#CB333B",fg="#000000", font=('Helvetica', 16, 'bold'), width = 12)
            gradepchart.grid(row = 3, column = 2, ipady = 5,  padx=10, pady=10, sticky=E+W+N+S)
            for keys, items in AppBuilder.results.items():
                add += items
                addcount += 1
                examstaken = Label(self, text = f"Exam{keys}",bg = "#ffffff",fg="#000000", font=('Helvetica', 16), width = 8)
                examstaken.grid(row = gradesrow, column = gradescolumn, ipady = 5,  padx=10, pady=10, sticky=E+W+N+S)
                examstaken = Label(self, text = f"{items}%",bg = "#ffffff",fg="#000000", font=('Helvetica', 16), width = 8)
                examstaken.grid(row = gradesrow, column = gradescolumn + 1, ipady = 5,  padx=10, pady=10, sticky=E+W+N+S)
                gradesrow +=1
            average = add / addcount
            gpa = Label(self, text = f"Current Overall Grade:{average}%",bg = "#ffffff",fg="#003087", font=('Helvetica', 16, 'bold'), width = 10)
            gpa.grid(row = 2, column = 1,columnspan=2, ipady = 6,  padx=10, pady=10, sticky=E+W+N+S)
        else:
            examstaken = Label(self, text = f"You haven't taken any exams yet",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, 'bold'), width = 10)
            examstaken.grid(row = 2, column = 1, ipady = 6,  padx=10, pady=10, sticky=E+W+N+S)
        self.pack()
    
    def goback(self):
        self.pack_forget()
        Dashboard.__init__(self, self.master)

class Dashboard(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "#ffffff")
        self.SetupDashboard()
        print(AppBuilder.results)



    def SetupDashboard(self):
        titlebar1 = Label(self, text = f" Techie's Translator ",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),anchor="w", width = 58)
        titlebar1.grid(row = 0, column = 0, columnspan=4,sticky=E+W+N+S, ipady = 8)
        titlebar = Label(self, text = f" Welcome, {os.getlogin()}",bg = "#003087",fg="#CB333B", font=('Helvetica', 12),anchor="w", width = 40)
        titlebar.grid(row = 1, column = 0, columnspan=4,sticky=E+W+N+S, ipady = 4)
        tab1 = Button(self, text = "Assignments",bg = "#003087",fg="#ffffff", font=('Helvetica', 16),relief= FLAT, width = 18, height=2, command = lambda: self.openPage(1))
        tab1.grid(row = 2, column= 1, padx=5, pady=30, sticky=W)

        tab2 = Button(self, text = "Grades",bg = "#003087",fg="#ffffff", font=('Helvetica', 16),relief= FLAT, width = 18, height=2, command = lambda: self.openPage(2))
        tab2.grid(row = 2, column= 2, padx=5, pady=30, sticky=W)

        tab3 = Button(self, text = "Settings",bg = "#003087",fg="#ffffff", font=('Helvetica', 16),relief= FLAT, width = 18, height=2, command = lambda: self.openPage(3))
        tab3.grid(row = 2, column= 3, padx=5, pady=30, sticky=W)

        self.pack()

    def openPage(self, page):
        if (page == 1):
            self.pack_forget()
            Assignments.__init__(self, self.master)
        elif (page == 2):
            self.pack_forget()
            Grades.__init__(self, self.master)
        elif (page == 3):
            self.pack_forget()
            Settings.__init__(self, self.master)

class AppBuilder(Dashboard, Quiz, Settings, Assignments, Overview, Grades):
    results = {}
    missed = {}
    def __init__(self, master):
        Dashboard.__init__(self, master)

#loading the window
window = Tk()
window.configure(bg = "#ffffff")
window.geometry("760x500")
window.resizable(False, False)
app = AppBuilder(window)
window.mainloop()