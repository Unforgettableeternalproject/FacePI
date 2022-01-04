import tkinter as tk
import platform, sys, time
from tkinter import messagebox
from PIL import Image, ImageTk

class Window:

    def __init__(self):
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
        is_windows = lambda : 1 if platform.system() == 'Windows' else 0

        self.isFullScreen = not self.isFullScreen
        self.window.attributes("-fullscreen" if is_windows() else "-zoomed", self.isFullScreen)

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

        self.div_size, self.img_size = 200, 400
        self.div1 = tk.Frame(self.window,  width=self.div_size , height=self.div_size)
        self.div2 = tk.Frame(self.window,  width=self.img_size , height=self.img_size) 

        self.div1.grid(column=0, row=0, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div2.grid(column=0, row=1, padx=self.pad, pady=self.pad, sticky=self.align_mode)

        self.bt1 = tk.Button(self.div1, text='Start Console', bg='slategrey', fg='black')
        self.bt1.grid(column=0, row=0, sticky=self.align_mode)
        self.bt2 = tk.Button(self.div1, text='Debug Mode', bg='slategrey', fg='black')
        self.bt2.grid(column=1, row=0, sticky=self.align_mode)
        self.bt3 = tk.Button(self.div1, text='Reset', bg='gainsboro', fg='black')
        self.bt3.grid(column=2, row=0, sticky=self.align_mode)
        self.bt4 = tk.Button(self.div1, text='Quit', bg='gainsboro', fg='black')
        self.bt4.grid(column=3, row=0, sticky=self.align_mode)
        self.readbt=tk.Button(self.div2, text="Read", height=1, width=10)
        self.textbox=tk.Text(self.div2, height=10)
        self.textbox.pack()
        

        
        define_layout(self.window, cols=1, rows=1)

        self.bt1['command'] = self.console
        self.bt2['command'] = self.debug_mode
        self.bt3['command'] = self.reset
        self.bt4['command'] = self.quit
        self.readbt['command'] = lambda text = self.textbox :self.get_text(text)

        self.isFullScreen = False
        self.window.bind('<F4>', self.toggle_fullScreen)
        self.window.bind('<Escape>', self.quit)
        self.window.bind('<Configure>', lambda event, obj=self.div2 :self.get_size(event, obj))
        self.readbt.pack()
        self.window.mainloop()
