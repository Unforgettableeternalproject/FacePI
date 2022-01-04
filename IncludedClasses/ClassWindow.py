import tkinter as tk
import platform, sys, time, os
from tkinter import messagebox
from tkinter.constants import E, W
from PIL import Image, ImageTk

class Window:

    def __init__(self):
        self.basepath = os.path.dirname(os.path.realpath(__file__))
        self.align_mode = 'nsew'
        self.pad = 10

    def get_size(self, event, obj=''):

        trg_obj = self.window if obj == '' else obj
        self.w, self.h = trg_obj.winfo_width(), trg_obj.winfo_height()
#        print(f'\r{(self.w, self.h)}', end='')

    def get_text(self, text):   
        self.result = text.get(1.0, tk.END+"-1c")
        print(f'Debug: {self.result}')

    def toggle_fullScreen(self):
        self.is_windows = lambda : 1 if platform.system() == 'Windows' else 0

        self.isFullScreen = not self.isFullScreen
        self.window.attributes("-fullscreen" if self.is_windows() else "-zoomed", self.isFullScreen)

    def quit(self):
        quit_check = messagebox.askokcancel('Notification', 'Do you want to quit?')
        if quit_check:
            print('\n>_Quitting the program...')
            self.window.destroy()	

    def console(self):
        print('hi - 1')

    def debug_mode(self):
        print('hi - 2')
    
    def reset(self):
        print('hi - 3')

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
        self.window.title('Test Tkinter Window owo')
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
        self.DS = tk.Text(self.description, width=10, height=10, fg='darkcyan', font=("Centaur", 16, "bold"))
        self.DS.grid(column=0, row=0, sticky=self.align_mode, rowspan=2)
        self.CO = tk.Text(self.description, width=40, height=8, fg = 'dimgrey', font=("Calibri", 12))
        self.CO.grid(column=1, row=0, sticky=self.align_mode)
        self.CP = tk.Text(self.description, width=40, height=2, fg = 'black', font=("Calibri", 12))
        self.CP.grid(column=1, row=1, sticky=self.align_mode)
#        self.DS.pack()
        

        
        define_layout(self.window, cols=1, rows=1)

        self.SC['command'] = self.console
        self.DM['command'] = self.debug_mode
        self.RE['command'] = self.reset
        self.QU['command'] = self.quit

        self.isFullScreen = False
        self.window.bind('<F4>', self.toggle_fullScreen)
        self.window.bind('<Escape>', self.quit)
        self.window.bind('<Configure>', lambda event, obj=self.description :self.get_size(event, obj))
        self.window.mainloop()
