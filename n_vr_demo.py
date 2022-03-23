from tkinter import *
import speech_recognition as sr
from googletrans import Translator, constants

status = "Connected to API"
class colors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
print(f"{colors.FAIL}Demo voice recognition program{colors.RESET}")
if status != sr.RequestError:
    print(f"Status: {colors.OK}{status}{colors.RESET}")

test = "test"
r = sr.Recognizer()
recording = True
DEBUG = False
test = sr.Microphone.list_microphone_names()
languages = constants.LANGUAGES
inputs = []
inputs1 = []
translator = Translator()
translation = translator.translate("test", dest = "arabic")
print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

for j in languages.values():
    inputs1.append(j)


for i in test:
    inputs.append(i)
  
class App(Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title('Voice Recogniton Test')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(3, weight=1)
        self.columnconfigure(3, weight=3)

        self.create_widgets()

    def create_widgets(self):
        
        input_label = Label(self, text="input method: ")
        input_label.grid(column=0, row=0, sticky= W, padx=5, pady=5)


        

        clicked = StringVar(self)
        clicked.set("")

        def change_dropdown(*args):
            global mic
            num = inputs.index(clicked.get())
            mic = sr.Microphone(device_index=num)
            return mic
        

        clicked.trace('w', change_dropdown)

        drop = OptionMenu(self , clicked , *inputs)
        drop.grid(column=1, row=0, sticky= W, padx=5, pady=5)
        
        clicked1 = StringVar(self)
        clicked1.set("")

        def change_dropdown1(*args):
            global translang
            translang = inputs1.index(clicked1.get())
            return translang
        clicked1.trace('w', change_dropdown1)

        drop1 = OptionMenu(self , clicked1 , *inputs1)
        drop1.grid(column=1, row=1, sticky= W, padx=5, pady=5)

        translate_label = Label(self, text="Translation Language: ")
        translate_label.grid(column=0, row=1, sticky= W, padx=5, pady=5)  

        record = Button(self, text= "Record", command = self.evalaudio)
        record.grid(column=0, row=2, sticky= W, padx=5, pady=5, columnspan = 5)

        self.audio_label = Label(self, text="", wraplength = 300)
        self.audio_label.grid(column=0, row=3, sticky= W, padx=5, pady=5, columnspan = 5)

        

    def evalaudio(self):
        while recording:
            with mic as input:
                r.adjust_for_ambient_noise(input)
                testaudio = r.listen(input)
            try:
                inputedaudio = r.recognize_google(testaudio)
                print(inputedaudio)
                detection = translator.detect(inputedaudio)
                translation = translator.translate(inputedaudio, dest = translang)
                self.audio_label["text"] = f"You said: '{inputedaudio} ({constants.LANGUAGES[detection.lang]})', \n The translation is: {translation} ({translang})"
                break
            except sr.UnknownValueError:
                print("Please repeat that, we couldn't understand what you just said!")

            
  

       


if __name__ == "__main__":
    app = App()
    app.mainloop()