import tkinter as tk
import os
import IncludedClasses.MainProgram as Main
import IncludedClasses.ClassOpenCV as CV
import IncludedClasses.ClassFacePI as PI
import IncludedClasses.ClassConfig as Config
from tkinter import messagebox
from tkinter.constants import DISABLED, E, NORMAL, RAISED, SUNKEN

class Window:

    def __init__(self):
        self.mode = 'Console'
        self.anwser = ''
        self.typing = False
        self.config = Config.Config()
        self.FacePI = Main.FacePI()
        self.detect = PI.Face()
        self.basepath = os.path.dirname(os.path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 10
        self.commandString = ["Acceptible Commands:\n'sign_in',\n'train'.", 
                "Acceptible Commands:\n'f_dt',\n'f_id_local',\n'f_id_url',\n'p_json',\n'lol'."]
        
    def c_print(self, text, mode = 'animated'):
        if(mode == 'animated'):
            self.CO['state'] = NORMAL
            if len(text) > 0:
                self.CO.insert(tk.END, text[0])
                if len(text) > 1:
                    self.CO.after(50, self.c_print, text[1:], mode)
                elif len(text) == 1: self.typing = True
        #    print(f"{len(text)}, {self.typing}")
        #    self.CO.update()
            self.CO['state'] = DISABLED
            self.CO.see("end")
        elif(mode == 'instant'):
            self.CO['state'] = NORMAL
            self.CO.insert(tk.END, text)
            self.CO['state'] = DISABLED
            self.CO.see("end")

    def get_person_data(self):
        def chkdata():
            if(name.get() == "" or description.get() == ""):
                if(name.get() == "" and not description.get() == ""): alertmsg.set("Please enter your name.")
                elif(description.get() == "" and not name.get() == ""): alertmsg.set("Please enter description for yourself.")
                else: alertmsg.set("Please enter both of them.")
            else:
                    prompt.destroy()
                    prompt.update()
                    self.FacePI.Train(description.get(), name.get())
                    self.c_print('\n' + self.FacePI.result, 'instant')
                    self.c_print('\n>_Returning to master console...\n')
                    self.CP['state'] = NORMAL
        prompt = tk.Toplevel()
        prompt.iconbitmap(self.basepath+'/Icon.ico')
        prompt.title("Person Data Fetcher")
        prompt.geometry('350x180')
        prompt.resizable(0,0)
        Cs = tk.Frame(prompt, width=200, height=200)
        Cs.pack()
        
        name = tk.StringVar()
        description = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel1 = tk.Label(Cs, text="Enter Your Name(In English):")
        userkeyin1 = tk.Entry(Cs, textvariable=name)
        inputlabel2 = tk.Label(Cs, text="Enter description for yourself(Ex: Sample 1): ")
        userkeyin2 = tk.Entry(Cs, textvariable=description)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro')
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg ='maroon')
        inputlabel1.pack()
        userkeyin1.pack()
        inputlabel2.pack()
        userkeyin2.pack()
        yrbtn.pack()
        msglabel.pack()
        
        yrbtn['command'] = chkdata
        
        prompt.mainloop()

    def get_imagepath(self, mode):
        def chkpath():
            if(path.get() == ""):
                if(mode == 'Local'): alertmsg.set("Please enter a image path.")
                elif(mode == 'URL'): alertmsg.set("Please enter a image url.")
            else:
                if(mode == 'Local' and not os.path.exists(path.get())):
                    alertmsg.set("Please enter a VALID image path.")
                elif(mode == 'URL' and not path.get().startswith("http")):
                    alertmsg.set("Please enter a VALID image url.")
                else:
                    prompt.destroy()
                    prompt.update()
                    self.FacePI.Signin(path.get())
                    for i in self.FacePI.result:
                        self.c_print('\n' + i, 'instant')
                    self.c_print('\n>_Returning to debug console...\n')
                    self.CP['state'] = NORMAL
        prompt = tk.Toplevel()
        prompt.iconbitmap(self.basepath+'/Icon.ico')
        prompt.title("Image Path Fetcher")
        prompt.geometry('350x150')
        prompt.resizable(0,0)
        Cs = tk.Frame(prompt, width=200, height=200)
        Cs.pack()
        path = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Enter Image Path(URL):")
        userkeyin = tk.Entry(Cs, textvariable=path)
        yrbtn = tk.Button(Cs, text="Confirm", width=20, bg='lightslategrey', fg='gainsboro')
        msglabel = tk.Label(Cs, textvariable=alertmsg, fg ='maroon')
        inputlabel.pack()
        userkeyin.pack()
        yrbtn.pack()
        msglabel.pack()
        
        yrbtn['command'] = chkpath
        
        prompt.mainloop()

    def get_size(self, event, obj=''):
        trg_obj = self.window if obj == '' else obj
        self.w, self.h = trg_obj.winfo_width(), trg_obj.winfo_height()

    def get_text(self, event):   
        self.anwser = self.CP.get(1.0, tk.END + "-1c")
        if(len(self.anwser) > 0 and self.anwser[0] == '\n'): self.anwser = self.anwser[1:]
        self.CP.delete('1.0','end')
        self.CP['state'] = DISABLED
        self.typing = False

        if(self.mode == 'Console'):
            if(self.anwser == 'sign_in'):
                self.c_print('\n>_Initializing Sign In protocol...', 'instant')
                self.FacePI.Signin('')
                for i in self.FacePI.result:
                    self.c_print('\n' + i, 'instant')
                self.c_print('\n>_Returning to master console...\n')
            elif(self.anwser == 'train'):
                self.c_print('\n>_Initializing Train protocol...', 'instant')
        #        self.FacePI.Train()
                self.get_person_data()
                self.c_print('\n>_Returning to master console...\n')
            else:
                self.c_print('\n>_Invaild command!\n')
        elif(self.mode == 'Debug'):
            if(self.anwser == 'f_dt'):
                self.c_print('\n>_Preparing for snapshot capture...', 'instant')
                self.detect.detectLocalImage(CV.show_opencv(' Smile :)'))
                self.c_print('\n>_Returning to debug console...\n')
            elif(self.anwser == 'f_id_local'):
                self.c_print('\n>_Require image path: ')
                self.get_imagepath('Local')
            elif(self.anwser == 'f_id_url'):
                self.c_print('\n>_Require image url: ')
                self.get_imagepath('URL')
            elif(self.anwser == 'p_json'):
                self.c_print('\n>_Printing Json File (config.json):\n', 'instant')
                self.window.after(200)
                self.c_print(f">_API Key:\n>_{self.config.readConfig()['api_key']}\n>_Host:\n>_{self.config.readConfig()['host']}\n>_Default Confidence:\n>_{self.config.readConfig()['confidence']}\n>_Default Person Group Name:\n>_{self.config.readConfig()['personGroupName']}\n>_Default Person Group ID:\n>_{self.config.readConfig()['personGroupID']}")
            elif(self.anwser == 'lol'):
                self.c_print('\n>_Bernie is the developer of this program.')
            else:
                self.c_print('\n>_Invaild command!')
        else:
            self.CP.delete('1.0','end+1c')
            self.CO.delete('1.0','end+1c')
            self.DS.delete('1.0','end+1c')
            self.CP['state'] = DISABLED
            self.c_print('How did we get here?')
            self.c_print('It should be impossible to reach here.')
            self.c_print('Error, please restart.')
            return 0
        self.CP['state'] = NORMAL

    def quit(self):
        quit_check = messagebox.askokcancel('Notification', 'Do you want to quit?')
        if quit_check:
            self.window.after(500)
            self.window.destroy()	
            os._exit()
            

    def console(self):
        self.answer = ''
        self.SC['relief'] = SUNKEN
        self.SC['state'] = DISABLED
        self.DM['relief'] = RAISED
        self.DM['state'] = NORMAL
        self.DS['state'] = NORMAL
        self.CO['state'] = NORMAL
        self.DS.delete('1.0','end+1c')
        self.CO.delete('1.0','end+1c')
        self.DS.insert(tk.END, self.commandString[0])
        self.DS['state'] = DISABLED
        self.c_print("Awaiting command...")
        self.mode = 'Console'

    def debug_mode(self):
        self.answer = ''
        self.DM['relief'] = SUNKEN
        self.DM['state'] = DISABLED
        self.SC['relief'] = RAISED
        self.SC['state'] = NORMAL
        self.DS['state'] = NORMAL
        self.CO['state'] = NORMAL
        self.DS.delete('1.0','end+1c')
        self.CO.delete('1.0','end+1c')
        self.DS.insert(tk.END, self.commandString[1])
        self.DS['state'] = DISABLED
        self.c_print("Awaiting command (Debug Mode Activated)...")
        self.mode = 'Debug'
    
    def reset(self):
        self.SC['relief'] = RAISED
        self.SC['state'] = NORMAL
        self.DM['relief'] = RAISED
        self.DM['state'] = NORMAL
        self.DS['state'] = NORMAL
        self.CO['state'] = NORMAL
        self.DS.delete('1.0','end+1c')
        self.CO.delete('1.0','end+1c')
        self.DS.insert(tk.END, 'Press \n"Start \nConsole" \nto activate \nthe program.')
        self.DS['state'] = DISABLED
        self.c_print("Welcome to Bernie's FacePI!")
        self.mode = 'Console'

    def activate(self):

        def define_layout(obj, cols=1, rows=1):
            def method(trg, col, row):
                [ trg.columnconfigure(c, weight=1)  for c in range(col) ]  
                [ trg.rowconfigure(r, weight=1)     for r in range(row) ]
            if type(obj)==list:        
                [ method(trg, cols, rows) for trg in obj ]
            else:
                method(obj, cols, rows)

        self.window = tk.Tk()
        self.window.title("Bernie's FacePI owo")
        self.window.iconbitmap(self.basepath+'/Icon.ico')
        self.window.resizable(0,0)

        self.upper, self.lower = 200, 400
        self.control_panel = tk.Frame(self.window,  width=self.upper , height=self.upper)
        self.description = tk.Frame(self.window,  width=self.lower , height=self.lower) 
        
        self.control_panel.grid(column=0, row=0, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.description.grid(column=0, row=1, padx=self.pad/2, pady=self.pad, sticky=self.align_mode)

        #Basic UI
        self.SC = tk.Button(self.control_panel, text='Start Console', bg='slategrey', fg='black', height=2)
        self.SC.grid(column=0, row=0, sticky=self.align_mode)
        self.DM = tk.Button(self.control_panel, text='Debug Mode', bg='slategrey', fg='black', height=2)
        self.DM.grid(column=1, row=0, sticky=self.align_mode)
        self.RE = tk.Button(self.control_panel, text='Reset', bg='gainsboro', fg='black', height=2)
        self.RE.grid(column=2, row=0, sticky=self.align_mode)
        self.QU = tk.Button(self.control_panel, text='Quit', bg='gainsboro', fg='black', height=2)
        self.QU.grid(column=3, row=0, sticky=self.align_mode)
        self.TM = tk.Label(self.control_panel, text='Made by Bernie', fg='steelblue', bg='lightgrey', font=("Gabriola", 17))
        self.TM.grid(column=4, row=0, ipadx = 10, sticky=E)
        self.DS = tk.Text(self.description, width=10, height=10, fg='goldenrod', font=("Arial", 8))
        self.DS.grid(column=0, row=0, sticky=self.align_mode, rowspan=2)
        self.CO = tk.Text(self.description, width=40, height=8, fg = 'dimgrey', font=("Calibri", 12))
        self.CO.grid(column=1, row=0, sticky=self.align_mode)
        self.CP = tk.Text(self.description, width=40, height=2, fg = 'black', font=("Calibri", 12))
        self.CP.grid(column=1, row=1, sticky=self.align_mode)
        self.reset()
        
        define_layout(self.window, cols=1, rows=1)

        self.SC['command'] = self.console
        self.DM['command'] = self.debug_mode
        self.RE['command'] = self.reset
        self.QU['command'] = self.quit

        self.isFullScreen = False
        self.CP.bind('<Return>', self.get_text)
    #    self.window.bind('<F4>', self.toggle_fullScreen)
    #    self.window.bind('<Escape>', self.quit)
    #    self.window.bind('<Configure>', lambda event, obj=self.description :self.get_size(event, obj))
        self.window.mainloop()