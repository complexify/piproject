#updated as of 5/2/22
from tkinter import *
import random
import json
import speech_recognition as sr
from googletrans import Translator, constants

counter = 0
r = sr.Recognizer()
recording = True
DEBUG = False
miclist = sr.Microphone.list_microphone_names()
languages = constants.LANGUAGES
#randomly generated list of languages
randlangs = []
#every single language from the library
inputs1 = []
inputs1 = [str (lang) for lang in inputs1]
#the quiz question's list
quizques = []
#the possible answer choices
ans1 = []
ans2 = []
ans3 = []
ans4 = []
#the list of audio inputs
miclist1 = []
#the correct answers for each question 
correctans = []
#translator
translator = Translator()
#text that the quiz will be based off of
testtext = "The dog is blue"
#menucolor
bgcolor = "#CB333B"

#for loop to fetch all mic inputs
for i in miclist:
    miclist1.append(i)

#for loop to get all the languages from the library 
for j in languages.values():
    inputs1.append(j)

#while the counter is less than 4, it genertaes a random list of languages 
while counter < 4:
    thelang = random.choice(inputs1)
    randlangs.append(thelang)
    counter += 1

print(f"Random languages are:{randlangs}")
randval = ""
rnddict = {}

#gets the .json file and randomizes the order for the questions
def getjsons(jsonfile):
    #opening/loading the json portion
    with open(jsonfile) as f:
        global q, options, a, z, l
        obj = json.load(f)
    q = (obj['question'])
    options = (obj['options'])
    a = (obj['answer'])
    #"shuffling" the question/answers/options in a certain order
    z = zip(q,options,a)
    l = list(z)
    random.shuffle(l)
    q,options,a=zip(*l)
    #return questions, options, answers
    return q, options, a

#makes the json file that is required to generate the quiz
def maketheexam(valued):
    #generates the questions for the json file
    for val1 in randlangs:
        quizques.append(f"What is the following phrase in {val1}: '{valued}'")
        test = translator.translate(valued, dest = val1)
        #generates the possible options for the json file
        ans1.append(test.text)
        ans2.append(test.text)
        ans3.append(test.text)
        ans4.append(test.text)
        #generates the correct answer for the json file
        newindex = ans1.index(test.text)
        correctans.append(newindex + 1)
        #adds the specific keys and items to the dict
        rnddict.update({"question": quizques})
        rnddict.update({"answer": correctans})
        rnddict.update({"options":[ans1, ans2, ans3, ans4]})
    print(rnddict)
    #converts the dict to the json file in a specific way
    json_object = json.dumps(rnddict, ensure_ascii=False, indent= 4) 
    print(json_object)
    #opens the generatedd json file
    with open("test.json", "w", encoding="utf-8") as write_file:
        json.dump(rnddict, write_file, indent=4)
    getjsons('test.json') 

maketheexam(testtext)
getjsons('test.json')

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
                maketheexam(testtext)
                break
            except sr.UnknownValueError:
                print("Please repeat that, we couldn't understand what you just said!")

    #main panel that places the questions on this quiz itself, along with the starting page
    def question(self, qn):
        #title bar
        title_bar = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        title_bar.pack(expand=1, fill=X)
        label1 = Label(title_bar, text = "Language Learner [Demo]", bg = "#003087", fg = "#ffffff", font = ('Helvetica', 12, 'bold'), width = 25, relief = FLAT, highlightthickness=0)
        label1.pack(pady = 3)
        self.test1 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test1.pack()
        self.test2 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test2.pack()
        self.test3 = Frame(self.master, bg="#003087", highlightthickness=0, bd=2)
        self.test3.pack()
        self.mainwindow = Canvas(self.test1, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
        self.mainwindow.pack()
        self.secondwindow = Canvas(self.test2, bg = "#ffffff", width = 750, height = 450, highlightthickness=0)
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
        #===============================
        self.thetext = Label(self.master, text = testtext,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), anchor="w")
        self.mainwindow.create_window(375, 200, window=self.thetext)
        self.quest.set(str(self.qno)+". "+q[qn])
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
        self.ques['text'] = q[qn]
        for op in options[qn]:
              self.opts[val]['text'] = op
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
        if self.opt_selected.get() == a[qn]:
            return True

    #simply loads the next question, along with the options
    def nextbtn(self):
        #if selected option is correct, your total score adds a 1 to it
        if self.checkans(self.qn):
            self.correct += 1
        #moves onto next question and options whether ans is correct or not
        self.qn += 1
        self.qno += 1
        #if quiz is on last question, clicking next will end the exam and bring up the results panel
        if self.qn == len(q):
            self.display_result()      
        else:
            #if not the last question, it will shwo the next question in order
            self.quest.set(str(self.qno)+". "+q[self.qn])
            self.display_options(self.qn)   
        
    #a simple results function, that prints out your percentage, along with a gui that shows statistics of how you did
    def display_result(self):
        score = int(self.correct / len(q) * 100)
        result = f"{str(score)}"
        wc = len(q) - self.correct
        correct = f"{str(self.correct)}"
        wrong = f"{str(wc)}"
        self.test2.pack_forget()
        self.resultwindow.pack()
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
        print(f"Right:  Wrong:  Score: \n{correct}\t{wrong}\t{result}%")
    
    #the starting button that loads the quiz pages
    def start(self):
        self.test1.pack_forget()
        self.secondwindow.pack()

#loading the window
window = Tk()
window.configure(bg = "#003087")
window.geometry("750x500")
window.resizable(False, False)
app = Quiz(window)
window.mainloop()