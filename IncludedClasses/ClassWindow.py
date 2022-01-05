import tkinter as tk
import platform, sys, time, os, cv2
from typing import Collection
import IncludedClasses.MainProgram as Main
import IncludedClasses.ClassOpenCV as CV
import IncludedClasses.ClassFacePI as PI
import IncludedClasses.ClassConfig as Config
from tkinter import messagebox
from tkinter.constants import E, W

class Window:

    def __init__(self):
        self.mode = 'Console'
        self.anwser = ''
        self.config = Config.Config()
        self.FacePI = Main.FacePI()
        self.detect = PI.Face()
        self.basepath = os.path.dirname(os.path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 10
        self.commandString = ["Acceptible Commands:\n Sign in: 'sign_in',\n Train: 'train',\n End Program: 'end'.", 
                "Acceptible Commands:\n Face Detection(Only scan charateristics): 'f_dt',\n Face Identification(Local Image): 'f_id_local',\n Face Identification(From Internet): 'f_id_url',\n Print Config.json: 'p_json',\n Print Useful(Useless) infomation: 'lol'."]
        
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
                    self.CO.insert(tk.END, '\n>_Returning to debug console...\n')
                    self.CP['state'] = 'normal'
        prompt = tk.Toplevel()
        prompt.iconbitmap(self.basepath+'/Icon.ico')
        prompt.title("Image Path Fetcher")
        prompt.geometry('450x200')
        Cs = tk.Frame(prompt, width=200, height=200)
        Cs.pack()
        path = tk.StringVar()
        alertmsg = tk.StringVar()
        inputlabel = tk.Label(Cs, text="Enter Image Path(URL):")
        userkeyin = tk.Entry(Cs, textvariable=path)
        yrbtn = tk.Button(Cs, text="Confirm", width=20)
        msglabel = tk.Label(Cs, textvariable=alertmsg)
        inputlabel.pack()
        userkeyin.pack()
        yrbtn.pack()
        msglabel.pack()
        
        yrbtn['command'] = chkpath
        prompt.mainloop()

    def get_size(self, event, obj=''):
        trg_obj = self.window if obj == '' else obj
        self.w, self.h = trg_obj.winfo_width(), trg_obj.winfo_height()
#        print(f'\r{(self.w, self.h)}', end='')

    def get_text(self, event):   
        self.anwser = self.CP.get(1.0, tk.END + "-1c")
        self.CP.delete('1.0','end')
        self.CP['state'] = 'disabled'
        self.CO.insert(tk.END, '\n' + self.anwser + '\n' + self.mode)
        if(self.mode == 'Console'):
            if(self.anwser == 'sign_in'):
                self.CO.insert(tk.END, '\n>_Initializing Sign In protocol...\n')
                self.FacePI.Signin('')
                self.CO.insert(tk.END, '\n>_Returning to master console...\n')
            elif(self.anwser == 'train'):
                self.CO.insert(tk.END, '\n>_Initializing Train protocol...\n')
                self.FacePI.Train()
                self.CO.insert(tk.END, '\n>_Returning to master console...\n')
            else:
                self.CO.insert(tk.END, '\n>_Invaild command!\n')
        elif(self.mode == 'Debug'):
            if(self.anwser == 'f_dt'):
                self.CO.insert(tk.END, '\n>_Preparing for snapshot capture...')
                imagepath = CV.show_opencv()
                self.detect.detectLocalImage(imagepath)
                self.CO.insert(tk.END, '\n>_Returning to debug console...\n')
            elif(self.anwser == 'f_id_local'):
                self.CO.insert(tk.END, '\n>_Require image path: ')
                self.get_imagepath('Local')
            elif(self.anwser == 'f_id_url'):
                self.CO.insert(tk.END, '\n>_Require image url: ')
                self.get_imagepath('URL')
            elif(self.anwser == 'p_json'):
                self.CO.insert(tk.END, '\n>_Printing Json File (config.json):\n')
                self.CO.insert(tk.END, f"{self.config.readConfig()['api_key']}\n{self.config.readConfig()['host']}\n{self.config.readConfig()['confidence']}\n{self.config.readConfig()['title']}\n{self.config.readConfig()['personGroupName']}\n{self.config.readConfig()['personGroupID']}")
            elif(self.anwser == 'lol'):
                self.CO.insert(tk.END, '\n>_Bernie is the developer of this program.\n')
            else:
                self.CO.insert(tk.END, '\n>_Invaild command!\n')
        else:
            self.CP.delete('1.0','end+1c')
            self.CO.delete('1.0','end+1c')
            self.DS.delete('1.0','end+1c')
            self.CP['state'] = 'disabled'
            self.CO['state'] = 'disabled'
            self.DS['state'] = 'disabled'
            self.CO.insert(tk.END, 'How did we get here?')
            self.CP.insert(tk.END, 'It should be impossible to reach this mode.')
            self.DS.insert(tk.END, 'Error, please restart.')
            return 0
        self.CP['state'] = 'normal'

    #def toggle_fullScreen(self, event):
    #    self.is_windows = lambda : 1 if platform.system() == 'Windows' else 0

    #    self.isFullScreen = not self.isFullScreen
    #    self.window.attributes("-fullscreen" if self.is_windows() else "-zoomed", self.isFullScreen)

    def quit(self):
        quit_check = messagebox.askokcancel('Notification', 'Do you want to quit?')
        if quit_check:
            print('\n>_Quitting the program...')
            print('\nProgram Ended. Press any key to continue.')
            cv2.waitKey()
            self.window.destroy()	
            

    def console(self):
        self.answer = ''
        self.DS.delete('1.0','end+1c')
        self.CO.delete('1.0','end+1c')
        self.DS.insert(tk.END, self.commandString[0])
        self.CO.insert(tk.END, "Awaiting command...")
        self.mode = 'Console'

        

    def debug_mode(self):
        self.answer = ''
        self.DS.delete('1.0','end+1c')
        self.CO.delete('1.0','end+1c')
        self.DS.insert(tk.END, self.commandString[1])
        self.CO.insert(tk.END, "Awaiting command (Debug Mode Activated)...")
        self.mode = 'Debug'
    
    def reset(self):
        self.DS.delete('1.0','end+1c')
        self.DS.insert(tk.END, 'Press "Start Console" to activate the program.')
        self.CO.delete('1.0','end+1c')
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
        self.TM.grid(column=4, row=0, ipadx = 32, sticky=E)
        self.DS = tk.Text(self.description, width=10, height=10, fg='darkcyan', font=("Centaur", 10, "bold"))
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
        self.window.bind('<Configure>', lambda event, obj=self.description :self.get_size(event, obj))
        self.window.mainloop()
