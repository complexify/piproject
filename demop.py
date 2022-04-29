from tkinter import *
from tkinter import messagebox as mb
import random
import json
import speech_recognition as sr
from googletrans import Translator, constants
import os
counter = 0
counter1 = 0
counter2 = 0
counter3 = 0
r = sr.Recognizer()
recording = True
DEBUG = False
miclist = sr.Microphone.list_microphone_names()
languages = constants.LANGUAGES
randlangs = []
thechoices = []
inputs1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
miclist1 = []
correctans = []
inputs1 = [str (lang) for lang in inputs1]
translator = Translator()
testtext = "The dog is blue"
newcounter = 0
for i in miclist:
    miclist1.append(i)
for j in languages.values():
    inputs1.append(j)

while counter < 4:
    thelang = random.choice(inputs1)
    randlangs.append(thelang)
    counter += 1

print(f"Random languages are:{randlangs}")
counter2 = 0
randval = ""
checkcounter = 0
rnddict = {}

def getjsons(jsonfile):
    with open(jsonfile) as f:
        global q, options, a, z, l
        obj = json.load(f)
    q = (obj['question'])
    options = (obj['options'])
    a = (obj['answer'])
    z = zip(q,options,a)
    l = list(z)
    random.shuffle(l)
    q,options,a=zip(*l)
    return q, options, a

def maketheexam(valued):
    for val1 in randlangs:
        list2.append(f"What is the following phrase in {val1}: '{valued}'")
        test = translator.translate(valued, dest = val1)
        list3.append(test.text)
        list4.append(test.text)
        list5.append(test.text)
        list6.append(test.text)
        newindex = list3.index(test.text)
        correctans.append(newindex + 1)
        ques = f"What is {valued} in {val1}"
        rnddict.update({"question":list2})
        rnddict.update({"answer": correctans})
        rnddict.update({"options":[list3, list4, list5, list6]})
    print(rnddict)
    json_object = json.dumps(rnddict, ensure_ascii=False, indent= 4) 
    print(json_object)
    with open("test.json", "w", encoding="utf-8") as write_file:
        json.dump(rnddict, write_file, indent=4) 
    getjsons('test.json') 
maketheexam(testtext)
getjsons('test.json')

bgcolor = "#CB333B"
class Quiz(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.qn = 0
        self.qno = 1
        self.quest = StringVar()
        self.ques = self.question(self.qn)
        self.opt_selected = IntVar()
        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.correct = 0

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


    def question(self, qn):
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
        self.thetext = Label(self.master, text = testtext,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), anchor="w")
        self.mainwindow.create_window(375, 200, window=self.thetext)
        self.quest.set(str(self.qno)+". "+q[qn])
        qn = Label(self.master, textvariable = self.quest,bg = "#ffffff",fg="#000000", font=('Helvetica', 16, "bold"), width = 50, anchor="w", wraplength = 600)
        self.secondwindow.create_window(375, 50, window=qn)
        return qn

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

    def display_options(self, qn):
        val = 0
        self.opt_selected.set(0)
        self.ques['text'] = q[qn]
        for op in options[qn]:
              self.opts[val]['text'] = op
              val += 1

    def buttons(self):
        nbutton = Button(self.master, text="Next",command=self.nextbtn, width=50,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.secondwindow.create_window(375, 380, window=nbutton)
        startbutton = Button(self.master, text="Generate Exam",command=self.start, width=50,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.mainwindow.create_window(375, 380, window=startbutton)
        startbutton = Button(self.master, text="Record",command=self.evalaudio,bg="#CB333B",fg="white",font=('Helvetica',16,"bold"), relief= FLAT)
        self.mainwindow.create_window(375, 150, window=startbutton)


    def checkans(self, qn):
        if self.opt_selected.get() == a[qn]:
            return True

    def nextbtn(self):
        if self.checkans(self.qn):
            self.correct += 1
        self.qn += 1
        self.qno += 1
        if self.qn == len(q):
            self.display_result()      
        else:
            self.quest.set(str(self.qno)+". "+q[self.qn])
            self.display_options(self.qn)   
        

    def display_result(self):
        score = int(self.correct / len(q) * 100)
        result = f"{str(score)}"
        wc = len(q) - self.correct
        correct = f"{str(self.correct)}"
        wrong = f"{str(wc)}"
        self.test2.pack_forget()
        self.resultwindow.pack()
        if score > 70:
            pasfail = "passed"
            acolor = "#00FF00"
        else:
            pasfail = "failed"
            acolor = "#ff0000"
        results1 = Label(self.master, text = f"You {pasfail} with a {result}%", bg = "#ffffff",fg=acolor, font=('Helvetica', 16, "bold"), anchor="w")
        self.resultwindow.create_window(375, 50, window=results1)
        print(f"Right:  Wrong:  Score: \n{correct}\t{wrong}\t{result}%")
    
    def start(self):
        self.test1.pack_forget()
        self.secondwindow.pack()

window = Tk()
window.configure(bg = "#003087")
window.geometry("750x500")
window.resizable(False, False)
app = Quiz(window)
window.mainloop()