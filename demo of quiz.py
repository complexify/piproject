from tkinter import *
from tkinter import messagebox as mb
import random
import json
import speech_recognition as sr
from googletrans import Translator, constants

counter = 0
counter1 = 0
counter2 = 0
counter3 = 0
languages = constants.LANGUAGES
randlangs = []
thechoices = []
inputs1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
correctans = []
inputs1 = [str (lang) for lang in inputs1]
translator = Translator()
text = "A dog jumped over the fence"
for j in languages.values():
    inputs1.append(j)

while counter < 4:
    thelang = random.choice(inputs1)
    randlangs.append(thelang)
    counter += 1

print(f"Random languages are:{randlangs}")
counter2 = 0
randval = ""
rnddict = {}
for val1 in randlangs:
    list2.append(f"What is the following phrase in {val1}: \n '{text}'")
    test = translator.translate(text, dest = val1)
    list3.append(test.text)
    list4.append(test.text)
    list5.append(test.text)
    list6.append(test.text)
    newindex = list3.index(test.text)
    correctans.append(newindex + 1)
    ques = f"What is {text} in {val1}"
    rnddict.update({"question":list2})
    rnddict.update({"answer": correctans})
    rnddict.update({"options":[list3, list4, list5, list6]})

print(rnddict)
json_object = json.dumps(rnddict, ensure_ascii=False, indent= 4) 
print(json_object)

with open("test.json", "w", encoding="utf-8") as write_file:
    json.dump(rnddict, write_file, indent=4)

root = Tk()
root.geometry("800x500")
root.configure(bg = "#ffffff")
root.title("Demo")
with open('test.json') as f:
    obj = json.load(f)
q = (obj['question'])
options = (obj['options'])
a = (obj['answer'])
z = zip(q,options,a)
l = list(z)
random.shuffle(l)
q,options,a=zip(*l)


class Quiz:
    def __init__(self):
        self.qn = 0
        self.qno = 1
        self.quest = StringVar()
        self.ques = self.question(self.qn)
        self.opt_selected = IntVar()
        self.opts = self.radiobtns()
        self.display_options(self.qn)
        self.buttons()
        self.correct = 0

    def question(self, qn):
        t = Label(root, text="Language Quiz v1.0", width=50, bg="#7289da", fg="white", font=("ariel", 20, "bold"))
        t.place(x=0, y=2)
        self.quest.set(str(self.qno)+". "+q[qn])
        qn = Label(root, textvariable = self.quest,bg = "#ffffff",fg="#000000",  width=60, font=("ariel", 16, "bold"), anchor="w")
        qn.place(x=70, y=100)
        return qn

    def radiobtns(self):
        val = 0
        b = []
        yp = 150
        while val < 4:
            btn = Radiobutton(root, text=" ", variable=self.opt_selected,bg = "#ffffff", value=val + 1, font=("ariel", 14))
            b.append(btn)
            btn.place(x=100, y=yp)
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
        nbutton = Button(root, text="Next",command=self.nextbtn, width=10,bg="#2c2f33",fg="white",font=("ariel",16,"bold"), relief= FLAT)
        nbutton.place(x=100,y=380)

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
        print(f"Right:  Wrong:  Score: \n{correct}\t{wrong}\t{result}%")



quiz=Quiz()
root.mainloop()


