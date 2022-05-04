from tkinter import *
import speech_recognition as sr
from googletrans import Translator, constants
from random import shuffle
import json

# CONSTANTS
testcounter = 1
languages = constants.LANGUAGES
FILE = f"exam{testcounter}.json"
# picking random languages
langs = list(languages.values())
shuffle(langs)
langs = langs[:4]
incorrect = []
incorrectans = []
overviewlist = []
exams = []
# Shows languages selected
print(langs)

def createQuiz(text, langs):
    translator = Translator()
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
        exams.append(exam)
def saveJSON(exam, file):
    for exam in exams:
        with open(file, "w", encoding="utf-8") as write_file:
            json.dump(exam, write_file, indent=4)


def loadJSON(file):
    global exam
    with open(file) as f:
        exam = json.load(f)
        return exam
exam = []
try:
    exam = loadJSON(FILE)
except:
    createQuiz("hey", langs)

# saveJSON(exam, FILE)
# print(exam)

r = sr.Recognizer()

recording = True

miclist = sr.Microphone.list_microphone_names()
miclist1 = []

for i in miclist:
    miclist1.append(i)

testtext = ""
settingstab = False
quiztab = False
overviewtab = False
resultstab = False
hasattempted = False
class Quiz(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        #variables for generating each question/options' elements
        self.qn = 0
        self.qno = 1
        self.quest = StringVar()
        self.ques = self.question(self.qn)
        self.opt_selected = IntVar()
        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.correct = 0
    
    #recieves audio input from the selected audio input
    def evalaudio(self):
        while recording:
            with mic as input:
                r.adjust_for_ambient_noise(input)
                testaudio = r.listen(input)
            try:
                inputedaudio = r.recognize_google(testaudio)
                testtext = inputedaudio
                print(testtext)
                createQuiz(testtext, langs)
                FILE = f"test{testcounter}.json"
                saveJSON(exam, FILE)
                print(FILE)
                break
            except sr.UnknownValueError:
                print("Please repeat that, we couldn't understand what you just said!")

    #main panel that places the questions on this quiz itself, along with the starting page
    def question(self, qn):
        #title bar
        title_bar = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        title_bar.pack()
        self.title = Canvas(title_bar,  bg = "#003087", width = 750, height = 50, highlightthickness=0)
        self.title.pack()
        label1 = Label(title_bar, text = "Techie's Translator Game", bg = "#003087", fg = "#ffffff", font = ('Helvetica', 12, 'bold'), width = 25, relief = FLAT, highlightthickness=0)
        self.title.create_window(110, 25, window=label1)
        menubar = Button(title_bar, text = "Dashboard", bg = "#003087", fg = "#ffffff", font = ('Helvetica', 12, 'bold'), relief = FLAT, highlightthickness=0, command = self.dashboard)
        self.title.create_window(680, 25, window=menubar)
        self.test1 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test1.pack()
        self.test2 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test2.pack()
        self.test3 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test3.pack()
        self.test4 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test4.pack()
        self.test5 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test5.pack()
        self.mainwindow = Canvas(self.test1, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        self.secondwindow = Canvas(self.test2, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        self.thirdwindow = Canvas(self.test4, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        self.fourthwindow = Canvas(self.test5, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        #dashboard
        self.dash = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.dash.pack()
        self.dash1 = Canvas(self.dash, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        self.dash1.pack()
        tab1 = Button(self.master, text = "Assignments",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),padx = 20,pady = 16, command = self.openpage2)
        self.dash1.create_window(150, 100, window=tab1)
        tab2 = Button(self.master, text = "Overview",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),padx = 20,pady = 16, command = self.openpage3)
        self.dash1.create_window(375.5, 100, window=tab2)
        tab3 = Button(self.master, text = "Settings",bg = "#003087",fg="#ffffff", font=('Helvetica', 16, "bold"),padx = 20,pady = 16, command = self.openpage1)
        self.dash1.create_window(600, 100, window=tab3)
        self.resultwindow = Canvas(self.test3, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        #input method dropdown
        starting = Label(self.master, text = "Input Method:",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), anchor="w")
        self.mainwindow.create_window(187.5, 50, window=starting)
        clicked = StringVar(self)
        clicked.set(" select microphone ")
        def change_dropdown(*args):
            global mic
            num = miclist1.index(clicked.get())
            mic = sr.Microphone(device_index=num)
            print(mic)
            return mic
        clicked.trace('w', change_dropdown)
        drop = OptionMenu(self.master, clicked , *miclist1)
        self.mainwindow.create_window(562.5, 50, window=drop)
        self.examstart = Label(self.master, text = FILE[:5],bg = "#ffffff",fg="#003087", font=('Helvetica', 16, "bold"), anchor="w")
        self.fourthwindow.create_window(150, 50, window=self.examstart)
        self.exambutton = Button(self.master, text = "Attempt",bg = "#CB333B",fg="#ffffff", font=('Helvetica', 16, "bold"), anchor="w", command = self.taketest, relief= FLAT)
        self.fourthwindow.create_window(600, 50, window=self.exambutton)

        #===============================
        self.thetext = Label(self.master, text = testtext,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), anchor="w")
        self.mainwindow.create_window(375, 200, window=self.thetext)
        if hasattempted == False:
            self.overtext1 = Label(self.master, text = "You haven't attempted any quizes.",bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), wraplength = 500, anchor="w")
            self.thirdwindow.create_window(375, 50, window=self.overtext1)
        self.quest.set(str(self.qno)+". "+exam[qn]["question"])
        qn = Label(self.master, textvariable = self.quest,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), width = 50, anchor="w", wraplength = 600)
        self.secondwindow.create_window(375, 50, window=qn)
        return qn
    
    #makes the question's options
    def radiobtns(self):
        val = 0
        b = []
        yp = 150
        while val < 4:
            btn = Radiobutton(self.master, text=" ", variable=self.opt_selected,bg = "#ffffff", value=val + 1, font=('Helvetica', 14), width = 50, anchor="w", relief = FLAT)
            b.append(btn)
            self.secondwindow.create_window(375, yp, window=btn)
            val += 1
            yp += 40
        return b
    #actually generates the question's options onto the gui
    def display_options(self, qn):
        val = 0
        self.opt_selected.set(0)
        self.ques['text'] = exam[qn]["question"]
        for op in exam[qn]["selections"]:
              self.opts[val]['text'] = op["translation-result"]
              val += 1

    #various buttons that make the gui work
    def buttons(self):
        nbutton = Button(self.master, text="Next",command=self.nextbtn, width=50,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.secondwindow.create_window(375, 380, window=nbutton)
        startbutton = Button(self.master, text="Generate Exam",command=self.start, width=50,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.mainwindow.create_window(375, 380, window=startbutton)
        startbutton = Button(self.master, text="Record",command=self.evalaudio,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.mainwindow.create_window(375, 150, window=startbutton)

    #checks to see if your selected radio button is the same as the correct answer's value
    def checkans(self, qn):
        if self.opt_selected.get() == exam[qn]["correct-index"]:
            return True
        else:
            incorrect.append(qn+1)
            for testval in exam[qn]["selections"]:
                incorrectans.append(testval["translation-result"])
    

            

    #simply loads the next question, along with the options
    def nextbtn(self):
        #if selected option is correct, your total score adds a 1 to it
        if self.checkans(self.qn):
            self.correct += 1
        #moves onto next question and options whether ans is correct or not
        self.qn += 1
        self.qno += 1
        #if quiz is on last question, clicking next will end the exam and bring up the results panel
        if self.qn == len(exam):
            self.display_result()      
        else:
            #if not the last question, it will shwo the next question in order
            self.quest.set(str(self.qno)+". "+exam[self.qn]["question"])
            self.display_options(self.qn)   
        
    #a simple results function, that prints out your percentage, along with a gui that shows statistics of how you did
    def display_result(self):
        global resultstab
        resultstab = True
        score = int(self.correct / len(exam) * 100)
        result = f"{str(score)}"
        wc = len(exam) - self.correct
        correct = f"{str(self.correct)}"
        wrong = f"{str(wc)}"
        self.test2.pack_forget()
        self.resultwindow.pack()
        self.title.pack()
        #if you did better than a 70, color is green
        if score > 70:
            pasfail = "passed"
            acolor = "#00FF00"
        else:
            #if you did worse than a 70, color is red
            pasfail = "failed"
            acolor = "#ff0000"
        #gui element that prints your results
        results1 = Label(self.master, text = f"You {pasfail} with a {result}%", bg = "#ffffff",fg=acolor, font=('Helvetica', 16, "bold"), anchor="w")
        self.resultwindow.create_window(375, 50, window=results1)
        #prints your resutls in the console as well
        overviewlist.append(f"You made a {result}% \nYou missed questions: {incorrect}")
        print(overviewlist)
        for grades in overviewlist:
            self.overtext = Label(self.master, text = grades,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), wraplength = 500, anchor="w")
            self.thirdwindow.create_window(375, 60, window=self.overtext)
        print(f"Right:  Wrong:  Score: \n{correct}\t{wrong}\t{result}%")

    
    #the starting button that loads the quiz pages
    def start(self):
        global settingstab
        self.test1.pack_forget()
        self.dash.pack()
        settingstab = False

    def dashboard(self):
        global settingstab, quiztab, overviewtab, resultstab
        if settingstab:
            self.test1.pack_forget()
            settingstab = False
        if quiztab:
            self.test5.pack_forget()
            quiztab = False
        if overviewtab:
            self.test4.pack_forget()
            overviewtab = False
        if resultstab:
            self.test3.pack_forget()
            resultstab = False
        self.dash.pack()

    def openpage1(self):
        global settingstab
        if settingstab == False:
            self.test1.pack()
            self.mainwindow.pack()
            self.dash.pack_forget()
            settingstab = True

    def openpage2(self):
        global quiztab
        if quiztab == False:
            self.test5.pack()
            self.fourthwindow.pack()
            self.dash.pack_forget()
            quiztab = True

    def openpage3(self):
        global overviewtab
        if overviewtab == False:
            self.test4.pack()
            self.thirdwindow.pack()
            self.dash.pack_forget()
            overviewtab = True

    def taketest(self):
        global hasattempted, overviewtab
        self.exambutton['text'] = "Review"
        if hasattempted == False:
            self.test2.pack()
            self.secondwindow.pack()
            self.fourthwindow.pack_forget()
            self.title.pack_forget()    
            hasattempted = True     
        if hasattempted == True:
            self.overtext1['text'] = ""
            self.test4.pack()
            self.thirdwindow.pack()
            self.test5.pack_forget()
            overviewtab = True
            

            



#loading the window
window = Tk()
window.configure(bg = "#003087")
window.geometry("750x500")
window.resizable(False, False)
app = Quiz(window)
window.mainloop()